
class PlaySong:
    def __init__(self, session):
        self.session = session

    def play_song(self, name):
        print("\n===============================")
        print("{} is playing now".format(name))
        print("===============================\n")
