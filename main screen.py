from kivy.lang import Builder # Builds the KV statement
from kivymd.app import MDApp # How to actually run the code
from kivy.properties import StringProperty
from kivymd.uix.navigationrail import MDNavigationRailItem

KV = """
# Template for the Rail item so that I dont have to repeat stuff multiple times
# I just found out about it recently (feels like I just had a eureka moment!)

<NavItem>

    MDNavigationRailItemIcon:
        icon: root.icon

    MDNavigationRailItemLabel:
        text: root.text
        
MDBoxLayout:

    MDNavigationRail:
        type: "labeled"
        
        NavItem:
            icon: "text-box-edit-outline"
            text: "Editor"
        
        NavItem:
            icon: "store"
            text: "Shop"
            
        NavItem:
            icon: "home"
            text: "Tasks"
            
        NavItem:
            icon: "bag-personal"
            text: "Inventory"
        
        NavItem:
            icon: "book"
            text: "Index"
            
        NavItem:
            icon: "pencil"
            text: "Editor"
            
    MDScreen:
        md_bg_color: self.theme_cls.secondaryContainerColor
        
"""

# This defines the class NavItem outside of the KV so that Kivy Understands what it is
class NavItem(MDNavigationRailItem):
    text = StringProperty() # The text underneath the icon
    icon = StringProperty() # The icon used to depict the function of a page
    screen_name = StringProperty() # The name of the screen to display
    
class MainScreen(MDApp):
    def build(self):
        return Builder.load_string(KV)
    
MainScreen().run()
