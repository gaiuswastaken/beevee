# Prevents the weird red dots from appearing when I hold the middle mouse button or start scrolling with the Ctrl key held (multi-touch emulation which is redundant for my purpose; a desktop app)
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Forces 720p, scaling issues are a nightmare to fix
Config.set("graphics", "width", "1280")
Config.set("graphics", "height", "720")
Config.set("graphics", "resizable", "0")

# General Libraries
from kivy.lang import Builder # Builds the KV statement
from kivymd.app import MDApp # How to actually run the code
from kivy.properties import StringProperty # For properties that are strings such as MDNavigationRailItemIcoon
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivymd.uix.list import MDListItem
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from colour_palette import colourScheme # My colour palette for the GUI

# Libraries for the editor screen
import os # For accessing the databases
import glob # For searching the databases
from fsrs_db_editor import editor_main # My database editor
import subprocess # How I can open my editor in a separate window
import sys # Used to get the absolute path of the Python interpreter
# Libraries for the shop screen

# Libraries for the task screen
from kivy.properties import DictProperty
from spaced_repetition_planner import spaced_repetition_recommendations # My module for the spaced repetition planner

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
        theme_font_name: "Custom"
        font_name: "robotvar.ttf"
        
# Creates a new class called EggFrame where I can just clone the control variables and alter stuff like image and text and tooltip text
<EggFrame>:
    size_hint: None, 1
    #spacing: dp(25)
    radius: 20
    height: self.parent.height
    width: root.height *0.75
    md_bg_color: app.theme_cls.primaryContainerColor
    
    RelativeLayout: # Makes positioning things much easier
        width: root.height * 0.75
        height: self.parent.height
        md_bg_color: app.theme_cls.tertiaryColor
        size_hint: None, 1
        MDBoxLayout:
            size_hint: None, None
            width: 0.4 * self.parent.parent.height
            spacing: "25dp"
            height: 0.4 * self.parent.parent.height
            pos_hint: {"center_x": 0.5,"center_y": 0.75}
            radius: 20
            md_bg_color: app.theme_cls.secondaryContainerColor
            
        MDLabel:
            id: name
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            halign: "center"
            text: root.name
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"
            
        MDLabel:
            id: cost
            pos_hint: {"center_x": 0.5, "center_y": 0.35}
            halign: "center"
            text: root.cost
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"
            
        MDButton:
            pos_hint: {"center_x": 0.5, "center_y": 0.25}
            halign: "center"
            style: "tonal"
            
            MDButtonIcon:
                icon: "shopping"
                
            MDButtonText:
                text: "Buy"
                #pos_hint: {"center_x": 0.5, "center_y": 0.5}
                halign: "center"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
                
<SubjectFrame>:
    size_hint: 1, None
    #halign: center
    #pos_hint: root.pos_hint_value
    #spacing: dp(25)
    radius: 20
    height: dp(160)
    width: self.parent.height *0.45
    md_bg_color: app.theme_cls.tertiaryColor
    
    MDLabel:
        text: root.text
        pos_hint: {"center_x": 0.5, "center_y": 0.8}
        halign: "center"
        theme_font_name: "Custom"
        font_name: "robotvar.ttf"

MDBoxLayout:

    MDNavigationRail:
        type: "unselected" # Never shows the label (only way that I can get larger padding :( )
        spacing: "8dp"
        padding: "8dp"
        md_bg_color: app.theme_cls.primaryContainerColor

        NavItem:
            icon: "text-box-edit"
            text: "Editor"
            screen_name: "editor"
            

        NavItem:
            icon: "store"
            text: "Shop"
            screen_name: "shop"

        NavItem:
            icon: "home"
            text: "Tasks"
            screen_name: "home"

        NavItem:
            icon: "bag-personal"
            text: "Inventory"
            screen_name: "inventory"

        NavItem:
            icon: "book"
            text: "Index"
            screen_name: "index"

        NavItem:
            icon: "cog"
            text: "Settings"
            screen_name: "settings"

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
                    scroll_type: ['bars', 'content']
                    bar_color: app.theme_cls.secondaryColor        # color when scrolling
                    bar_color_inactive: app.theme_cls.secondaryColor
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    size_hint: 0.5, 0.5
                    do_scroll_x: False
                    bar_width: dp(4)
                    MDBoxLayout:
                        id: dblist
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        
        
        # The Shop            
        MDScreen:
            name: "shop"
            MDLabel:
                text: "Shop"
                pos_hint: {"center_y": 0.95}
                halign: "center"
                theme_font_name: "Custom"
                font_style: "Headline"
                role: "small"
                font_name: "robotvar.ttf"
    
            MDAnchorLayout:
                anchor_x: "center"
                anchor_y: "center"
                #size_hint_y: None
                
                MDScrollView:
                    scroll_type: ['bars', 'content']
                    bar_color: app.theme_cls.secondaryColor        
                    bar_color_inactive: app.theme_cls.secondaryColor
                    size_hint: None, None
                    width: root.width * 0.85
                    height: root.height * 0.85
                    do_scroll_x: True
                    do_scroll_y: False
                    bar_width: dp(4)
                    padding: dp(10)

                    MDGridLayout:
                        id: shop_grid
                        rows: 1
                        size_hint_x: None
                        radius: 20
                        height: self.parent.height
                        md_bg_color: app.theme_cls.primaryColor
                        width: max(self.minimum_width, self.parent.width)
                        

                        spacing: dp(25)
                        padding: dp(10)

                        EggFrame:
                            name: "Starter"
                            cost: "1 Coin"
                        
                        EggFrame:
                            name: "Rare"
                            cost: "2 Coins"
                            
                        EggFrame:
                            name: "Epic"
                            cost: "3 Coins"
                                       
                        EggFrame:
                            name: "Legendary"
                            cost: "4 Coins"
                            
                        EggFrame:
                            name: "Mythic" 
                            cost: "5 Coins"
                                
        
        # The homepage - where the tasks are shown
        MDScreen:
            name: "home"
            MDAnchorLayout:
                anchor_x: "center"
                anchor_y: "center"
                size_hint: 0.9, 0.9
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                #spacing: dp(25)
                radius: 20
                #height: self.parent.height
                #width: root.height *0.75
                md_bg_color: app.theme_cls.primaryContainerColor
                
                MDScrollView:
                    scroll_type: ['bars', 'content']
                    bar_color: app.theme_cls.secondaryColor        
                    bar_color_inactive: app.theme_cls.secondaryColor
                    size_hint: 0.9, 0.9
                    do_scroll_x: False
                    do_scroll_y: True
                    bar_width: dp(4)
                    padding: dp(10)

                    MDBoxLayout:
                        id: home_list
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(15)
                        padding: dp(15)
                # MDLabel:
                #     text: "Tasks"
                #     halign: "center"
                #     theme_font_name: "Custom"
                #     font_name: "robotvar.ttf"
        
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

# This defines the class DBItem outside the KV so Kivy understands it
class DBItem(MDListItem, ButtonBehavior):
    text = StringProperty() # The text used to show the databases' name
    
class SubjectFrame(MDBoxLayout):
    text = StringProperty()
    
# This defines the EggFrame
class EggFrame(MDBoxLayout):
    name = StringProperty()
    cost = StringProperty()
    
class MainScreen(MDApp):
    def build(self):
        # Defines theme colours (adds a lot of lines :O )
        self.theme_cls.theme_style = "Light" # Kind of self explanatory as this just determines the theme (light vs dark mode)
        # Saves time from me writing self.theme_cls like 20 times
        theme = self.theme_cls
        
        for key, value in colourScheme.items():
            attr = key + "Color"   # appends Color to each key so that I can use the Material 3 convention. Learn more about it here: https://m3.material.io/
            if hasattr(theme, attr):
                setattr(theme, attr, value)
        
        # theme_cls.primary_hue = "500" # Controls how light or dark this is (500 is a balance between light and dark)
        root = Builder.load_string(KV)
        self.process = None # Flag for checking if DBEditor is open
        return root
    
    def openDB(self, text):
        print(f"Opening database: {text}")
        # Starts the editor in a separate process so the current window stays open
        python = sys.executable # The absolute path (independent of the users drive-tree layout) of the Python interpreter running the editor
        # Passes the name of the database (a string) as an argument
        if self.process and self.process.poll() is None:
            self.process.terminate() # 'Graceful Termination' - An algorithmic way of 'Press the red button to close me'
            try:
                self.process.wait(timeout=3) # Ensures old data is cleaned up
            except subprocess.TimeoutExpired: # If the DBEditor is being unresponsive (a fail-safe)
                self.process.kill() # 'Forceful Termination' - Kind of like how you kill an unresponsive app from Task Manager (or the Mac/Linux equivalents)
            
        self.process = subprocess.Popen([python, "fsrs_db_editor.py", text])
            
        
        
    def on_start(self):
        # Creates the database list
        databases = glob.glob("*.db") # Finds all the databases in the current directory
        for db in databases:
            item = DBItem(text=db)
            # The function on_release sends the ListItem instance as first argument, so capture db separately
            item.bind(on_release=lambda instance, db=db: self.openDB(db)) # 'lambda' is a way for a small function to be defined without a name. There is no main benefit apart from making my (long) code shorter
            self.root.ids.dblist.add_widget(item)

        for db in databases: # 
            subject_frame = SubjectFrame(text=os.path.splitext(db)[0])
            self.root.ids.home_list.add_widget(subject_frame)
    

MainScreen().run()
