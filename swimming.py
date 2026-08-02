import string
import random
import os
import ast
import customtkinter as ctk

# --- INITIAL FILE SETUP ---
if not os.path.exists('swimming_clubs.txt'):
    with open('swimming_clubs.txt', 'w') as swim:
        swim.write('Dar Swim Club\n')
        swim.write('FK Blue Marlins\n')
        swim.write('Taliss\n')

if not os.path.exists('swimming_events.txt'):
    with open('swimming_events.txt', 'w') as f:
        f.write('1. Freestyle (Free) - 50m, 100m, 200m\n')
        f.write('2. Backstroke - 50m, 100m\n')
        f.write('3. Butterfly (Fly) - 50m, 100m\n')

if not os.path.exists('swimmers.txt'):
    with open('swimmers.txt', 'w') as swim:
        swim.write('mark\n')
        swim.write('cathleen\n')
        swim.write('amelia\n')
        swim.write('derek\n')

# --- THEME SETUP ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class SwimmingPortalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tanzania Swimming Association Portal")
        self.geometry("500x720")
        self.resizable(False, False)

        self.current_user = None
        self.show_welcome_screen()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- VALIDATION LOGIC ---
    def validate_username(self, user_name):
        if len(user_name) < 8:
            return False, "Username is too short (minimum 8 characters)."
        if not any(c.isdigit() for c in user_name):
            return False, "Include at least one number."
        if not any(c in string.punctuation for c in user_name):
            return False, "Include a special character (@, #, $)."
        if not any(c in string.ascii_lowercase for c in user_name):
            return False, "Include a lowercase letter."
        if not any(c in string.ascii_uppercase for c in user_name):
            return False, "Include an uppercase letter."
        return True, "Valid"

    def validate_password(self, character):
        if len(character) < 8:
            return False, "Password is too short (minimum 8 characters)."
        if not any(c.isdigit() for c in character):
            return False, "Include at least one number."
        if not any(c in string.punctuation for c in character):
            return False, "Include a special character (@, #, $)."
        if not any(c in string.ascii_lowercase for c in character):
            return False, "Include a lowercase letter."
        if not any(c in string.ascii_uppercase for c in character):
            return False, "Include an uppercase letter."
        return True, "Valid"

    # --- WELCOME SCREEN ---
    def show_welcome_screen(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="TANZANIA SWIMMING PORTAL", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(40, 30))

        btn_create = ctk.CTkButton(self, text="Create Account Manually", command=self.show_manual_create_screen, width=320, height=45)
        btn_create.pack(pady=15)

        btn_gen = ctk.CTkButton(self, text="Generate Credentials Automatically", command=self.show_generate_screen, width=320, height=45)
        btn_gen.pack(pady=15)

        btn_login = ctk.CTkButton(self, text="Login to Existing Account", command=self.show_login_screen, width=320, height=45, fg_color="transparent", border_width=2)
        btn_login.pack(pady=15)

    # --- MANUAL CREATION SCREEN ---
    def show_manual_create_screen(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="Create New Account", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(20, 10))

        self.err_label = ctk.CTkLabel(self, text="", text_color="red", font=ctk.CTkFont(size=12))
        self.err_label.pack(pady=5)

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Create Username", width=320, height=40)
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Create Password", show="*", width=320, height=40)
        self.pass_entry.pack(pady=10)

        self.confirm_entry = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*", width=320, height=40)
        self.confirm_entry.pack(pady=10)

        btn_submit = ctk.CTkButton(self, text="Register & Save", command=self.process_manual_creation, width=320, height=40)
        btn_submit.pack(pady=15)

        btn_back = ctk.CTkButton(self, text="Back", command=self.show_welcome_screen, width=320, height=35, fg_color="gray")
        btn_back.pack(pady=5)

    def process_manual_creation(self):
        uname = self.user_entry.get()
        pwd = self.pass_entry.get()
        cpwd = self.confirm_entry.get()

        valid_u, msg_u = self.validate_username(uname)
        if not valid_u:
            self.err_label.configure(text=msg_u)
            return

        if pwd != cpwd:
            self.err_label.configure(text="Passwords do not match. Try again.")
            return

        valid_p, msg_p = self.validate_password(pwd)
        if not valid_p:
            self.err_label.configure(text=msg_p)
            return

        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                if any(uname in line for line in file):
                    self.err_label.configure(text="That username is already taken! Please log in.")
                    return

        with open('users.txt', 'a') as file:
            file.write(f"('{uname}', '{pwd}')\n")

        self.current_user = uname
        self.show_dashboard()

    # --- GENERATOR SCREEN ---
    def show_generate_screen(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="Generate Credentials", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(20, 10))

        self.info_label = ctk.CTkLabel(self, text="Automatically generate strong credentials:", font=ctk.CTkFont(size=12))
        self.info_label.pack(pady=5)

        btn_generate = ctk.CTkButton(self, text="Generate & Save Credentials", command=self.process_generation, width=320, height=45)
        btn_generate.pack(pady=20)

        self.result_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13, weight="bold"), text_color="green")
        self.result_label.pack(pady=10)

        self.dash_btn = ctk.CTkButton(self, text="Continue to Dashboard", command=lambda: self.show_dashboard(), width=320, height=40, state="disabled")
        self.dash_btn.pack(pady=10)

        btn_back = ctk.CTkButton(self, text="Back", command=self.show_welcome_screen, width=320, height=35, fg_color="gray")
        btn_back.pack(pady=5)

    def process_generation(self):
        char_pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        gen_name = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(9))
        gen_pass = "".join(random.choice(char_pool) for _ in range(10))

        with open('users.txt', 'a') as file:
            file.write(f"('{gen_name}', '{gen_pass}')\n")

        self.current_user = gen_name
        self.result_label.configure(text=f"Generated User: {gen_name}\nGenerated Pass: {gen_pass}")
        self.dash_btn.configure(state="normal")

    # --- LOGIN SCREEN ---
    def show_login_screen(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="Portal Login", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(20, 10))

        self.login_err = ctk.CTkLabel(self, text="", text_color="red")
        self.login_err.pack(pady=5)

        self.login_user = ctk.CTkEntry(self, placeholder_text="Enter Username", width=320, height=40)
        self.login_user.pack(pady=10)

        self.login_pass = ctk.CTkEntry(self, placeholder_text="Enter Password", show="*", width=320, height=40)
        self.login_pass.pack(pady=10)

        btn_login = ctk.CTkButton(self, text="Login", command=self.process_login, width=320, height=40)
        btn_login.pack(pady=15)

        btn_back = ctk.CTkButton(self, text="Back", command=self.show_welcome_screen, width=320, height=35, fg_color="gray")
        btn_back.pack(pady=5)

    def process_login(self):
        uname = self.login_user.get()
        pwd = self.login_pass.get()

        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    if uname in line and pwd in line:
                        self.current_user = uname
                        self.show_dashboard()
                        return
            self.login_err.configure(text="Invalid username or password.")
        except FileNotFoundError:
            self.login_err.configure(text="No users found yet. Please sign up first.")

    # --- DASHBOARD SCREEN ---
    def show_dashboard(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="TANZANIA SWIMMING DASHBOARD", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(20, 5))

        user_info = ctk.CTkLabel(self, text=f"Logged in as: [{self.current_user}]", text_color="green", font=ctk.CTkFont(size=13, weight="bold"))
        user_info.pack(pady=(0, 15))

        btn_profile = ctk.CTkButton(self, text="1. Build / Add Swimmer Profile", command=self.show_profile_screen, width=340, height=38)
        btn_profile.pack(pady=8)

        btn_events = ctk.CTkButton(self, text="2. Register for Swimming Races & Events", command=self.show_events_screen, width=340, height=38)
        btn_events.pack(pady=8)

        btn_clubs = ctk.CTkButton(self, text="3. View Registered Swimming Clubs", command=self.show_clubs_screen, width=340, height=38)
        btn_clubs.pack(pady=8)

        btn_view_profiles = ctk.CTkButton(self, text="4. View Swimmer Profiles & Events", command=self.show_view_profiles_screen, width=340, height=38, fg_color="#2b7a78", hover_color="#17252a")
        btn_view_profiles.pack(pady=8)

        btn_logout = ctk.CTkButton(self, text="5. Log out / Exit", command=self.show_welcome_screen, width=340, height=38, fg_color="#b22222", hover_color="#8b0000")
        btn_logout.pack(pady=15)

    # --- FEATURE 1: SWIMMER PROFILE SCREEN (Redesigned with more space & event integration) ---
    def show_profile_screen(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="CREATE SWIMMER PROFILE", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(12, 5))

        self.age_entry = ctk.CTkEntry(self, placeholder_text="Enter Age", width=360, height=35)
        self.age_entry.pack(pady=6)

        self.height_entry = ctk.CTkEntry(self, placeholder_text="Enter Height (e.g., 175 cm)", width=360, height=35)
        self.height_entry.pack(pady=6)

        self.mass_entry = ctk.CTkEntry(self, placeholder_text="Enter Weight (e.g., 65 kg)", width=360, height=35)
        self.mass_entry.pack(pady=6)

        self.club_entry = ctk.CTkEntry(self, placeholder_text="Enter Club Name", width=360, height=35)
        self.club_entry.pack(pady=6)

        # Category Selection Menu
        cat_label = ctk.CTkLabel(self, text="Select Specialization Category:", font=ctk.CTkFont(size=12, weight="bold"))
        cat_label.pack(pady=(6, 2))
        self.cat_menu = ctk.CTkOptionMenu(self, values=["Sprinter", "Middle Distance", "Butterfly Specialist", "Backstroke Specialist"], width=360, height=35)
        self.cat_menu.pack(pady=4)

        # Primary Event Selection Menu (Integrated into Profile Creation)
        event_label = ctk.CTkLabel(self, text="Select Primary Event/Stroke:", font=ctk.CTkFont(size=12, weight="bold"))
        event_label.pack(pady=(6, 2))
        
        events_list = [
            "Freestyle (Free) - 50m, 100m, 200m",
            "Backstroke - 50m, 100m",
            "Butterfly (Fly) - 50m, 100m"
        ]
        self.event_menu = ctk.CTkOptionMenu(self, values=events_list, width=360, height=35)
        self.event_menu.pack(pady=4)

        # Large Space for Race Times
        race_label = ctk.CTkLabel(self, text="Notable Race Times (Provide details below):", font=ctk.CTkFont(size=12, weight="bold"))
        race_label.pack(pady=(6, 2))
        self.race_textbox = ctk.CTkTextbox(self, width=360, height=80)
        self.race_textbox.pack(pady=4)

        btn_save = ctk.CTkButton(self, text="Save Swimmer Profile & Event", command=self.save_profile_data, width=360, height=40)
        btn_save.pack(pady=10)

        btn_back = ctk.CTkButton(self, text="Back to Dashboard", command=self.show_dashboard, width=360, height=35, fg_color="gray")
        btn_back.pack(pady=5)

    def save_profile_data(self):
        race_times_text = self.race_textbox.get("0.0", "end").strip().replace("\n", " ")

        swimmer_data = {
            "username": self.current_user,
            "age": self.age_entry.get(),
            "height": self.height_entry.get(),
            "mass": self.mass_entry.get(),
            "club": self.club_entry.get(),
            "category": self.cat_menu.get(),
            "race_times": race_times_text
        }

        # Save profile
        with open('swimmers_profiles.txt', 'a') as file:
            file.write(f"{swimmer_data}\n")

        # Automatically register the selected event/stroke as requested
        selected_event = self.event_menu.get()
        registration_record = {
            "username": self.current_user,
            "event": selected_event
        }

        with open('event_registrations.txt', 'a') as file:
            file.write(f"{registration_record}\n")

        self.show_dashboard()

    # --- FEATURE 2: EVENTS REGISTRATION SCREEN ---
    def show_events_screen(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="SWIMMING EVENTS & RACES", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(20, 10))

        events_text = ""
        try:
            with open('swimming_events.txt', 'r') as file:
                events_text = file.read()
        except FileNotFoundError:
            events_text = "Events file not found."

        info = ctk.CTkLabel(self, text=events_text, justify="left", font=ctk.CTkFont(size=12))
        info.pack(pady=10)

        self.event_choice = ctk.CTkEntry(self, placeholder_text="Select event number (1-3)", width=320, height=35)
        self.event_choice.pack(pady=15)

        btn_reg = ctk.CTkButton(self, text="Register for Event", command=self.save_event_registration, width=320, height=40)
        btn_reg.pack(pady=10)

        btn_back = ctk.CTkButton(self, text="Back to Dashboard", command=self.show_dashboard, width=320, height=35, fg_color="gray")
        btn_back.pack(pady=5)

    def save_event_registration(self):
        choice = self.event_choice.get()
        event_name = ""
        if choice == '1':
            event_name = "Freestyle (Free) - 50m, 100m, 200m"
        elif choice == '2':
            event_name = "Backstroke - 50m, 100m"
        elif choice == '3':
            event_name = "Butterfly (Fly) - 50m, 100m"
        else:
            return

        registration_record = {
            "username": self.current_user,
            "event": event_name
        }

        with open('event_registrations.txt', 'a') as file:
            file.write(f"{registration_record}\n")

        self.show_dashboard()

    # --- FEATURE 3: VIEW CLUBS SCREEN ---
    def show_clubs_screen(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="REGISTERED CLUBS", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(20, 10))

        clubs_content = ""
        try:
            with open('swimming_clubs.txt', 'r') as file:
                clubs_content = file.read()
        except FileNotFoundError:
            clubs_content = "Club list file not found."

        textbox = ctk.CTkTextbox(self, width=400, height=220)
        textbox.pack(pady=10)
        textbox.insert("0.0", clubs_content)
        textbox.configure(state="disabled")

        btn_back = ctk.CTkButton(self, text="Back to Dashboard", command=self.show_dashboard, width=320, height=35, fg_color="gray")
        btn_back.pack(pady=20)

    # --- FEATURE 4: VIEW PROFILES, RACE TIMES & STROKES ---
    def show_view_profiles_screen(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="SWIMMER PROFILES & REGISTERED STROKES", font=ctk.CTkFont(size=15, weight="bold"))
        title.pack(pady=(15, 10))

        profiles = []
        if os.path.exists('swimmers_profiles.txt'):
            with open('swimmers_profiles.txt', 'r') as f:
                for line in f:
                    try:
                        profiles.append(ast.literal_eval(line.strip()))
                    except:
                        pass

        events_dict = {}
        if os.path.exists('event_registrations.txt'):
            with open('event_registrations.txt', 'r') as f:
                for line in f:
                    try:
                        ev = ast.literal_eval(line.strip())
                        uname = ev.get('username')
                        events_dict.setdefault(uname, []).append(ev.get('event'))
                    except:
                        pass

        display_content = ""
        if not profiles:
            display_content = "No swimmer profiles created yet."
        else:
            for p in profiles:
                uname = p.get('username', 'Unknown')
                display_content += f"Swimmer: {uname}\n"
                display_content += f"  - Age: {p.get('age')} | Club: {p.get('club')}\n"
                display_content += f"  - Height: {p.get('height')} | Weight: {p.get('mass')}\n"
                display_content += f"  - Category: {p.get('category')}\n"
                display_content += f"  - Notable Times: {p.get('race_times')}\n"
                
                user_strokes = events_dict.get(uname, [])
                if user_strokes:
                    display_content += f"  - Registered Strokes / Events:\n"
                    # Remove duplicates if any
                    for s in list(set(user_strokes)):
                        display_content += f"    * {s}\n"
                else:
                    display_content += f"  - Registered Strokes: None yet\n"
                display_content += "-" * 45 + "\n\n"

        textbox = ctk.CTkTextbox(self, width=440, height=380)
        textbox.pack(pady=10)
        textbox.insert("0.0", display_content)
        textbox.configure(state="disabled")

        btn_back = ctk.CTkButton(self, text="Back to Dashboard", command=self.show_dashboard, width=320, height=35, fg_color="gray")
        btn_back.pack(pady=15)


if __name__ == "__main__":
    try:
        app = SwimmingPortalApp()
        app.mainloop()
    except Exception as e:
        import traceback
        print("\n" + "="*50)
        print("CRITICAL ERROR UPON STARTUP:")
        print("="*50)
        traceback.print_exc()
        print("="*50)
        input("\nAn error occurred. Press Enter to close this window...")
