# Prevents the weird red dots from appearing when I hold the middle mouse button or start scrolling with the Ctrl key held (multi-touch emulation which is redundant for my purpose; a desktop app)
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')


# Forces 720p, scaling issues are a nightmare to fix
Config.set("graphics", "width", "1280")
Config.set("graphics", "height", "720")
Config.set("graphics", "resizable", "0")

# Check if this is the first run before loading everything else
def is_first_run():
    try:
        from config_manager import get_setting
        result = get_setting("Onboarding Complete")
        if not result:  # Setting doesn't exist (most likely because config.db hasn't been created yet by the onboarding screen)
            return True
        enabled = result[0][0]  # Get the first tuple's first value
        # If enabled is the string 'True', onboarding is complete, so not first run
        return enabled != 'True'
    except Exception as e:
        print(f"Error checking first run status: {e}")
        # If config.db doesn't exist or there's an error, assume first run
        return True

# If not first run, launch main app and exit
if __name__ == "__main__" and not is_first_run():
    print("Onboarding already complete - launching main app...")
    from main_screen import beevee
    beevee()
    exit()

# Libraries
from kivy.lang import Builder # Builds the KV statement
from kivy.utils import get_color_from_hex # Convert hex colors to RGBA
from kivy.properties import NumericProperty, ListProperty, DictProperty # For properties
from kivymd.app import MDApp # How to actually run the code
from kivy.clock import Clock # Allows for functions to be scheduled (useful for stuff that involves networking, in this case Gemini)
from threading import Thread # Allows for the use of threading (separate code executions, useful for running multiple things at once).
# Lets model our program as a kitchen, each thread would be a chef in a kitchen that is making a separate dish (threads are independent of each other).
import webbrowser # Opens the default web browser with a link as a parameter
import specification_creator # My module that creates the subject specification using Google Gemini
import requests # Validation of the Gemini API key
import os # Deletes redundant database files (if it failed so that Gemini can regenerate it without SQLite operation issues)
from colour_palette import * # My colour palette for the GUI
from currency_manager import create_honeycomb_currency_db
from inventory_manager import create_inventory
from index_manager import create_index, build_index
from config_manager import create_setting, enable_setting
import subprocess # For launching the main app after onboarding
import sys # For getting the current Python interpreter path to launch the main screen after onboarding


KV = """
MDScreen:
    Carousel:
        id: onboarding
        loop: False # If true, it will go on and on (which is not ideal)
        scroll_timeout: 0
        

        # Welcome Screen
        MDBoxLayout:
            orientation: "vertical"
            spacing: "24dp"
            padding: "32dp"
            md_bg_color: self.theme_cls.backgroundColor # Allows for dark mode in the future

            MDLabel:
                text: "Welcome to Beevee!!!"
                halign: "center"
                font_style: "Display"
                role: "medium"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"

            MDButton:
                style: "filled"
                pos_hint: {"center_x": 0.5}
                on_release: onboarding.load_next()
                
                MDButtonText:
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
                    text: "Let's go!"

        # Gemini API Key Setup
        MDBoxLayout:
            orientation: "vertical"
            spacing: "16dp"
            padding: "32dp"
            md_bg_color: self.theme_cls.backgroundColor # Allows for dark mode in the future
            
            MDLabel:
                text: "Please enter your Google Gemini API Key or get one if you don't (I am not giving you mine 😭)"
                halign: "center"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"

            MDTextField:
                id: api_key
                password: True
                
                MDTextFieldHintText:
                    text: "Gemini API Key"
                    
                MDTextFieldHelperText:
                    text: ""
                    mode: "on_focus"

            MDButton:
                style: "tonal"
                pos_hint: {"center_x": 0.5}
                on_release: app.open_api_docs()
                
                MDButtonText:
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
                    text: "How to get a Gemini API Key"
                

            MDButton:
                style: "tonal"
                pos_hint: {"center_x": 0.5}
                on_release: app.validate_api_key()
                
                MDButtonText:
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
                    text: "Submit API Key"

        # Subject 1 Input
        MDBoxLayout:
            orientation: "vertical"
            spacing: "16dp"
            padding: "32dp"
            md_bg_color: self.theme_cls.backgroundColor # Allows for dark mode in the future

            MDLabel:
                id: subject_title
                text: "Subject 1 of 4"
                halign: "center"
                font_style: "Headline"
                role: "medium"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
                
            MDLabel:
                id: subject_errors
                text: ""
                halign: "center"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"

            MDTextField:
                id: subject_input
                
                MDTextFieldHintText:
                    text: "Enter subject name"
                
                MDTextFieldHelperText:
                    text: ""
                    mode: "on_focus"
                
            MDTextField:
                id: url_input
                
                MDTextFieldHintText:
                    text: "Enter the URL of the subject specification"
                
                MDTextFieldHelperText:
                    text: ""
                    mode: "on_focus"

            MDButton:
                style: "filled"
                pos_hint: {"center_x": 0.5}
                on_release: app.start_gemini()
                
                MDButtonText:
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
                    text: "Generate specification"

        # Gemini Processing Page
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: self.theme_cls.backgroundColor # Allows for dark mode in the future

            MDLoadingIndicator:
                id: indicator
                size_hint: None, None
                size: sp(100), sp(100)
                pos_hint: {"center_x": 0.5, "center_y": 0.2}

            MDLabel:
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
                id: spinner_text
                text: "Gemini is working…"
                halign: "center"

        # Final Page
        MDBoxLayout:
            orientation: "vertical"
            spacing: "24dp"
            padding: "32dp"
            md_bg_color: self.theme_cls.backgroundColor # Allows for dark mode in the future

            MDLabel:
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
                font_style: "Display"
                role: "large"
                text: "You're all set! Welcome to Beevee!!! 🥳"
                halign: "center"
                #font_style: "H4"

            MDButton:
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
                style: "filled"
                pos_hint: {"center_x": 0.5}
                on_release: app.finish_onboarding()
                
                MDButtonText:
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
                    text: "Start studying"
"""

class OnboardingScreen(MDApp):
    key = "" # This way the API Key can be accessed throughout the application
    honeycombs_balance = NumericProperty(0)  # For KV file compatibility
    nav_bg_color = ListProperty()  # For KV file compatibility
    custom_colors = DictProperty({})  # For KV file compatibility
    def build(self):
        # Make spinner and buttons render properly
        self.theme_cls.theme_style = "Light" # Kind of self explanatory as this just determines the theme (light vs dark mode)
        self.apply_custom_theme()
        return Builder.load_string(KV)
    
    def apply_custom_theme(self):
        # Re-applies the custom palette. KivyMD resets these when theme_style changes.
        theme = self.theme_cls
        
        # Choose scheme based on theme style. KivyMD does not automatically handle light and dark mode for custom colour schemes
        scheme = (
            light_colourScheme
            if theme.theme_style == "Light"
            else dark_colourScheme
        )
        
        for key, value in scheme.items():
            # Validate that the value is a valid hex color string
            if isinstance(value, str) and (value.startswith("#") or value.startswith("rgba")):
                attr = key + "Color"   # appends Color to each key so that I can use the Material 3 convention.
                setattr(theme, attr, value)

    def on_start(self):
        # Builds the necessary non-subject databases
        create_honeycomb_currency_db()
        create_inventory()
        create_index()
        build_index()
        create_setting("Dark Mode")
        create_setting("Onboarding Complete")
        # Track which subject we're on (1..4)
        self.subject_index = 1
        self._update_subject_title()

    def _update_subject_title(self):
        try:
            self.root.ids.subject_title.text = f"Subject {self.subject_index} of 4"
        except Exception:
            pass

    def open_api_docs(self):
        webbrowser.open("https://github.com/gaiuswastaken/beevee/blob/main/GEMINI_KEY.md")

    def validate_api_key(self):
        global key
        key = self.root.ids.api_key.text.strip()
        
        # A fast request to ensure that the API Key is valid (takes like a second)
        geminiUrlValidator = "https://generativelanguage.googleapis.com/v1beta/models?key=" + key

        resp = requests.get(geminiUrlValidator)
        if resp.status_code != 200:
            # API Key Validation shenanigans
            # Code 200 means that the API key is valid
            self.root.ids.api_key.helper_text = f"Invalid key, code: {resp.status_code} - {resp.text}."
            self.root.ids.api_key.helper_text_mode = "on_error"
            self.root.ids.api_key.error = True
            print("Invalid key:", resp.status_code, resp.text)
            return
        self.api_key = key
        self.root.ids.onboarding.load_next()

    def start_gemini(self):
        subject = self.root.ids.subject_input.text.strip()
        url = self.root.ids.url_input.text.strip()
        if not subject:
            self.root.ids.subject_input.helper_text = "Please enter a subject"
            self.root.ids.subject_input.helper_text_mode = "on_error"
            self.root.ids.subject_input.error = True
            return

        if not url:
            self.root.ids.url_input.helper_text = "Please enter a URL"
            self.root.ids.url_input.helper_text_mode = "on_error"
            self.root.ids.url_input.error = True
            return

        # If we're on the 4th subject and the user explicitly says 'none', skip processing and go to final
        if self.subject_index == 4 and subject.lower() == "none":
            self.root.ids.subject_input.text = ""
            self.root.ids.url_input.text = ""
            self.root.ids.onboarding.index = 4
            return

        # Clear any previous error hints
        self.root.ids.subject_input.helper_text = ""
        self.root.ids.subject_input.error = False
        self.root.ids.url_input.helper_text = ""
        self.root.ids.url_input.error = False

        self.root.ids.spinner_text.text = f"Creating specification for {subject}"
        self.root.ids.indicator.start()
        # Move to the processing page (it's the next carousel slide)
        self.root.ids.onboarding.load_next()

        Thread(target=self._gemini_worker, args=(subject, url, key), daemon=True).start()

    def _gemini_worker(self, subject, url, api_key_param):
        # Call the specification creator which returns a list of errors (empty if successful)
        try:
            errors = specification_creator.sub_list_gen(url, subject, api_key_param)
        except Exception as e:
            errors = [f"Internal error: {e}"]
        # 'lambda' is a way for a small function to be defined without a name. There is no main benefit apart from making my (long) code shorter
        Clock.schedule_once(lambda dt: self.finish_gemini(subject, errors))

    def finish_gemini(self, subject, result):
        # Stop spinner
        try:
            self.root.ids.indicator.stop()
        except Exception:
            pass

        # If result is a list it consists of errors, otherwise treat as success message
        if isinstance(result, list) and result:
            # Display errors on the URL field helper text and go back to subject input
            msg = "; ".join(result)
            self.root.ids.url_input.helper_text = msg
            self.root.ids.url_input.helper_text_mode = "on_error"
            self.root.ids.url_input.error = True
            self.root.ids.spinner_text.text = "Errors occurred"
            print("SPEC ERRORS:", subject, "=>", result)
            # Return the carousel to the subject input page
            try:
                self.root.ids.onboarding.index = self.root.ids.onboarding.index-1 # This returns the carousel to the last page the user was on
                self.root.ids.subject_errors.text = str(msg) # This prints all the possible errors in the inputs (not the most user friendly but will do)
                
                # Now need to delete the redundant files (if they are found)
                program_dir = os.path.dirname(os.path.abspath(__file__))
                redundant_db = os.path.join(program_dir,f"{subject}.db")
                redundant_sql = os.path.join(program_dir,f"{subject}.sql")
                if os.path.isfile(redundant_db):
                    os.remove(redundant_db)
                if os.path.isfile(redundant_sql):
                    os.remove(redundant_sql)
            except Exception:
                pass
            return

        # Success: if more subjects remain, go back to the subject input; otherwise finish
        print("SPEC:", subject, "=>", result)
        self.root.ids.subject_input.text = ""
        self.root.ids.url_input.text = ""
        # Clear any previous error messages on success
        self.root.ids.subject_errors.text = ""
        self.root.ids.url_input.error = False

        if self.subject_index < 4:
            self.subject_index += 1
            self._update_subject_title()
            self.root.ids.spinner_text.text = f"Ready for subject {self.subject_index}"
            try:
                self.root.ids.onboarding.index = 2
            except Exception:
                pass
            return

        # Finished all subjects -> go to final page
        self.root.ids.spinner_text.text = f"Created specification for {subject}"
        try:
            self.root.ids.onboarding.index = 4
        except Exception:
            pass
    
    def launch_beevee(self):
        from main_screen import beevee # The main screen (where the user will spend most of their time after onboarding)
        # I have to import it here otherwise the Main Screen would show up first
        beevee()

    def finish_onboarding(self):
        print("Onboarding complete!")
        enable_setting("Onboarding Complete")
        # I should call it so that the main app gets launched
        process = subprocess.Popen([sys.executable, "main_screen.py"])
        process.start()
        Clock.schedule_once(lambda dt: self.stop(), 5)  # Stops the onboarding screen so that the main screen can be shown (otherwise they would run at the same time and confuse the user)

if __name__ == "__main__": # Necessary to prevent the code from being run when imported
    print("First run detected - launching onboarding...")
    OnboardingScreen().run()
