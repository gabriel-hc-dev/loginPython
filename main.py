from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
import os

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text and self.email.text and "@" in self.email.text and "." in self.email.text:
            if self.password.text:
                db.add_user(self.email.text, self.password.text, self.namee.text)
                self.reset()
                self.manager.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        self.manager.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            self.manager.get_screen("main").current = self.email.text
            self.reset()
            self.manager.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        self.manager.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        self.manager.current = "login"

    def on_enter(self, *args):
        user_data = db.get_user(self.current)
        if user_data != -1:
            password, name, created = user_data
            self.n.text = f"Account Name: {name}"
            self.email.text = f"Email: {self.current}"
            self.created.text = f"Created On: {created}"

class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(
        title='Invalid Login',
        content=Label(text='Invalid username or password.'),
        size_hint=(None, None), size=(400, 400)
    )
    pop.open()

def invalidForm():
    pop = Popup(
        title='Invalid Form',
        content=Label(text='Please fill in all inputs with valid information.'),
        size_hint=(None, None), size=(400, 400)
    )
    pop.open()

if os.path.exists("my.kv"):
    Builder.load_file("my.kv")
else:
    print("Error: 'my.kv' file not found!")

sm = WindowManager()
db = DataBase("users.txt")

screens = [
    LoginWindow(name="login"),
    CreateAccountWindow(name="create"),
    MainWindow(name="main")
]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()
