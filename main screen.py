import os # For accessing the databases
import glob # For searching the databases
from kivy.lang import Builder # Builds the KV statement
from kivymd.app import MDApp # How to actually run the code
from kivy.properties import StringProperty # For properties that are strings such as MDNavigationRailItemIcoon
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivymd.uix.list import MDListItem
from kivy.uix.behaviors import ButtonBehavior
from fsrs_db_editor import editor_main # My database editor

KV = """
# Template class for the Rail item so that I dont have to repeat stuff multiple times
# I just found out about it recently (feels like I just had a eureka moment!)

# Forces NavItem to inherit MDNavigationRailItem
<NavItem>:
    
    on_active:
        if args[1]: app.root.ids.screen_manager.current = root.screen_name

    MDNavigationRailItemIcon:
        icon: root.icon
        pos_hint: {"center_x": 0.5,"y": 1}  # Moves the icon up

    # MDNavigationRailItemLabel:
    #     text: root.text
    #     #pos_hint: {"y": -1}  # Moves the label up
    
# Creates a new class called DBItem where I can alter the text and what will happen if I click on it
<DBItem>:
    divider: True
    MDListItemSupportingText:
        text: root.text
        
        
MDBoxLayout:

    MDNavigationRail:
        type: "unselected" # Never shows the label (only way that I can get larger padding :( )
        spacing: "8dp"
        padding: "8dp"
        md_bg_color: app.theme_cls.secondaryContainerColor

        NavItem:
            icon: "text-box-edit"
            text: "Editor"
            screen_name: "editor"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"

        NavItem:
            icon: "store"
            text: "Shop"
            screen_name: "shop"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"

        NavItem:
            icon: "home"
            text: "Tasks"
            screen_name: "home"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"
            

        NavItem:
            icon: "bag-personal"
            text: "Inventory"
            screen_name: "inventory"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"

        NavItem:
            icon: "book"
            text: "Index"
            screen_name: "index"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"

        NavItem:
            icon: "cog"
            text: "Settings"
            screen_name: "settings"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"

    MDScreenManager:
        id: screen_manager
        current: ""
        md_bg_color: app.theme_cls.backgroundColor # This way, dark mode is also supported
        
        # The blank screen that shows up first (when the main program is launched)
        MDScreen:
            name: "blank"
            MDBoxLayout:
                MDLabel:
                    text: "Click on the home icon to see your tasks 😊"
                    halign: "center"
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
        
        # The editor
        MDScreen:
            name: "editor"
            FloatLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                MDLabel:
                    text: "Editor"
                    halign: "center"
                    pos_hint: {"center_y": 0.9}
                    theme_font_name: "Custom"
                    font_style: "Display"
                    role: "small"
                    font_name: "robotvar.ttf"
                
                MDLabel:
                    text: "Choose your database to edit and the editor will open here"
                    halign: "center"
                    pos_hint: {"center_y": 0.8}
                    theme_font_name: "Custom"
                    font_style: "Headline"
                    role: "small"
                    font_name: "robotvar.ttf"
                
                # Where the databases are listed   
                MDScrollView:
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    size_hint: 0.5, 0.5
                    do_scroll_x: False
                    MDBoxLayout:
                        id: dblist
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        
        
        # The Shop            
        MDScreen:
            name: "shop"
            MDBoxLayout:
                MDLabel:
                    text: "Shop"
                    halign: "center"
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
        
        # The homepage - where the tasks are shown
        MDScreen:
            name: "home"
            MDBoxLayout:
                MDLabel:
                    text: "Tasks"
                    halign: "center"
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
        
        # The inventory
        MDScreen:
            name: "inventory"
            MDBoxLayout:
                MDLabel:
                    text: "Inventory"
                    halign: "center"
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
        
        # The index         
        MDScreen:
            name: "index"
            MDBoxLayout:
                MDLabel:
                    text: "Index"
                    halign: "center"
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
        
        # The settings page (implement last as minor)            
        MDScreen:
            name: "settings"
            MDBoxLayout:
                MDLabel:
                    text: "Settings"
                    halign: "center"
                    theme_font_name: "Custom"
                    font_name: "robotvar.ttf"
        
"""

# This defines the class NavItem outside of the KV so that Kivy Understands what it is
class NavItem(MDNavigationRailItem):
    text = StringProperty() # The text underneath the icon
    icon = StringProperty() # The icon used to depict the function of a page
    screen_name = StringProperty() # The name of the screen to display
    
class DBItem(MDListItem, ButtonBehavior):
    text = StringProperty() # The text used to show the databases' app
    
    
class MainScreen(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light" # Kind of self explanatory as this just determines the theme (light vs dark mode)
        self.theme_cls.primary_palette = "Cyan" # The accent colour, might change this to a more 'bee-themed' colour
        self.theme_cls.primary_hue = "500" # Controls how light or dark this is (500 is a balance between light and dark)
        root = Builder.load_string(KV)
        return root
    
    def openDB(self, text):
        print(f"Opening database: {text}")
        # start the editor in a separate process so the current window stays open
        import subprocess, sys
        python = sys.executable
        # pass the database filename as an argument
        subprocess.Popen([python, "fsrs_db_editor.py", text])
        # optionally you could also call editor_main(text) if you want an in‑process run
        
    def on_start(self):
        
        databases = glob.glob("*.db")
        for db in databases:
            item = DBItem(text=db)
            # on_release sends the widget instance as first arg, so capture db separately
            item.bind(on_release=lambda instance, db=db: self.openDB(db))
            self.root.ids.dblist.add_widget(item)
    

MainScreen().run()
