import os
import wave
import numpy as np
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.core.audio import SoundLoader
from pedalboard import Pedalboard, Chorus, Reverb, Distortion, Gain, Phaser, Compressor
from pedalboard.io import AudioFile

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    wav_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    # loadfile = ObjectProperty(None)
    # savefile = ObjectProperty(None)
    # wav_input = ObjectProperty(None)

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
        self.display_waveform(self.wav_path)
        self.dismiss_popup()

    def save(self, path, filename):
        if self.wav_path:
            with open(os.path.join(path, filename), 'wb') as stream:
                with open(self.wav_path, 'rb') as f:
                    stream.write(f.read())
        self.dismiss_popup()

    def display_waveform(self, file_path):
        with wave.open(file_path, 'rb') as wave_file:
            n_channels, sampwidth, framerate, n_frames, comptype, compname = wave_file.getparams()
            frames = wave_file.readframes(n_frames)
            wave_data = np.frombuffer(frames, dtype=np.int16)
            wave_data = wave_data / np.iinfo(np.int16).max  




class Editor(App):
    def build(self):
        root = Root()
        main_layout = GridLayout(cols=1)

        aabb_tlacitko = Button(text="Načíst soubor")
        aabb_tlacitko.bind(on_press=root.show_load)
        main_layout.add_widget(aabb_tlacitko)

        xxyy_tlacitko = Button(text="Uložit")
        xxyy_tlacitko.bind(on_press=root.show_save)
        main_layout.add_widget(xxyy_tlacitko)

        self.slider1 = Slider(min=0, max=1, value=1, step=0.01)
        main_layout.add_widget(Label(text="1"))
        main_layout.add_widget(self.slider1)

        self.speed_slider = Slider(min=0, max=1, value=1, step=0.01)
        main_layout.add_widget(Label(text="2"))
        main_layout.add_widget(self.speed_slider)

        board_button = Button(text="Play")
        board_button.bind(on_release=self.play_audio)
        main_layout.add_widget(board_button)

        self.root_widget = root
        return main_layout

    def play_audio(self, instance):
        if self.root_widget.wav_path:
            sound = SoundLoader.load(self.root_widget.wav_path)
            if sound:
                with AudioFile('sound') as f:
                
                    with AudioFile('output.wav', 'w', f.samplerate, f.num_channels) as o:
                    
                        while f.tell() < f.frames:
                            chunk = f.read(f.samplerate)
                            effected = board(chunk, f.samplerate, reset=False)
                            o.write(effected)                

board = Pedalboard([Compressor(threshold_db = -10, ratio= 2,attack_ms = 1,release_ms= 100), Distortion(10), Gain(100)])




Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    Editor().run()
