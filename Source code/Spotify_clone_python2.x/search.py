
class Search:
    def __init__(self, session, username):
        self.session = session
        self.username = username
        self.select_query = "SELECT * from application.songs WHERE album = ?"
        self.select_query_using_name = "SELECT * FROM application.songs where name = ?"
        self.select_query_using_id = "SELECT * FROM application.songs where id = ?"

    def get_songs(self, search_string):
        lower_case = search_string.lower()
        search_string = search_string.capitalize()
        title = search_string.title()
        prepared_statement = self.session.prepare(self.select_query)
        prepared_statement_name = self.session.prepare(self.select_query_using_name)
        rows = self.session.execute(prepared_statement, [search_string])
        song_list = list(rows)
        rows = self.session.execute(prepared_statement, [lower_case])
        song_list = song_list + list(rows)
        rows = self.session.execute(prepared_statement, [title])
        song_list = song_list + list(rows)
        rows = self.session.execute(prepared_statement_name, [search_string])
        song_list = song_list + list(rows)
        rows = self.session.execute(prepared_statement_name, [lower_case])
        song_list = song_list + list(rows)
        rows = self.session.execute(prepared_statement_name, [title])
        song_list = song_list + list(rows)
        return song_list

    def get_songs_from_id(self, song_id_list):
        song_list = []
        prepared_statement = self.session.prepare(self.select_query_using_id)
        for song_id in song_id_list:
            rows = self.session.execute(prepared_statement, [song_id])
            rows = list(rows)
            song_list.append(rows[0])
        return song_list


