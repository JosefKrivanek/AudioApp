from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from pedalboard import Pedalboard, Chorus, Reverb, Distortion, Gain, Phaser, Compressor
from pedalboard.io import AudioFile
import os



class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    wav_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    wav_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.wav_input.wav = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.wav_input.wav)

        self.dismiss_popup()

class Editor(App):
    def build(self):
        main_layout = GridLayout (cols = 1)

        aabb_tlacitko = Button(wav="Načíst soubor")
        aabb_tlacitko.bind(on_press=self.on_aabb_pressed)
        main_layout.add_widget(aabb_tlacitko)

        xxyy_tlacitko = Button(wav="Uložit")
        xxyy_tlacitko.bind(on_press=self.on_xxyy_pressed)
        main_layout.add_widget(xxyy_tlacitko)

        self.slider1 = Slider(min=0, max=1, value=1, step=0.01)
        main_layout.add_widget(Label(wav="1"))
        main_layout.add_widget(self.slider1)

        self.speed_slider = Slider(min=0, max=1, value=1, step=0.01)
        main_layout.add_widget(Label(wav="2"))
        main_layout.add_widget(self.speed_slider)

        return main_layout

    def on_aabb_pressed(self, instance):
        root = Root()
        root.show_load()


    def on_xxyy_pressed(self, instance):
        root = Root()
        root.show_save()
        pass

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    Editor().run()
