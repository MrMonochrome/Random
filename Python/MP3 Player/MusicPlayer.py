import vlc
from MusicLibrary import MusicLibrary
from Song import Song


class MusicPlayer:
    current_song: Song

    def __init__(self, library: MusicLibrary):
        self.player = None
        self.library = library
        self.play_list = []
        self.current_song = None
        self.play_list_length = 10

    def start(self):
        self.get_next_song()
        self.player = vlc.MediaPlayer(self.current_song.full_path)
        self.player.play()

    def get_next_song(self):
        if not self.play_list:
            self.play_list = self.library.get_random_playlist(self.play_list_length)
        self.current_song = self.play_list.pop(0)

    def next(self):
        self.stop()
        self.start()

    def stop(self):
        self.player.stop()

