from kivy.lang import Builder # This applies the formatting defined on KV
from kivy.properties import NumericProperty, StringProperty # Kivy has an easier way to set th datatypes of properties than stock python
from kivy.properties import ListProperty # Same with lists. 
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
#from kivy.uix.filechooser import FileChooserListView
# from kivymd.uix.dialog import MDDialogContentContainer
from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
import db_helper # Has a function that allows the data to be extracted from the SQL database without the need to converge SQL and Python in the editor
from pathlib import Path
KV = """
MDScreen:
    md_bg_color: 1,1,1,1
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            size_hint_y: None
            height: "64dp"
            padding: "6dp"
            spacing: "8dp"
            MDLabel:
                text: "DB Editor"
                halign: "left"
            BoxLayout:
                orientation: "horizontal"
                size_hint_x: None
                width: "520dp"
                spacing: "8dp"
                MDLabel:
                    text: "Key:"
                    size_hint_x: None
                    width: "36dp"
                    halign: "left"
                    valign: "middle"
                BoxLayout:
                    orientation: "horizontal"
                    size_hint_x: None
                    width: "92dp"
                    spacing: "4dp"
                    MDLabel:
                        text: "1=Again"
                        size_hint_x: None
                        width: "60dp"
                        halign: "left"
                        valign: "middle"
                    Image:
                        source: app._grade_img_path(1)
                        size_hint_x: None
                        width: dp(20)
                        size_hint_y: None
                        height: dp(20)
                        pos_hint: {'center_y': .5}
                BoxLayout:
                    orientation: "horizontal"
                    size_hint_x: None
                    width: "92dp"
                    spacing: "4dp"
                    MDLabel:
                        text: "2=Hard"
                        size_hint_x: None
                        width: "60dp"
                        halign: "left"
                        valign: "middle"
                    Image:
                        source: app._grade_img_path(2)
                        size_hint_x: None
                        width: dp(20)
                        size_hint_y: None
                        height: dp(20)
                        pos_hint: {'center_y': .5}
                BoxLayout:
                    orientation: "horizontal"
                    size_hint_x: None
                    width: "92dp"
                    spacing: "4dp"
                    MDLabel:
                        text: "3=Good"
                        size_hint_x: None
                        width: "60dp"
                        halign: "left"
                        valign: "middle"
                    Image:
                        source: app._grade_img_path(3)
                        size_hint_x: None
                        width: dp(20)
                        size_hint_y: None
                        height: dp(20)
                        pos_hint: {'center_y': .5}
                BoxLayout:
                    orientation: "horizontal"
                    size_hint_x: None
                    width: "92dp"
                    spacing: "4dp"
                    MDLabel:
                        text: "4=Easy"
                        size_hint_x: None
                        width: "60dp"
                        halign: "left"
                        valign: "middle"
                    Image:
                        source: app._grade_img_path(4)
                        size_hint_x: None
                        width: dp(20)
                        size_hint_y: None
                        height: dp(20)
                        pos_hint: {'center_y': .5}
        BoxLayout:
            size_hint_y: None
            height: '36dp'
            spacing: '4dp'
            padding: 0
            canvas.before:
                Color:
                    rgba: .95, .95, .95, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            MDLabel:
                text: "ID"
                size_hint_x: 0.04
                halign: 'left'
            MDLabel:
                text: "MainCategory"
                size_hint_x: 0.12
                halign: 'left'
            MDLabel:
                text: "SubCategory"
                size_hint_x: 0.12
                halign: 'left'
            MDLabel:
                text: "TopicDetail"
                size_hint_x: 0.35
                halign: 'left'
            MDLabel:
                text: "Grade"
                size_hint_x: 0.06
                halign: 'left'
            MDLabel:
                text: "Reviewed"
                size_hint_x: 0.09
                halign: 'left'
            MDLabel:
                text: "To Review"
                size_hint_x: 0.09
                halign: 'left'
        RecycleView:
            id: rv
            viewclass: 'TopicRow'
            RecycleBoxLayout:
                default_size: None, dp(40)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: "56dp"
            padding: "8dp"
            Button:
                text: "Refresh"
                on_release: app.load_topics()

<TopicRow>:
    canvas.before:
        Color:
            rgba: root.bgcolor if hasattr(root, 'bgcolor') else (1,1,1,1)
        Rectangle:
            pos: self.pos
            size: self.size
    MDLabel:
        text: root.col0
        size_hint_x: 0.04
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        font_size: '14sp'
        text_size: self.size
        valign: 'middle'
    MDLabel:
        text: root.col1
        size_hint_x: 0.12
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        font_size: '14sp'
        text_size: self.size
        valign: 'middle'
    MDLabel:
        text: root.col2
        size_hint_x: 0.12
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        font_size: '14sp'
        text_size: self.size
        valign: 'middle'
    MDLabel:
        text: root.col3
        size_hint_x: 0.35
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        font_size: '14sp'
        text_size: self.size
        valign: 'middle'
    BoxLayout:
        size_hint_x: 0.06
        size_hint_y: 1
        padding: 0
        Image:
            source: root.col4_src
            size_hint: None, None
            size: dp(24), dp(24)
            pos_hint: {'center_x': .5, 'center_y': .5}
    MDLabel:
        text: root.col7
        size_hint_x: 0.09
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        font_size: '14sp'
        text_size: self.size
        valign: 'middle'
    MDLabel:
        text: root.col8
        size_hint_x: 0.09
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        font_size: '14sp'
        text_size: self.size
        valign: 'middle'
"""

def editor_main(database:str):
    Window.size = (1280,720)
    class TopicRow(ButtonBehavior, MDBoxLayout): # This defines 9 blank columns (which are attributes of class TopicRow) which will be later added into the GUI. The titles will be added later via fsrs_db_editor.kv
        col0 = StringProperty('')
        col1 = StringProperty('')
        col2 = StringProperty('')
        col3 = StringProperty('')
        col4 = StringProperty('')
        col4_src = StringProperty('')
        #col5 = StringProperty('')
        #col6 = StringProperty('')
        col7 =  StringProperty('')
        col8 = StringProperty('')
        topic_id = NumericProperty()
        bgcolor = ListProperty([1, 1, 0, 1])
        
        def __init__(self, **kwargs):
            super().__init__(orientation='horizontal', padding=(6, 6), size_hint_y=None, height='40dp')
            with self.canvas.before:
                self._bg_color = Color(*self.bgcolor)
                self._bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_rect, size=self._update_rect, bgcolor=self._on_bg_change)
            
        def _on_bg_change(self, instance, value):
            try:
                self._bg_color.rgba = value
            except Exception:
                pass    
        
        def _update_rect(self, *args):
            try:
                self._bg_rect.pos = self.pos
                self._bg_rect.size = self.size
            except Exception:
                pass
        
        def on_release(self):
            MDApp.get_running_app().open_grade_dialog_by_id(self.topic_id)
    
    class DBEditorApp(MDApp):
        dialog = None
        db_file = database # Referred to using self.db_file unless inheritance is used (not necessary here)

        def build(self):
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Blue"
            return Builder.load_string(KV)

        def on_start(self):
            # This procedure is bound when the program starts up
            self.load_topics()

        # This loads the topics into a list of dictionaries before drawing it on the canvas (aka showing it on the GUI)
        def load_topics(self):
            rv = self.root.ids.rv
            rv.data = []
            try:
                # This is why I did not get rid of db_helper, otherwise it would be a lot uglier mixing SQL and Python in this section of code (however, I do use it in other sections as it seems appropriate)
                rows = db_helper.get_topics(self.db_file, limit=500)
            except Exception as e:
                # Shows an error dialog if an error is caught such as an invalid format of a database
                self._show_error(str(e))
                return
            data = []
            # idx is simply the index in the list 'rows' and r is just the individual row
            for idx, r in enumerate(rows):
                bgcolor = (0.98, 0.98, 0.995, 1) if idx % 2 else (1, 1, 1, 1)
                grade = r.get('Grade')
                data.append(
                    {
                        'col0': str(r.get('TopicID') or ''),
                        'col1': str(r.get('MainCategory') or ''),
                        'col2': str(r.get('SubCategory') or ''),
                        'col3': str(r.get('TopicDetail') or ''),
                        'col4': str(grade or ''),
                        'col4_src': self._grade_img_path(grade),
                        #'col5': str(r.get('Difficulty') or ''),
                        #'col6': str(r.get('Stability') or ''),
                        'col7': str(r.get('DateReviewed') or ''),
                        'col8': str(r.get('DateToReview') or ''),
                        'topic_id': r.get('TopicID'),
                        'bgcolor': bgcolor,
                    }
                )
            rv.data = data        
        
        def _grade_img_path(self, grade):
            base = Path("assets") / "for_code/images"
            try:
                g = int(grade)
            except Exception:
                g = None
            mapping = {
                1: str(base / "again_128.png"),
                2: str(base / "hard_128.png"),
                3: str(base / "good_128.png"),
                4: str(base / "easy_128.png"),
                None: str(base / "grade_empty.png"), # hopefully it falls back to a blank image
            }
            return mapping.get(g, mapping[None])
            #return mapping.get(g)
            
        def open_grade_dialog(self, instance):
            topic_id = instance.topic_id
            if self.dialog:
                self.dialog.dismiss()

            def _do_update(grade):
                try:
                    db_helper.update_grade(self.db_file, topic_id, grade)
                except Exception as e:
                    self._show_error(str(e))
                    return
                self.dialog.dismiss()
                self.load_topics()

            # What dlg does is that it opens a KivyMD dialog (notice there is no -ue) that prompts the user to update the grade for the topic
            dlg = MDDialog(
                MDDialogHeadlineText(text=f"Set Grades 1-4, 1 being hardest and 4 being easiest for Topic {topic_id}"),
                MDDialogSupportingText(text="Choose new grade:"),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=lambda *a: dlg.dismiss(),
                    ),
                    MDButton(
                        MDButtonText(text="1"),
                        style="text",
                        on_release=lambda *a: _do_update(1),
                    ),
                    MDButton(
                        MDButtonText(text="2"),
                        style="text",
                        on_release=lambda *a: _do_update(2),
                    ),
                    MDButton(
                        MDButtonText(text="3"),
                        style="text",
                        on_release=lambda *a: _do_update(3),
                    ),
                    MDButton(
                        MDButtonText(text="4"),
                        style="text",
                        on_release=lambda *a: _do_update(4),
                    ),
                    spacing="8dp",
                ),
                size_hint=(0.9, None),
            )
            self.dialog = dlg
            dlg.open()
        
        def open_grade_dialog_by_id(self, topic_id):
            # Helper to open dialog when an ID is only used (used by RecycleView rows)
            if self.dialog:
                self.dialog.dismiss()

            def _do_update(grade):
                try:
                    db_helper.update_grade(self.db_file, topic_id, grade)
                except Exception as e:
                    self._show_error(str(e))
                    return
                self.dialog.dismiss()
                self.load_topics()

            dlg = MDDialog(
                MDDialogHeadlineText(text=f"Set Grades 1-4, 1 being hardest and 4 being easiest for Topic {topic_id}"),
                MDDialogSupportingText(text="Choose new grade:"),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=lambda *a: dlg.dismiss(),
                    ),
                    MDButton(
                        MDButtonText(text="1"),
                        style="text",
                        on_release=lambda *a: _do_update(1),
                    ),
                    MDButton(
                        MDButtonText(text="2"),
                        style="text",
                        on_release=lambda *a: _do_update(2),
                    ),
                    MDButton(
                        MDButtonText(text="3"),
                        style="text",
                        on_release=lambda *a: _do_update(3),
                    ),
                    MDButton(
                        MDButtonText(text="4"),
                        style="text",
                        on_release=lambda *a: _do_update(4),
                    ),
                    spacing="8dp",
                ),
                size_hint=(0.9, None),
            )
            self.dialog = dlg
            dlg.open()    
        # Updates dlg if there are errors and shows the user the error   
        def _show_error(self, message: str):
            dlg = MDDialog(
                MDDialogHeadlineText(text="Error"),
                MDDialogSupportingText(text=message),
                MDDialogButtonContainer(
                    MDButton(MDButtonText(text="OK"), style="text", on_release=lambda *a: dlg.dismiss()),
                ),
                size_hint=(0.9, None),
            )
            dlg.open()
        
    if __name__ == "__main__":
        DBEditorApp().run()

editor_main("further_maths_for_me.db")