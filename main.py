import os
import json
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.storage.jsonstore import JsonStore

class JarvisAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        # Local JSON database storage for settings & memory
        self.store = JsonStore('jarvis_config.json')
        if not self.store.exists('settings'):
            self.store.put('settings', name='J.A.R.V.I.S.', code='code 10', key='')
            
        settings = self.store.get('settings')
        self.assistant_name = settings['name']
        self.security_code = settings['code']
        self.api_key = settings['key']

        # Header Title
        self.add_widget(Label(text=f"[b]{self.assistant_name} Core Matrix[/b]", markup=True, font_size='24sp', size_hint_y=None, height=40))
        
        # Configuration Inputs
        config_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        self.name_input = TextInput(text=self.assistant_name, hint_text="Name", multiline=False)
        self.code_input = TextInput(text=self.security_code, hint_text="Override Code", multiline=False)
        config_box.add_widget(self.name_input)
        config_box.add_widget(self.code_input)
        self.add_widget(config_box)

        self.key_input = TextInput(text=self.api_key, hint_text="Gemini API Key", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.key_input)

        save_btn = Button(text="Sync Core Configurations", size_hint_y=None, height=45, background_color=(0, 0.7, 0.9, 1))
        save_btn.bind(on_press=self.save_configurations)
        self.add_widget(save_btn)

        # Output Terminal Screen
        self.scroll = ScrollView()
        self.console_output = Label(text="Systems fully operational. Awaiting command parameters, sir...\n", text_size=(None, None), halign='left', valign='top', markup=True)
        self.scroll.add_widget(self.console_output)
        self.add_widget(self.scroll)

        # Chat Text Input Interaction
        chat_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        self.msg_input = TextInput(hint_text="Interface command terminal...", multiline=False)
        send_btn = Button(text="Send", size_hint_x=None, width=80)
        send_btn.bind(on_press=self.process_text_chat)
        chat_box.add_widget(self.msg_input)
        chat_box.add_widget(send_btn)
        self.add_widget(chat_box)

    def save_configurations(self, instance):
        self.assistant_name = self.name_input.text.strip()
        self.security_code = self.code_input.text.strip()
        self.api_key = self.key_input.text.strip()
        self.store.put('settings', name=self.assistant_name, code=self.security_code, key=self.api_key)
        self.log_to_terminal(f"[System] Settings updated. Identity reassigned to: {self.assistant_name}")

    def log_to_terminal(self, text):
        self.console_output.text += text + "\n"

    def process_text_chat(self, instance):
        user_text = self.msg_input.text.strip()
        if not user_text:
            return
        self.msg_input.text = ""
        self.log_to_terminal(f"[b]You:[/b] {user_text}")
        
        # Intercept custom system passcode words
        if user_text.lower() == self.security_code.lower():
            self.log_to_terminal(f"[b]{self.assistant_name}:[/b] Security override code detected. Purging mainframe lock status, master.")
            return
            
        # Standard brain computation route
        if not self.api_key:
            self.log_to_terminal(f"[b]{self.assistant_name}:[/b] Warning sir, no API matrix signature found. Paste your key above.")
            return
            
        self.log_to_terminal(f"[{self.assistant_name}] Processing tracking vectors...")
        # Gemini query execution would resolve here in final compilation runtime

class JarvisNativeApp(App):
    def build(self):
        return JarvisAppLayout()

if __name__ == '__main__':
    JarvisNativeApp().run()
