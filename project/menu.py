##Make a program that logs into the different apis from the different sites. .ie twitter, facebook, google, instagram

import save
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token
from user import User, choice


class Menu:
    # table_name=input("What table would you like to modify? ")
    # table_name = 'new_users'
    column_names=None
    @staticmethod
    def display_table_columns(show=0):
        cont = True
        while cont:
            table_name = 'new_users'
            try:
                user_table = User.load_from_db(table_name)
                Menu.column_names = user_table.view_column_names()
                if show==1:
                    print(" | ".join(Menu.column_names))
                cont = False
            except AttributeError:
                if show==1:
                    print("Table {} Does Not Exist".format(table_name))
                    print(choice("create table"))

    @classmethod
    def param_type(cls,token):
        # Menu.display_table_columns()
        print("param_type")
        try:
            search_token=int(token)
            name=Menu.column_names[0] #Change to a dictionary so I can call it by it's name
            param=search_token,name  #Return id and the fact that it is the id identifier
        except ValueError:
            email_test=token.split('@')
            if len(email_test)==2:
                name=Menu.column_names[1]
                param=token,name
            else:
                name=Menu.column_names[2]
                param=token,name
            print(name)
        # print("Exit Param Type")
        return param

    @staticmethod
    def create(email=None): ##Find a way to have it options how many table names there are....
        print("Create")
        client="Twitter"
        token_value=email
        token_name='email'
        #screen_name = input("Please enter {} Screen name: ".format(client))
        if email==None:
            token_value = input("Please enter email address: ")
        token = (token_value, token_name)
        save_details = input('Would you like to save this user? ([Y]/N): ')
        if save_details.upper() != 'N':
            new_user = User.load_from_db_by_token(token)
            print(new_user)
            try:
##USER DOES NOT EXIST, NEED TO GET IT SO SAVE NEW USER
                print("User {} already exists.".format(new_user.email.upper()))
            except AttributeError or TypeError:
                print("Attempting to create {}...".format(token))
                request=get_request_token()
                oauth=get_oauth_verifier(request)
                access_token = get_access_token(request, oauth)
                print(access_token)
                new_user = save.create_user(access_token) ##Fix to use access token
                print("Saving {}...".format(new_user))
                new_user.save_to_db()
                # print(User.load_from_db_by_token(token))
                return new_user
        else:
            print('Record not saved.')
        print("Exiting Create")

    @classmethod
    def search(cls,token=None):###MAKE IT SO CAN SEARCH USING THE PARAMATERS OR CREATE IF IT DOES NOT EXIST
        # print("Search")
        User.print_all_from_db()
        token = input("\nPlease select a record (User ID, Screen Name,  Email): ")
        search_var=cls.param_type(token)
        search_result=None
        print("search {}".format(search_var))
        print

        try:
            search_result = User.load_from_db_by_token(search_var)
            print(search_result)
            if search_var[1].lower()=='email':
                email=search_var[0]
                try:
                    # search_result=User.load_from_db_by_token(search_var)
                    print("{} Account exists".format(search_result.email))##If doesn't exist make a new one. or try again.
                except TypeError:
                    print("{} does not have and existing email record.".format(email.upper()+' '))
                    not_there=input('Would you like to create this record?')
                    if not_there.lower()=='y':
                        Menu.create(email)
                    else:
                        print("Please Select option")
            elif search_var[1].lower=='id':
                try:
                    # search_result=User.load_from_db_by_token(search_var)
                    print("{} Account exists".format(search_result.email))##If doesn't exist make a new one. or try again.
                except TypeError:
                    print("There is no existing record in the database")
        except TypeError:
            try:
                int(token)
                print("No Record Exists")
                return
            except ValueError:
                print("{} does not have and existing email record.".format(token.upper() + ' '))
                not_there = input('Would you like to create this record?')
                if not_there.lower() == 'y':
                    Menu.create(token)
                else:
                    # print("Please Select option")
                    print("No record exists.")
                    return None
            # not_there = input('Would you like to create this record?')
        #     if not_there.lower() == 'y':
        #         search_result=Menu.create(search_var[0])
        #     else:
        #         print("Please Select option")
        # elif search_var[1].lower()=='id':
        # else:
            # id=search_var[0]
            # print(User.load_from_db_by_token(search_var))
        # print("Leaving Search")
        return search_result, search_var

        # elif search_var[1].lower()== 'screen_name':
        #     screen_name=search_var[0]
        #     print(User.load_from_db_by_token(search_var))

    @classmethod
    def modify(cls,token=None):
        # token = input("Please enter email for record to modify: ").lower()
        modify_var=cls.search()[1]
        record=modify_var[0]
        print("Modify")
        # modify_var=cls.param_type(token)
        try:
            modify = input(
                '[{}]\n Is this the record you want to modify? ([Y]/N): '.format(User.load_from_db_by_token(modify_var)))
            if modify.upper() != 'N':
               print("Modifying Record")
               User.modify_record_in_db(modify_var)
            else:
                print("Nothing Changing")
        except TypeError:
            print("{} Does not have and existing record.".format(record.upper()))
        pass

    @classmethod
    def delete(cls, token=None):
        print("Delete")
        delete_var=cls.search()[1]
        record=delete_var[0]
        email=User.load_from_db_by_token(delete_var).email
        try:
            print()
            delete = input('[{}]\n Is this the record you want to delete? ([Y]/N): '.format(email))
            if delete.upper() != 'N':
                print("Deleting... {}".format(email))
                User.delete_from_db(email)
                User.print_all_from_db()
            else:
                print("Skipping Delete")
        except TypeError:
            print("{} Does not have and existing record.".format(email.upper()))

    @staticmethod
    def print():
        User.print_all_from_db()

    @classmethod
    def select(cls,token=None):
        select=cls.search()[0]
        return select



    @staticmethod
    def user_menu(user):
        print("User Menu\n"
              "[S]earch twitter for topic\n"
              "[M]odify {}'s record\n"
              "[R]eturn to previous Menu\n"
              "[Q]uit Program".format(user.screen_name))

    @staticmethod
    def app_menu():
        print('\n'
              '[U]se existng Record\n'
              '[C]reate New Record\n'
              '[S]earch Existing Record\n'
              '[M]odify Existing Record\n'
              '[D]elete Existing Record\n'
              '[P]rint All Records\n'
              '[Q]uit\n')

    @classmethod
    def options(cls,user=None,menu=0):
        if menu==0:
            cls.app_menu()
        elif menu==1:
            cls.user_menu(user)
        selection = (input('Please enter Selection: ')).upper()
        if menu==0 and selection=='U':
             menu=1
        elif menu==1 and selection=='R':
             menu=0
        return menu,selection

    # @classmethod
    # def print_selected_user(cls, menu=0):
    #     user=cls.select()
    #     try:
    #         print("User {}".format(user.screen_name))
    #         menu, action = cls.options(user, menu)
    #     except NameError or AttributeError:
    #         print("No User Selected")
    #         menu, action = Menu.options(menu)


