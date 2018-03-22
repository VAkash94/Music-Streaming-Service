import sys
from application_exception import CreateAccountException
from cassandra.cluster import Cluster
from create_account import CreateAccount
from home import Home


class Signin:
    def __init__(self):
        self.key_space = "userinfo"
        self.select_query = "SELECT username, password from login where username = ?"
        self.cluster = Cluster()
        self.session = self.cluster.connect()
        self.session.execute("USE " + self.key_space)
        print("Application started...")

    def authenticate(self):
        login = raw_input("Do you want login using existing account? [Y/n] \n")
        username = ""
        try:
            if login == 'n':
                raise CreateAccountException
            username = raw_input("Enter your username:")
            password = raw_input("Enter your password:")
            prepared_statement = self.session.prepare(self.select_query)
            rows = self.session.execute(prepared_statement, [username])
            rows = list(rows)
            if len(rows) > 0:
                pswd = rows[0].password
                while pswd != password:
                    password = raw_input("Incorrect password. Enter your password:")
            else:
                username_list = self.get_username(rows)
                while username not in username_list:
                    print("----Username not found----")
                    retry = raw_input("Do do wish to retry? [Y/n] \n")
                    if retry == 'Y':
                        username = raw_input("Enter your username:")
                        password = raw_input("Enter your password:")
                        rows = self.session.execute(prepared_statement, [username])
                        rows = list(rows)
                        if len(rows) > 0:
                            pswd = rows[0].password
                        username_list = self.get_username(rows)
                    else:
                        raise CreateAccountException
                while pswd != password:
                    password = raw_input("Incorrect password. Enter your password:")

        except CreateAccountException:
            create = raw_input("Do you  want to create new account? [Y/n]\n")
            if create == 'Y':
                new_account = CreateAccount(self.session)
                username = new_account.open_Account()
            else:
                print("Closing application...")
                sys.exit(1)

        print("Login successful....")

        home = Home(self.session, username)
        home.display_menu()
        print ("Closing application....")
        home.update_profile(None)

    def get_username(self, rows):
        username_list = []
        for row in rows:
            username_list.append(row.username)
        return username_list

if __name__ == '__main__':
    signin = Signin()
    signin.authenticate()
