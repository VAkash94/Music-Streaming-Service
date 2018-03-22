class Playlist:
    def __init__(self, session, username):
        self.session = session
        self.username = username
        self.select_query = "SELECT playlist from userinfo.profile WHERE username = ?"
        self.update_query = "UPDATE userinfo.profile set playlist = ? where username = ?"

    def create_playlist(self):
        user_input = input("Enter playlist name\n")
        playlist = self.get_playlists()
        playlist[user_input] = []
        self.update_playlist(playlist)
        print("===============================\n")
        print("Playlist {} is created". format(user_input))
        print("===============================\n")

    def get_playlists(self):
        prepared_statement = self.session.prepare(self.select_query)
        rows = self.session.execute(prepared_statement, [self.username])
        playlists = rows[0].playlist
        return playlists

    def update_playlist(self, playlist):
        prepared_statement = self.session.prepare(self.update_query)
        self.session.execute(prepared_statement, [playlist, self.username])

    def add_song_to_playlist(self, song_id):
        playlists = self.get_playlists()
        playlist_dict = {}
        count = 1
        disply = "----Playlist----\n"
        for key in playlists:
            if key != 'default':
                playlist_dict[str(count)] = key
                description = "{}. {}".format(count, key)
                disply += description + "\n"

        print(disply)
        user_input = input("Enter playlist number to add the song\n")
        playlist_name = playlist_dict[user_input]
        playlists[playlist_name].append(song_id)
        self.update_playlist(playlists)
        return playlist_name

    def get_songs_from_playlist(self):
        playlists = self.get_playlists()
        playlist_dict = {}
        count = 1
        disply = "----Playlist----\n"
        for key in playlists:
            if key != 'default':
                playlist_dict[str(count)] = key
                description = "{}. {}".format(count, key)
                disply += description + "\n"

        print(disply)
        user_input = input("Enter playlist number \n")
        if int(user_input) > len(playlists)-1:
            raise Exception
        playlist_name = playlist_dict[user_input]
        song_id_list = playlists[playlist_name]
        return song_id_list, playlist_name

    def display_menu(self):
        user_input = input("1. Create playlist \n2. List existing playlist\nEnter the number or 'back' "
                               "to go to home\n")
        if user_input == '1':
            self.create_playlist()
        elif user_input == '2':
            pass