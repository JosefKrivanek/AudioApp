import os
import wave
import numpy as np
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from pedalboard import Pedalboard, Compressor, Distortion, Gain, Reverb, Chorus
from pedalboard.io import AudioFile

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wav_path = None

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, instance):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self, instance):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.wav_path = os.path.join(path, filename[0])
        self.dismiss_popup()

    def save(self, path, filename):
        if self.wav_path:
            with AudioFile(self.wav_path) as f:
                board = self.create_pedalboard()
                with AudioFile(os.path.join(path, filename), 'w', f.samplerate, f.num_channels) as o:
                    while f.tell() < f.frames:
                        chunk = f.read(f.samplerate)
                        effected = board(chunk, f.samplerate, reset=False)
                        o.write(effected)
        self.dismiss_popup()

class Editor(App):
    def build(self):
        root = Root()
        main_layout = GridLayout(cols=1)

        load_button = Button(text="Načíst soubor")
        load_button.bind(on_press=root.show_load)
        main_layout.add_widget(load_button)

        save_button = Button(text="Uložit")
        save_button.bind(on_press=root.show_save)
        main_layout.add_widget(save_button)

        self.distortion_slider = Slider(min=0, max=20, value=10, step=1)
        main_layout.add_widget(Label(text="Distortion"))
        main_layout.add_widget(self.distortion_slider)

        self.gain_slider = Slider(min=0, max=40, value=20, step=1)
        main_layout.add_widget(Label(text="Gain"))
        main_layout.add_widget(self.gain_slider)

        self.reverb_slider = Slider(min=0, max=1, value=0.5, step=0.01)
        main_layout.add_widget(Label(text="Reverb"))
        main_layout.add_widget(self.reverb_slider)

        self.chorus_slider = Slider(min=0, max=5, value=1, step=0.1)
        main_layout.add_widget(Label(text="Chorus"))
        main_layout.add_widget(self.chorus_slider)

        board_button = Button(text="Play")
        board_button.bind(on_release=self.play_audio)
        main_layout.add_widget(board_button)

        self.root_widget = root
        return main_layout

    def play_audio(self, instance):
        if self.root_widget.wav_path:
            with AudioFile(self.root_widget.wav_path) as f:
                board = Pedalboard([
                        Compressor(threshold_db=-10, ratio=2, attack_ms=5, release_ms=20),
                        Distortion(self.distortion_slider.value),
                        Gain(self.gain_slider.value),
                        Reverb(room_size=self.reverb_slider.value),
                        Chorus(rate_hz=self.chorus_slider.value)
                        ])
                with AudioFile('output.wav', 'w', f.samplerate, f.num_channels) as o:
                    while f.tell() < f.frames:
                        chunk = f.read(f.samplerate)
                        effected = board(chunk, f.samplerate, reset=False)
                        o.write(effected)
            sound = SoundLoader.load('output.wav')
            if sound:
                sound.play()

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    Editor().run()
