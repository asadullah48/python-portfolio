import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'drop': pygame.mixer.Sound('assets/drop.wav'),
            'win': pygame.mixer.Sound('assets/win.wav'),
            'draw': pygame.mixer.Sound('assets/draw.wav'),
            'invalid': pygame.mixer.Sound('assets/invalid.wav')
        }
        
    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()