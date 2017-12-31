
from menu import Menu
from user import User
from user import choice as ch

print('Welcome to the records entry system\nPlease options from the following options:')

Menu.display_table_columns()

choice=True
menu=0
while choice:
    # Menu.print_selected_user()
    try:
        print("User {}".format(User.screen_name))
        menu, action = Menu.options(User,menu)
    except AttributeError:
        print("No User Selected")
        menu, action = Menu.options(menu)
    print(menu)
    if action=='U':
        User=Menu.select()
        print(User.email)
        try:
            User.screen_name
        except AttributeError:
            print("Wrong Value Entered")
            user=None
    elif action =='C':
        Menu.create()
    elif action=='S' and menu==0:
        Menu.search()
    elif action=='S' and menu==1:
        tweets = User.tw_request(input("What phrase would you like to search for? "))
        for tweet in tweets['statuses']:
            print(tweet['text'])
    elif action=='R' and menu==1:
        menu=0
    elif action=='M':
        Menu.modify()
    elif action=='D':
        Menu.delete()
    elif action=='P':
        Menu.print()
    elif action=='Q':
        choice=False
        print('Thank You')
    else:
        print("Please Try Again")
