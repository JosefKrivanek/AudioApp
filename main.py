import os
import wave
import numpy as np
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from pedalboard import Pedalboard, Compressor, Distortion, Gain, Reverb, Chorus
from pedalboard.io import AudioFile
from kivy.lang import Builder

# Load the KV file
Builder.load_file('style.kv')

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    wav_input = ObjectProperty(None)
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

    def create_pedalboard(self):
        return Pedalboard([
            Compressor(threshold_db=-10, ratio=2, attack_ms=5, release_ms=20),
            Distortion(self.ids.distortion_slider.value),
            Gain(self.ids.gain_slider.value),
            Reverb(room_size=self.ids.reverb_slider.value),
            Chorus(rate_hz=self.ids.chorus_slider.value)
        ])

class Editor(App):
    def build(self):
        root = Root()
        self.root_widget = root  # Assign root to self.root_widget
        self.sound = None  # Initialize sound variable
        return root

    def play_audio(self, instance):
        if self.root_widget.wav_path:
            if self.sound:
                self.sound.stop()  # Stop any currently playing sound
            with AudioFile(self.root_widget.wav_path) as f:
                board = self.root_widget.create_pedalboard()
                with AudioFile('output.wav', 'w', f.samplerate, f.num_channels) as o:
                    while f.tell() < f.frames:
                        chunk = f.read(f.samplerate)
                        effected = board(chunk, f.samplerate, reset=False)
                        o.write(effected)
            self.sound = SoundLoader.load('output.wav')
            if self.sound:
                self.sound.play()

    def stop_audio(self, instance):
        if self.sound:
            self.sound.stop()

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    Editor().run()
