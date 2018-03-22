

class CurrentlyPlaying:
    def __init__(self, session, username):
        self.session = session
        self.username = username
        self.key_space = "userinfo"
        self.session.execute("USE " + self.key_space)
        self.select_currently_playing = "SELECT currently_playing FROM profile WHERE username = ?"
        self.update_query = "UPDATE profile SET currently_playing = ? where username = ?"
        self.select_query = "SELECT * from songs where id = ?"

    def get_currently_playing_id(self):
        prepared_statement = self.session.prepare(self.select_currently_playing)
        rows = self.session.execute(prepared_statement, [self.username])
        song_id = rows[0].currently_playing
        return song_id

    def get_currently_playing(self):
        song_id = self.get_currently_playing_id()
        if song_id is None:
            return None
        self.session.execute("USE application")
        prepared_statement = self.session.prepare(self.select_query)
        rows = self.session.execute(prepared_statement, [song_id])
        return list(rows)

    def update_currently_playing(self, sid):
        prepared_statement = self.session.prepare(self.update_query)
        self.session.execute(prepared_statement, [sid, self.username])
