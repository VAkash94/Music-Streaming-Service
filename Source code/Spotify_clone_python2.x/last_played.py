from currently_playing import CurrentlyPlaying


class LastPlayed:
    def __init__(self, session, username):
        self.session = session
        self.username = username
        self.key_space = "userinfo"
        self.session.execute("USE " + self.key_space)
        self.select_song_id = "SELECT last_played FROM profile WHERE username = ?"
        self.select_currently_playing = "SELECT currently_playing FROM profile WHERE username = ?"
        self.select_query = "SELECT * from songs where id = ?"
        self.update_query = "UPDATE profile SET last_played = ? where username = ?"

    def get_last_played(self):
        prepared_statement = self.session.prepare(self.select_song_id)
        rows = self.session.execute(prepared_statement, [self.username])
        song_id = rows[0].last_played
        if song_id is None:
            return None
        self.session.execute("USE application")
        prepared_statement_song = self.session.prepare(self.select_query)
        rows = self.session.execute(prepared_statement_song, [song_id])
        return list(rows)

    def update_last_played(self):
        currently_playing = CurrentlyPlaying(self.session, self.username)
        song_id = currently_playing.get_currently_playing_id()
        if song_id is not None:
            prepared_statement_update = self.session.prepare(self.update_query)
            self.session.execute(prepared_statement_update, [song_id, self.username])

