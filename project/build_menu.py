#Create Menu to add, modify, search, print, delete players on the team
#Add Menu to Add, modify, delete columns for database
#from build_table import build_table
#from database import Database
import menu_options as mo

class menu_option:
    def __init__(self,*args):
        self.key=[]
        self.title=[]


selections=(mo.c_table,mo.s_table,mo.d_table,mo.a_column,mo.d_column,mo.m_column,mo.f_column,mo.cn_column,
            mo.ct_column,mo.cc_column,mo.ck_column,mo.cm_column)
menu=menu_option()
for item in selections:
    #print(item[0], item[1])
    menu.key.append((item[0],item[1]))
#print(menu.key)

for item in menu.key:
    if item[0][0:2]=="CC":
        print("\t\t[{}]\t{}".format(item[0], item[1]))
    else:
        print("[{}]\t{}".format(item[0],item[1]))

cont=True
while cont:
    selection=input("Choose Selection: ")
    if selection=="CT":
        print('Creating Table')
        pass
    elif selection=="ST":
        pass
    elif selection == "DT":
        pass
    elif selection=="AC":
        pass
    elif selection=="DC":
        pass
    elif selection=="MC":
        pass
    elif selection=="FC":
        pass
    elif selection=="CCN":
        pass
    elif selection=="CCT":
        pass
    elif selection=="CCC":
        pass
    elif selection=="CCK":
        pass
    elif selection=="CCM":
        pass
    else:
        print("Exiting")
        cont=False
        break