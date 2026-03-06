# Set this to the database file you want to edit (relative to this folder or absolute path)
DB_FILE = "comp_sci.db"
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.dialog import MDDialogContentContainer
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
import db_helper_resolve as db_helper

# Default DB_FILE is optional; GUI should pass path to helper functions.
#DB_FILE = None

Window.size = (1920, 1080)



class TopicRow(ButtonBehavior, MDBoxLayout):
    col0 = StringProperty('')
    col1 = StringProperty('')
    col2 = StringProperty('')
    col3 = StringProperty('')
    col4 = StringProperty('')
    col5 = StringProperty('')
    col6 = StringProperty('')
    topic_id = NumericProperty()
    bgcolor = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', padding=(6, 6), size_hint_y=None, height='40dp')
        # create 7 labels that bind to properties via kv viewclass (see db_editor.kv)
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
        MDApp.get_running_app().open_rag_dialog_by_id(self.topic_id)


class DBEditorApp(MDApp):
    dialog = None
    db_file = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string("db_editor.kv")

    def on_start(self):
        # If DB_FILE env/arg discovery is desired, db_helper_resolve can be used directly in calls.
        self.load_topics()

    def load_topics(self):
        # Use RecycleView (id: rv) for efficient lists
        # clear any previous data
        rv = self.root.ids.rv
        rv.data = []
        try:
            rows = db_helper.get_topics(self.db_file, limit=500)
        except Exception as e:
            # show a dialog if loading failed
            self._show_error(str(e))
            return
        data = []
        for idx, r in enumerate(rows):
            bgcolor = (0.98, 0.98, 0.995, 1) if idx % 2 else (1, 1, 1, 1)
            data.append(
                {
                    'col0': str(r.get('TopicID') or ''),
                    'col1': str(r.get('MainCategory') or ''),
                    'col2': str(r.get('SubCategory') or ''),
                    'col3': str(r.get('TopicDetail') or ''),
                    'col4': str(r.get('RAG') or ''),
                    'col5': str(r.get('DateReviewed') or ''),
                    'col6': str(r.get('DateToReview') or ''),
                    'topic_id': r.get('TopicID'),
                    'bgcolor': bgcolor,
                }
            )
        rv.data = data

        # if no db_file selected yet and rows exist, remember nothing; require user to "Open DB" to pick file

    def open_rag_dialog(self, instance):
        topic_id = instance.topic_id
        if self.dialog:
            self.dialog.dismiss()

        def _do_update(rag_value):
            try:
                db_helper.update_rag(self.db_file, topic_id, rag_value)
            except Exception as e:
                self._show_error(str(e))
                return
            self.dialog.dismiss()
            self.load_topics()

        dlg = MDDialog(
            MDDialogHeadlineText(text=f"Set R/A/G for Topic {topic_id}"),
            MDDialogSupportingText(text="Choose new RAG value:"),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=lambda *a: dlg.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="R"),
                    style="text",
                    on_release=lambda *a: _do_update("R"),
                ),
                MDButton(
                    MDButtonText(text="A"),
                    style="text",
                    on_release=lambda *a: _do_update("A"),
                ),
                MDButton(
                    MDButtonText(text="G"),
                    style="text",
                    on_release=lambda *a: _do_update("G"),
                ),
                spacing="8dp",
            ),
            size_hint=(0.9, None),
        )
        self.dialog = dlg
        dlg.open()

    def open_rag_dialog_by_id(self, topic_id):
        # Helper to open dialog when we only have an ID (used by RecycleView rows)
        if self.dialog:
            self.dialog.dismiss()

        def _do_update(rag_value):
            try:
                db_helper.update_rag(self.db_file, topic_id, rag_value)
            except Exception as e:
                self._show_error(str(e))
                return
            self.dialog.dismiss()
            self.load_topics()

        dlg = MDDialog(
            MDDialogHeadlineText(text=f"Set R, A or G for Topic {topic_id}"),
            MDDialogSupportingText(text="Choose new RAG value:"),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=lambda *a: dlg.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="R"),
                    style="text",
                    on_release=lambda *a: _do_update("R"),
                ),
                MDButton(
                    MDButtonText(text="A"),
                    style="text",
                    on_release=lambda *a: _do_update("A"),
                ),
                MDButton(
                    MDButtonText(text="G"),
                    style="text",
                    on_release=lambda *a: _do_update("G"),
                ),
                spacing="8dp",
            ),
            size_hint=(0.9, None),
        )
        self.dialog = dlg
        dlg.open()

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

    # File picker dialog
    def open_file_picker(self):
        # Create a file chooser with a usable height so it is visible inside the dialog
        self._filechooser = FileChooserListView(filters=['*.db'], path='.', size_hint=(1, 0.65))

        def _pick(*args):
            selection = self._filechooser.selection
            if selection:
                self.db_file = selection[0]
                dlg.dismiss()
                self.load_topics()

        content = MDDialogContentContainer(self._filechooser)

        dlg = MDDialog(
            MDDialogHeadlineText(text="Open database"),
            MDDialogSupportingText(text="Select a .db file to load"),
            content,
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Cancel"), style="text", on_release=lambda *a: dlg.dismiss()),
                MDButton(MDButtonText(text="Open"), style="text", on_release=_pick),
            ),
            size_hint=(0.9, None),
        )
        dlg.open()


if __name__ == "__main__":
    DBEditorApp().run()
