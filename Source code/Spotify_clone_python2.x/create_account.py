from add_profile import AddProfile


class CreateAccount:
    def __init__(self, session):
        self.session = session
        self.key_space = "userinfo"
        self.session.execute("USE " + self.key_space)
        self.select_query = "SELECT username from login"
        self.inset_query = "Insert into login(username, password) values(?, ?)"

    def open_Account(self):
        username = raw_input("Enter your username:")
        prepared_statement = self.session.prepare(self.select_query)
        rows = self.session.execute(prepared_statement, [])
        username_list = self.get_username(rows)
        while username in username_list:
            print("username already exists. Enter a new username")
            username = raw_input("Enter your username:")
        password = raw_input("Enter your password:")
        insert_prepared_statement = self.session.prepare(self.inset_query)
        self.session.execute(insert_prepared_statement, [username, password])
        print("Account created....")
        add_profile = AddProfile(self.session)
        add_profile.add(username)
        return username

    def get_username(self, rows):
        username_list = []
        for row in rows:
            username_list.append(row.username)
        return username_list
