
class AddProfile:
    def __init__(self, session):
        self.session = session
        self.key_space = "userinfo"
        self.session.execute("USE " + self.key_space)
        self.inset_query = "Insert into profile(username, currently_playing, last_played, playlist) values(?, ?, ?, ?)"

    def add(self, username):
        insert_prepared_statement = self.session.prepare(self.inset_query)
        self.session.execute(insert_prepared_statement, [username, None, None, {'default': []}])
