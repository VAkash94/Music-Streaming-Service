from top_hits import TodaysTopHits
from play import PlaySong
from last_played import LastPlayed
from currently_playing import CurrentlyPlaying
from search import Search
from playlist import Playlist


class Home:
    def __init__(self, session, username):
        self.session = session
        self.username = username
        self.key_space = "application"
        self.session.execute("USE " + self.key_space)

    def display_menu(self):
        home = "-----Menu-----\n1. Today's hits \n2. Playlist \n3. Search \n4. Last played " \
               "\n5. Currently playing \n6. Close\n"
        user_input = input(home)
        while user_input != '6':
            if user_input == '1':
                self.todays_hits()
            elif user_input == '2':
                self.goto_playlist()
            elif user_input == '3':
                self.search()
            elif user_input == '4':
                self.last_played()
            elif user_input == '5':
                self.currently_playing()
            user_input = input(home)
        return

    def todays_hits(self):
        hits = TodaysTopHits(self.session)
        song_list = hits.get_todays_hits()
        disply = "---------Today's Hits-------\n"
        print(disply)
        self.display_songs(disply, song_list)

    def last_played(self):
        last_played_song = LastPlayed(self.session, self.username)
        song_details = last_played_song.get_last_played()
        if song_details is None:
            print("===============================\n")
            print("---No song has been played yet---\n")
            print("===============================\n")
            return
        sid = song_details[0].id
        name = song_details[0].name
        artist_list = song_details[0].artist
        artist = ", ".join(artist_list)
        album = song_details[0].album
        description = "----Last played-----\n1. {} by {}. Album - {}".format(name, artist, album)
        print(description)
        user_input = input("Enter song number to play or 'back' go to home\n")
        while user_input != 'back':
            if user_input != '1':
                print("Invalid option. Going back to home......\n")
                return
            play = PlaySong(self.session)
            play.play_song(name)
            self.update_profile(sid)
            print(description)
            user_input = input("Enter song number to play or 'back' go to home\n")


    def currently_playing(self):
        currently_playing_song = CurrentlyPlaying(self.session, self.username)
        song_details = currently_playing_song.get_currently_playing()
        if song_details is None:
            print("===============================\n")
            print("---No song is currently playing---\n")
            print("===============================\n")
            return
        name = song_details[0].name
        artist_list = song_details[0].artist
        artist = ", ".join(artist_list)
        album = song_details[0].album
        description = "----Currently playing-----\n1. {} by {}. Album - {}".format(name, artist, album)
        print(description)
        user_input = input("Enter 'back' go to home\n")
        while user_input != 'back':
            user_input = input("Enter 'back' go to home\n")

    def update_profile(self, song_id):
        last_played_song = LastPlayed(self.session, self.username)
        last_played_song.update_last_played()
        currently_playing_song = CurrentlyPlaying(self.session, self.username)
        currently_playing_song.update_currently_playing(song_id)

    def search(self):
        search_song = Search(self.session, self.username)
        user_input = input("Enter the search string......\n")
        song_list = search_song.get_songs(user_input)
        if len(song_list) == 0:
            user_input = input("No songs found.....\nDo you want to search again [Y/n]\n")
            while user_input == 'Y' and len(song_list) == 0:
                user_input = input("Enter the search string......\n")
                song_list = search_song.get_songs(user_input)
                if len(song_list) == 0:
                    user_input = input("No songs found.....\nDo you want to search again [Y/n]\n")

        if user_input == 'n':
            return
        description = "----Search result----\n"
        print(description)
        self.display_songs(description, song_list)

    def goto_playlist(self):
        playlist = Playlist(self.session, self.username)
        user_input = input("1. Create playlist \n2. List existing playlist\nEnter the number or 'back' "
                               "to go to home\n")
        if user_input == '1':
            playlist.create_playlist()
        elif user_input == '2':
            try:
                song_id_list, playlist_name = playlist.get_songs_from_playlist()
                disply = "--------{}--------\n".format(playlist_name)
                search = Search(self.session, self.username)
                song_list = search.get_songs_from_id(song_id_list)
                self.display_songs(disply, song_list)
            except Exception:
                print("Invalid option....\nReturning to home...\n")

    def display_songs(self, disply, song_list):
        count = 1
        song_id_list = []
        for song in song_list:
            song_id_list.append(song.id)
            name = song.name
            artist_list = song.artist
            artist = ", ".join(artist_list)
            album = song.album
            description = "{}. {} by {}. Album - {}".format(count, name, artist, album)
            print(description)
            disply += description + "\n"
            count += 1
        user_input = input("Enter song number to play, 'add song number' to add songs to playlist or 'back' go to home\n")
        while user_input != 'back':
            if 'add' in user_input:
                data = user_input.strip().split(" ")
                number = int(data[1]) - 1
                playlist = Playlist(self.session, self.username)
                playlist_name = playlist.add_song_to_playlist(song_id_list[number])
                print("===============================\n")
                print("Song {} added to {}".format(song_list[number].name, playlist_name))
                print("===============================\n")
            elif not user_input.isdigit():
                print("Invalid option. \nReturning to home......\n")
                return
            elif int(user_input) > len(song_list):
                print("Invalid option.... \nReturning to home....\n")
                return
            else:
                number = int(user_input) - 1
                play = PlaySong(self.session)
                name = song_list[number].name
                play.play_song(name)
                self.update_profile(song_id_list[number])
            print(disply)
            user_input = input("Enter song number to play, 'add song number' to add songs to playlist or 'back' "
                                   "go to home\n")