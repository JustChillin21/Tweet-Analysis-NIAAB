# from database import connection_pool
import json
import oauth2
import psycopg2 as pg
from tabulate import tabulate

from database import CursorFromConnectionFromPool, Database
from twitter_utils import consumer

##What happens if we stop after the pin. right now it errors our...
cont = False


def choice(question):
    temp = input("Do you want to {}?".format(question)).lower()
    if temp == 'y':
        test = question.split(' ')
        try:
            test.remove('a')
        except ValueError:
            pass
        if len(test) > 2:
            option = (test[0][:-1] + "ing " + ' '.join(test[-2:])).title()
        else:
            option = (test[0][:-1] + "ing " + ' '.join(test[-1:])).title()
    else:
        option = ("Please try again.")
    return option


while cont == False:
    try:
        # Database.initialize(minconn=1, maxconn=10, user='y2venom', password='jun34u2I',
        #                     database=input("Database name?"),
        #                     host='SpiderVault')
        Database.initialize(minconn=1, maxconn=10, user='y2venom', password='jun34u2I',
                            database="learning",
                            host='SpiderVault')
        cont = True
        print("Loading...")
    except pg.Error:
        print("Database Connection Error.")
        print(choice("create a new database"))
        # self.create_database()


class User:
    def __init__(self, email, screen_name, first_name=None, middle_name=None, last_name=None, oauth_token=None,
                 oauth_token_secret=None, id=None):
        self.email = email
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        # self.table_name=table_name
        self.id = id

    def __repr__(self):
        if self.id:
            return "<User[{}] {}: {}>".format(self.id, self.screen_name, self.email)
        else:
            return "<{}: {}>".format(self.screen_name, self.email)

    def save_to_db(self):

        with CursorFromConnectionFromPool() as cursor:
            query = """INSERT INTO {} (email, screen_name, first_name, middle_name, last_name,  oauth_token, oauth_token_secret) VALUES (%s, %s, %s, %s, %s, %s, %s)""".format(
                self.table_name)
            values = (self.email, self.screen_name, self.first_name, self.middle_name, self.last_name, self.oauth_token,
                      self.oauth_token_secret)
            cursor.execute(query, values)
            print("Record Saved: {}".format(self.email))

    @classmethod
    def delete_from_db(cls, email):
        with CursorFromConnectionFromPool() as cursor:
            query = """
            DELETE FROM {} WHERE email=%s
            """.format(cls.table_name)
            values = (email,)
            cursor.execute(query, values)
            print("Record Deleted: {}".format(email))

    @classmethod
    def view_column_names(cls, table_name='new_users'):  ##Returns Column Headers from table
        cls.table_name = table_name
        with CursorFromConnectionFromPool() as cursor:
            query = """
            SELECT 
            * 
            FROM 
            {}
            LIMIT
            0
            """.format(cls.table_name)
            cursor.execute(query, )
            ###
            col_names = []
            for header in cursor.description:
                col_names.append(header[0])
        return col_names

    @classmethod  # Modify a record in the Database
    def modify_record_in_db(cls, token):

        record_to_modify = cls.load_from_db_by_token(token)
        token_name = token[1]
        token_value = token[0]
        record_type = None
        print('\nModify\n(F)irst Name: {}\n(L)ast Name: {}\n(E)mail Address: {}\n'.format(record_to_modify.first_name,
                                                                                          record_to_modify.last_name,
                                                                                          record_to_modify.email))
        choice = input('What would you like to modify?').lower()
        if choice == 'f':
            newvalue = input('Please enter new First Name for {}: '.format(record_to_modify.first_name))
            record_type = "First Name"
            with CursorFromConnectionFromPool() as cursor:
                # cursor.execute('UPDATE users SET first_name=%s WHERE email=%s', (newvalue, email,))
                query = """
                UPDATE {} SET first_name=%s WHERE {}=%s
                """.format(cls.table_name, token_name)
                values = (newvalue, token_value)
                cursor.execute(query, values, )
        elif choice == 'l':
            newvalue = input('Please enter new Last Name for {}: '.format(record_to_modify.last_name))
            record_type = "Last Name"
            with CursorFromConnectionFromPool() as cursor:
                # cursor.execute('UPDATE users SET last_name=%s WHERE email=%s', (newvalue, email,))
                query = """
                UPDATE {} SET last_name=%s WHERE {}=%s
                """.format(cls.table_name, token_name)
                values = (newvalue, token_value)
                cursor.execute(query, values)
        elif choice == 'e':
            newvalue = input('Please enter new Email Address for {}: '.format(record_to_modify.email))
            record_type = "Email Address"
            with CursorFromConnectionFromPool() as cursor:
                # cursor.execute('UPDATE users SET email=%s WHERE email=%s', (newvalue, email,))
                query = """
                UPDATE {} SET email=%s WHERE {} = %s
                """.format(cls.table_name, token_name)
                values = (newvalue, token_value)
                cursor.execute(query, values)
        else:  # choice=='q':
            # check is column exists, if it doesn't create column, if it does, display existing key and ask to modify
            pass

        if record_type:
            print('{} has been updated for {}'.format(record_type, record_to_modify.screen_name))
        else:
            print("Nothing to Change")

    @classmethod
    def print_all_from_db(cls):
        cls.view_column_names()
        with CursorFromConnectionFromPool() as cursor:
            query = """
            SELECT * FROM {} ORDER BY id
            """.format(cls.table_name)
            cursor.execute(query)  # , values)
            rows = cursor.fetchall()
            print(tabulate(rows, headers=cls.view_column_names()))

            return rows

    # @classmethod
    # def load_from_db_by_email(cls, email):
    #     with CursorFromConnectionFromPool() as cursor:
    #         query = """
    #         SELECT
    #           *
    #         FROM
    #           {}
    #         WHERE
    #           email = %s
    #         """.format(cls.table_name)
    #         values=(email,)
    #         #cursor.execute('SELECT * FROM users WHERE email=%s',(email,))
    #         cursor.execute(query, values)
    #         user_data = cursor.fetchone()
    #         try:
    #             return cls(email=user_data[1], screen_name=user_data[2], first_name=user_data[3], middle_name=user_data[4], last_name=user_data[5],
    #                    oauth_token=user_data[6],oauth_token_secret=user_data[7],id=user_data[0])
    #         except TypeError:
    #             return None

    @classmethod
    def load_from_db_by_token(cls, token, table_name='new_user'):
        print("Load from DB by Token")
        token_name = token[1]
        token_value = token[0]
        with CursorFromConnectionFromPool() as cursor:
            query = """
            SELECT 
              * 
            FROM 
              {} 
            WHERE 
              {} = %s
            """.format(cls.table_name, token_name)
            values = (token_value,)
            cursor.execute(query, values)
            user_data = cursor.fetchone()
            try:
                return cls(email=user_data[1], screen_name=user_data[2], first_name=user_data[3],
                           middle_name=user_data[4], last_name=user_data[5],
                           oauth_token=user_data[6], oauth_token_secret=user_data[7], id=user_data[0])
            except AttributeError or TypeError:
                # add option to create user if not exist.
                print("User does not exist")
                save_option = input("Would you like to save this user [{}]?".format(token_value))
                ###OPTION TO SAVE FILE###
        print("Leaving Load from DB by Token")

    @classmethod
    def load_from_db(cls, table_name='new_user'):
        cls.table_name = table_name
        try:
            with CursorFromConnectionFromPool() as cursor:
                query = """
                SELECT 
                  * 
                FROM 
                  {} 
                """.format(cls.table_name)
                values = ()
                cursor.execute(query, values)
                user_data = cursor.fetchone()
                if user_data:
                    return cls(email=user_data[1], screen_name=user_data[2], first_name=user_data[3],
                               middle_name=user_data[4], last_name=user_data[5],
                               oauth_token=user_data[6], oauth_token_secret=user_data[7], id=user_data[0])
        except pg.Error:
            print("Table Does Not Exist")

    def tw_request(self, topic, uri='https://api.twitter.com/1.1/search/tweets.json?q={}+filter:images',verb='GET'):

        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        response, content = authorized_client.request(
            uri.format(topic), verb)

        if response.status != 200:
            print("An error occurred when searching!")
        tweets = json.loads(content.decode('utf-8'))
        return tweets
