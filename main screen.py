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
from kivy.properties import ListProperty, NumericProperty # Same with lists. 
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivymd.uix.list import MDListItem
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from colour_palette import colourScheme # My colour palette for the GUI
from currency_manager import * # My module for the currency system
from inventory_manager import * # My module for the inventory management system
import egg_demo # Example import of your egg logic module
from index_manager import * # My module for the index management system

# Libraries for the editor screen
import os # For accessing the databases
import glob # For searching the databases
from fsrs_db_editor import editor_main # My database editor
import subprocess # How I can open my editor in a separate window
import sys # Used to get the absolute path of the Python interpreter

# Libraries for the shop screen

# Libraries for the task screen
import sqlite3 # I will need to create another database for the daily tasks (will need to find a way to prevent it appearing in the program)
from datetime import date # Checks the age of the task
import db_helper # Helper for updating grades
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
            on_release: app.buy_egg(root.name)
            
            MDButtonIcon:
                icon: "shopping"
                
            MDButtonText:
                text: "Buy"
                #pos_hint: {"center_x": 0.5, "center_y": 0.5}
                halign: "center"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"

# Creates a frame for the tasks to be contained in
<TaskItem>:
    orientation: "horizontal"
    size_hint_y: None
    adaptive_height: True
    spacing: "10dp"
    padding: "5dp"

    MDLabel:
        text: root.text
        adaptive_height: True
        pos_hint: {"center_y": .5}
        theme_font_name: "Custom"
        font_name: "robotvar.ttf"

    MDBoxLayout:
        adaptive_size: True
        spacing: "4dp"
        pos_hint: {"center_y": .5}

        MDButton:
            style: "tonal"
            theme_bg_color: "Custom"
            md_bg_color: app.theme_cls.errorColor
            on_release: root.mark_complete(1)
            MDButtonText:
                text: "1"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
                theme_text_color: "Custom"
                text_color: app.theme_cls.onErrorColor

        MDButton:
            style: "tonal"
            theme_bg_color: "Custom"
            md_bg_color: app.theme_cls.tertiaryContainerColor
            on_release: root.mark_complete(2)
            MDButtonText:
                text: "2"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
                theme_text_color: "Custom"
                text_color: app.theme_cls.onTertiaryContainerColor

        MDButton:
            style: "tonal"
            theme_bg_color: "Custom"
            md_bg_color: app.theme_cls.secondaryContainerColor
            on_release: root.mark_complete(3)
            MDButtonText:
                text: "3"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
                theme_text_color: "Custom"
                text_color: app.theme_cls.onSecondaryContainerColor

        MDButton:
            style: "tonal"
            theme_bg_color: "Custom"
            md_bg_color: app.theme_cls.primaryContainerColor
            on_release: root.mark_complete(4)
            MDButtonText:
                text: "4"
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
                theme_text_color: "Custom"
                text_color: app.theme_cls.onPrimaryContainerColor

# How the users balanced is displayed              
<CurrencyView>:
    pos_hint: {"center_x": 0.85, "center_y": 0.975}
    halign: "center"
    theme_font_name: "Custom"
    font_name: "robotvar.ttf"

# How topics in a database are displayed     
<SubjectFrame>:
    orientation: 'vertical'
    size_hint: 1, None
    adaptive_height: True
    radius: 20
    md_bg_color: app.theme_cls.tertiaryContainerColor
    
    MDLabel:
        text: root.text
        size_hint_y: None
        height: self.texture_size[1]
        pos_hint: {"center_x": 0.5}
        padding: dp(10)
        halign: "center"
        theme_font_name: "Custom"
        font_name: "robotvar.ttf"

    MDBoxLayout:
        id: tasks_container
        orientation: "vertical"
        adaptive_height: True
        padding: dp(10)
        spacing: dp(5)
        
# The layout for each bee in the inventory (I think index may have a different layout)
<BeeInInventoryFrame>:
    orientation: 'vertical'
    size_hint_y: None
    size: "300dp", "150dp"
    padding: "16dp"
    spacing: "12dp"
    radius: 24
    md_bg_color: app.theme_cls.primaryContainerColor
    
    MDFloatLayout:
        orientation: "vertical"
        size_hint: None, None
        size: self.parent.size
        spacing: "4dp"

        # Container for the bee image (Lighter box)
        MDBoxLayout:
            size_hint: None, None
            size: "120dp", "120dp"
            pos_hint: {"center_x": 0.1, "center_y": 0.4}
            radius: 16
            md_bg_color: app.theme_cls.secondaryContainerColor
            # Add Image here later


        # The name of the bee
        MDLabel:
            text: root.name
            pos_hint: {"center_x": 0.95, "center_y": 0.65}
            #halign: "center"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"
            font_style: "Headline"
            role: "large"

        # The cost of the bee
        MDLabel:
            text: f"{root.rarity} | Count: {root.count}"
            pos_hint: {"center_x": 0.95,"center_y": 0.25}
            #halign: "center"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"
            theme_text_color: "Secondary"
            font_style: "Title"
            role: "large"
            
# The layout for each bee in the index (Index shares some similaritiies to inventory)
<BeeInIndexFrame>:
    orientation: 'vertical'
    size_hint_y: None
    size: "300dp", "150dp"
    padding: "16dp"
    spacing: "12dp"
    radius: 24
    md_bg_color: app.theme_cls.primaryContainerColor
    
    MDFloatLayout:
        orientation: "vertical"
        size_hint: None, None
        size: self.parent.size
        spacing: "4dp"

        # Container for the bee image (Lighter box)
        MDBoxLayout:
            size_hint: None, None
            size: "120dp", "120dp"
            pos_hint: {"center_x": 0.1, "center_y": 0.4}
            radius: 16
            md_bg_color: app.theme_cls.secondaryContainerColor
            # Add Image here later


        # The name of the bee
        MDLabel:
            text: root.name
            pos_hint: {"center_x": 0.95, "center_y": 0.65}
            #halign: "center"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"
            font_style: "Headline"
            role: "large"

        # The rarity of the bee and whether it was discovered
        MDLabel:
            text: f"{root.rarity} | Discovered: {root.discovered}"
            pos_hint: {"center_x": 0.95,"center_y": 0.25}
            #halign: "center"
            theme_font_name: "Custom"
            font_name: "robotvar.ttf"
            theme_text_color: "Secondary"
            font_style: "Title"
            role: "large"

# The main KV Layout

MDBoxLayout:

    # The side bar
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

    # How each screen is managed, including transitions and the reflective changes on the side bar
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
                    bar_color: app.theme_cls.secondaryColor        # The colour of the scrollbar when scrolling
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
            
            CurrencyView:
                text: f"Honeycombs: {int(app.honeycombs_balance)}"
    
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
                            cost: "200 Honeycombs"
                        
                        EggFrame:
                            name: "Rare"
                            cost: "400 Honeycombs"
                            
                        EggFrame:
                            name: "Epic"
                            cost: "800 Honeycombs"
                                       
                        EggFrame:
                            name: "Legendary"
                            cost: "1600 Honeycombs"
                            
                        EggFrame:
                            name: "Mythic" 
                            cost: "3200 Honeycombs"
                                
        
        # The homepage - where the tasks are shown
        MDScreen:
            name: "home"
            
            CurrencyView:
                text: f"Honeycombs: {int(app.honeycombs_balance)}"
            
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
                    width: root.width * 0.85
                    height: root.height * 0.85

                    MDBoxLayout:
                        id: home_list
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(15)
                        padding: dp(15)
        
        # The inventory
        MDScreen:
            name: "inventory"
            MDScrollView:
                scroll_type: ['bars', 'content']
                bar_color: app.theme_cls.secondaryColor        
                bar_color_inactive: app.theme_cls.secondaryColor
                size_hint: 0.9, 0.9
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                do_scroll_x: False
                do_scroll_y: True
                bar_width: dp(4)
                padding: dp(10)
                width: root.width * 0.85
                height: root.height * 0.85

                MDBoxLayout:
                    id: inventory_list
                    md_bg_color: app.theme_cls.primaryColor
                    radius: 20
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(15)
                    padding: dp(15)
                    
                
            MDLabel:
                text: "Inventory"
                halign: "center"
                pos_hint: {"center_y": 0.975}
                theme_font_name: "Custom"
                font_name: "robotvar.ttf"
        
        # The index         
        MDScreen:
            name: "index"
            MDScrollView:
                scroll_type: ['bars', 'content']
                bar_color: app.theme_cls.secondaryColor        
                bar_color_inactive: app.theme_cls.secondaryColor
                size_hint: 0.9, 0.9
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                do_scroll_x: False
                do_scroll_y: True
                bar_width: dp(4)
                padding: dp(10)
                width: root.width * 0.85
                height: root.height * 0.85

                MDBoxLayout:
                    id: index_list
                    md_bg_color: app.theme_cls.primaryColor
                    radius: 20
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(15)
                    padding: dp(15)
                    
                
            MDLabel:
                text: "Index"
                halign: "center"
                pos_hint: {"center_y": 0.975}
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
                
                MDScrollView:
                    scroll_type: ['bars', 'content']
                    bar_color: app.theme_cls.secondaryColor        
                    bar_color_inactive: app.theme_cls.secondaryColor
                    size_hint: 0.9, 0.9
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    do_scroll_x: False
                    do_scroll_y: True
                    bar_width: dp(4)
                    padding: dp(10)
                    width: root.width * 0.85
                    height: root.height * 0.85
                    
                    # Dark mode switch
                    MDSwitch:
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        theme_font_name: "Custom"
                        font_name: "robotvar.ttf"
                        #on_active: app.toggle_dark_mode()
        
"""


# This defines the class NavItem outside of the KV so that Kivy Understands what it is
class NavItem(MDNavigationRailItem):
    text = StringProperty() # The text underneath the icon
    icon = StringProperty() # The icon used to depict the function of a page
    screen_name = StringProperty() # The name of the screen to display

# This defines the class DBItem outside the KV so Kivy understands it
class DBItem(MDListItem, ButtonBehavior):
    text = StringProperty() # The text used to show the databases' name
    
class TaskItem(MDBoxLayout):
    text = StringProperty()
    topic_id = NumericProperty()
    db_name = StringProperty()

    def mark_complete(self, grade):
        app = MDApp.get_running_app()
        app.handle_task_completion(self, grade)
        
class CurrencyView(MDLabel):
    pass

class BeeInInventoryFrame(MDBoxLayout):
    name = StringProperty() 
    rarity = StringProperty()
    count = NumericProperty()
    
class BeeInIndexFrame(MDBoxLayout):
    name = StringProperty() 
    rarity = StringProperty()
    discovered = StringProperty() # Booleans cannot be displayed nor stored in sqlite so they would have to be converted to strings

class SubjectFrame(MDBoxLayout):
    text = StringProperty() # Display name
    db_name = StringProperty() # Actual DB filename
    tasks = ListProperty() # The task list to be displayed

    # Starts when the task_container object is created 
    def on_kv_post(self, base_widget):
        if not hasattr(self, 'ids') or not self.ids or not 'tasks_container' in self.ids:
            return
        self.ids.tasks_container.clear_widgets()
        if self.tasks and len(self.tasks) > 0:
            for task in self.tasks:
                item = TaskItem(text=f"- {task['detail']}", topic_id=task['id'], db_name=self.db_name)
                self.ids.tasks_container.add_widget(item)
        else:
            item = MDLabel(text="No tasks for today!!!", halign="center", theme_font_name="Custom", font_name="robotvar.ttf")
            self.ids.tasks_container.add_widget(item)
    
# This defines the EggFrame
class EggFrame(MDBoxLayout):
    name = StringProperty()
    cost = StringProperty()
    
class MainScreen(MDApp):
    daily_tasks_db_name = "daily_tasks.db"
    honeycombs_balance = NumericProperty(0)

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
    
    # This function creates a new table called daily_tasks.db if it does not exist and then gets the day the task was created before invoking my spaced_repetition_planner.py to get three random tasks 
    def setup_daily_tasks_db(self):
        conn = sqlite3.connect(self.daily_tasks_db_name)
        cursor = conn.cursor()
        # Recreate table to ensure schema includes topic_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_tasks (
                db_name TEXT,
                topic_id INTEGER,
                task_detail TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS refresh_log (
                last_refresh_date TEXT
            )
        ''')
        # Check if refresh_log is empty and insert a dummy date if it is, it will get overidden after
        cursor.execute("SELECT count(*) FROM refresh_log")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO refresh_log (last_refresh_date) VALUES (?)", ("1970-01-01",))
        conn.commit()
        conn.close()

    def get_daily_tasks(self):
        self.setup_daily_tasks_db()
        conn = sqlite3.connect(self.daily_tasks_db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT last_refresh_date FROM refresh_log LIMIT 1")
        last_refresh = cursor.fetchone()[0]
        today_str = date.today().isoformat()
        
        cursor.execute("SELECT count(*) FROM daily_tasks")
        task_count = cursor.fetchone()[0]

        if last_refresh != today_str or task_count == 0:
            cursor.execute("DELETE FROM daily_tasks")
            databases = glob.glob("*.db")
            excluded = [self.daily_tasks_db_name, "currency.db", "index.db", "inventory.db"]
            # Filters out the non subject related databases
            filtered_databases = []
            for db in databases:
                if db not in excluded:
                    filtered_databases.append(db)
            databases = filtered_databases

            for db_name in databases:
                tasks = spaced_repetition_recommendations(db_name)
                # tasks is now a list of rows (TopicID, TopicDetail)
                for task in tasks:
                    cursor.execute("INSERT INTO daily_tasks (db_name, topic_id, task_detail) VALUES (?, ?, ?)", (db_name, task[0], task[1]))
            
            cursor.execute("UPDATE refresh_log SET last_refresh_date = ?", (today_str,))
            conn.commit()

        cursor.execute("SELECT db_name, topic_id, task_detail FROM daily_tasks")
        tasks_by_db = {}
        for db_name, topic_id, task_detail in cursor.fetchall():
            if db_name not in tasks_by_db:
                tasks_by_db[db_name] = []
            tasks_by_db[db_name].append({'id': topic_id, 'detail': task_detail})
        
        conn.close()
        return tasks_by_db
    
    def handle_task_completion(self, task_item, grade):
        # Update the specific topic in the specific DB
        try:
            db_helper.update_grade(task_item.db_name, task_item.topic_id, grade)
        except Exception as e:
            print(f"Error updating grade: {e}")
            return

        conn = sqlite3.connect(self.daily_tasks_db_name)
        cursor = conn.cursor()

        # Delete the completed task from the daily_tasks database
        cursor.execute("DELETE FROM daily_tasks WHERE topic_id = ? AND db_name = ?", (task_item.topic_id, task_item.db_name))
        conn.commit()
        conn.close()
        
        # Update currency and UI
        update_honeycombs_after_task_completion()
        self.update_balance()
        
        # Remove the widget from the list
        if task_item.parent:
            task_item.parent.remove_widget(task_item)
            
    def buy_egg(self, egg_name):
        # Map egg names to their specific update functions from currency_manager. More secure than passing the value of the cost
        # Using a dictionary is much more efficient than using a selection chain (the dictionary search is O(1) average case while the chain is O(n) average case)
        mapping = {
            "Starter": update_honeycombs_after_starter_egg_purchase,
            "Rare": update_honeycombs_after_rare_egg_purchase,
            "Epic": update_honeycombs_after_epic_egg_purchase,
            "Legendary": update_honeycombs_after_legendary_egg_purchase,
            "Mythic": update_honeycombs_after_mythic_egg_purchase
        }
        
        # Map egg names to their corresponding Egg objects from egg_demo. Strings cannot be passed into open_egg (expects an object)
        egg_object_mapping = {
            "Starter": egg_demo.starter_egg,
            "Rare": egg_demo.rare_egg,
            "Epic": egg_demo.epic_egg,
            "Legendary": egg_demo.legendary_egg,
            "Mythic": egg_demo.mythic_egg
        }
                    
        # Invokes the method for the respective egg
        # This passes the egg name so egg_demo knows which bee to generate
        egg_to_open = egg_object_mapping[egg_name]
        print(egg_name)
        egg_demo.open_egg(egg_to_open) 
        
        
        if egg_name in mapping: # Dictionary lookup is O(1)
            mapping[egg_name]() # Calls the specific function

        self.update_balance() # Seems self explanatory but it just updates the label that shows the balance
        
        self.populate_inventory() # Updates the inventory after an egg is bought
        self.populate_index() # Updates the index after an egg is bought (slightly inefficient to do this every time an egg is opened as it may not always be the case that a bee has been discovered after opening an egg)
        
        
        
    def update_balance(self):
        self.honeycombs_balance = get_honeycombs()
        
    def populate_inventory(self):
        # Clear old widgets before repopulating (ensures no old remnants remain from the previous session)
        self.root.ids.inventory_list.clear_widgets()
        bees = get_bees_from_inventory()
        if not bees:
            self.root.ids.inventory_list.add_widget(
                MDLabel(text="You have no bees in your inventory...Get some tasks done to hatch eggs!!!", halign="center", theme_font_name="Custom", font_name="robotvar.ttf")
            )
            return
        
        for name, rarity, count in bees:
            bee_frame = BeeInInventoryFrame(name=name, rarity=rarity, count=count)
            self.root.ids.inventory_list.add_widget(bee_frame)
            
    def populate_index(self):
        # Clear old widgets before repopulating (ensures no old remnants remain from the previous session)
        self.root.ids.index_list.clear_widgets()
        bees = get_bees_from_index()
        if not bees:
            self.root.ids.inventory_list.add_widget(
                MDLabel(text="You may need to run the onboarding screen", halign="center", theme_font_name="Custom", font_name="robotvar.ttf")
            )
            return
        
        for name, rarity, discovered in bees:
            if discovered == str(True):
                display_discovered = "Yes"
            else:
                display_discovered = "No"
            bee_frame = BeeInIndexFrame(name=name, rarity=rarity, discovered=display_discovered)
            self.root.ids.index_list.add_widget(bee_frame)
        
    def on_start(self):
        self.update_balance()
        # Creates the database list for the editor
        databases = glob.glob("*.db")
        excluded = [self.daily_tasks_db_name, "currency.db", "index.db", "inventory.db"]
        # Filters out the non subject related databases       
        filtered_databases = []
        for db in databases:
            if db not in excluded:
                filtered_databases.append(db)
        databases = filtered_databases

        for db in databases:
            item = DBItem(text=db)
            # The function on_release sends the ListItem instance as first argument, so gets the db separately
            item.bind(on_release=lambda instance, db=db: self.openDB(db)) # 'lambda' is a way for a small function to be defined without a name. There is no main benefit apart from making my (long) code shorter
            self.root.ids.dblist.add_widget(item)

        # Creates the subject frames for the home screen
        tasks_by_db = self.get_daily_tasks()
        
        
        for db in databases:
            tasks = tasks_by_db.get(db, [])
            subject_frame = SubjectFrame(text=os.path.splitext(db)[0], db_name=db, tasks=tasks)
            self.root.ids.home_list.add_widget(subject_frame)
            
        # Populates the inventory when the app starts
        self.populate_inventory()
        # Populates index when app starts
        self.populate_index()
    

MainScreen().run()
