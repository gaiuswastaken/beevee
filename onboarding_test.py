import os
import sys
import subprocess
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.clock import Clock
from config_manager import get_setting, enable_setting
from main_test import mainapp

# Simulate first run check
def is_first_run():
    setting = get_setting("Onboarding Complete")
    if setting and setting[0][0] == "False":
        return False
    else:
        return True


def mark_onboarding_complete():
    enable_setting("Onboarding Complete")

# ---------------- ONBOARDING ----------------
class OnboardingApp(MDApp):
    def build(self):
        return Label(text="Onboarding... Main app will launch, this will close in 5 seconds")

    def on_start(self):
        print("Launching main app...")
        
        # Mark onboarding complete
        mark_onboarding_complete()

        # Launch main app as separate process
        subprocess.Popen([sys.executable, __file__, "main"])

        # Close onboarding after 5 seconds
        Clock.schedule_once(lambda dt: self.stop(), .000005)


# ---------------- LAUNCH LOGIC ----------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "main":
        print("Running MAIN app")
        mainapp()

    else:
        if is_first_run():
            print("First run -> Onboarding")
            OnboardingApp().run()
        else:
            print("Not first run -> Main app")
            mainapp()