

class TodaysTopHits:
    def __init__(self, session):
        self.session = session
        self.key_space = "application"
        self.session.execute("USE " + self.key_space)
        self.select_query = "SELECT * from todays_hits"

    def get_todays_hits(self):
        prepared_statement = self.session.prepare(self.select_query)
        rows = self.session.execute(prepared_statement, [])
        rows = list(rows)
        return rows
