from argparse import Action
from atexit import register
from email import header
import opcode
import psycopg2
import re
from tabulate import tabulate
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
connection = psycopg2.connect(
    user='postgres',
    password='12345',
    host='localhost',
    port='5432',
    database='postgres'
)
def register():
    username = input("Create UserName: ").strip()
    gmail = input('Enter Gmail: ').strip()
    if (re.fullmatch(regex, gmail)):
        pass
    else:
        print("Invalid Email")
        register()

    password = input('Create Password: ').strip()
    password2 = input('Re-Enter Password: ').strip()


    cursor = connection.cursor()
    check='''select * from register where gmail=%s'''
    cursor.execute(check,(gmail,))
    check_result=cursor.fetchall()
    if password != password2:
        print("password did not match")
        register()
    elif len(check_result)>0:
        print('Gmail Already Exist please enter Another Gmail ')
        register()
    else:
        register_user='''insert into register values (%s,%s,%s)'''
        cursor = connection.cursor()
        cursor.execute(register_user,(username,gmail,password))
        connection.commit()
        print("You are Successfuly Register---")
        connection.close()

def login():
    
    print()
    print('Log-In Page')
    username = input("Enter username: ")
    password = input("Enter Password: ")
    cursor = connection.cursor()
    check='''select * from register where username=%s'''
    cursor.execute(check,(username,))
    check_result=cursor.fetchall()

    if len(check_result)==0:
        print("UserName Not Exist---")
        login()
    elif len(check_result)>0:
        if check_result[0][2]!=password:
            print('Password Did Not Matched---')
            login()
        else:
            print("Login Successful")
            action_user()

            # Add Contacts

def Add_contact():
    print("---------Add Contact----------")
    First_name = input("Enter First Name: ")
    Last_name = input('Enter Last Name: ')
    contact_number = input('Enter Number: ')
    gmail = input("Enter gmail:")

    check_number='''select * from contact where number=%s'''
    cursor = connection.cursor()
    cursor.execute(check_number,(contact_number,))
    exist_number=cursor.fetchall()

    if len(exist_number) >0:
        print('Number Already Exist')
        print()
        Add_contact()
    
    else:
        add_sql_query = '''
        insert into contact (first_name,last_name,number,gmail) values(%s,%s,%s,%s)
        '''
        cursor = connection.cursor()
        cursor.execute((add_sql_query), (First_name,
                   Last_name, contact_number, gmail))
        connection.commit()
        print('Add successfuly....')
        action_user()
        connection.close()



                    # View Contact

def view_contact():
    contact_query =input('Enter first name: ')
    view_sql_query = '''
                    select*from contact where first_name=%s
                    '''
    cursor = connection.cursor()
    cursor.execute(view_sql_query,(contact_query,))
    data=cursor.fetchall()
    header=["FirstName","LastName","Number","Email"]
    print(tabulate(data,headers=header,tablefmt='fancy_grid'))
    action_user()


def view_All_contact():
    view_sql_query = '''
                    select*from contact
                    '''
    cursor = connection.cursor()
    cursor.execute(view_sql_query)
    data=cursor.fetchall()
    header=["FirstName","LastName","Number","Email"]
    print(tabulate(data,headers=header,tablefmt='fancy_grid', missingval='N/A'))
    action_user()

def Update_contact():
    contact_id=input('Enter Contact id what do you want to update: ')
    print('FirstName-----uptade \nLastName----update \nNumber----update \nGmailId----update')
    update_query=input('What do you want to update: ')
    if update_query =='firstname':
        old_value='first_name'
        new_value=input("Enter New FirstName")
    elif update_query == 'lastname':
        old_value='last_name'
        new_value=input("Enter New LastName")
    elif update_query == 'Number':
        old_value= 'number'
        new_value=input('Enter New Number')
    elif update_query == 'gmailid':
        old_value='gmail'
        new_value=input("Enter New GmailId")
    else:
        print("Plese select a valid field !")
        return None
    cursor = connection.cursor()   
    cursor.execute("UPDATE contact SET %s='%s' WHERE contact_id=%s" % (old_value, new_value, contact_id))
    connection.commit()
    action_user()
    
def delete_contact():
    contact_id =input("What contact id do you want to delete:")
    delete_qurey="""
                  DELETE from contact WHERE contact_id=%s
                  """
    cursor = connection.cursor()
    cursor.execute(delete_qurey,contact_id)
    connection.commit()
    print("Contact delete successfuly.....")
    action_user()

def delete_all_contact():
    delete_all_qurey = """TRUNCATE contact"""
    cursor = connection.cursor()
    cursor.execute(delete_all_qurey)
    connection.commit()
    print('Delete successfuly')
    action_user()

def home():
    print()
    print(" <-------Digital Contact Book--------->")
    print()
    print('Plese Enter Login || Register || Exist:')
    UserInput=input("").lower()
    if UserInput=='login':
        login()
    elif UserInput=='register':
        register()



def action_user():
      print('What Perform Do you want:')
      print()
      print('1---Add_Contac \n2---View_Contact \n3---View_All_Contact \n4---Delete_Contact \n5---Delete_All_contact \n6---exite')
      action=input("Enter Number:")
      if action=='1':
        Add_contact()
      elif action=='2':
        view_contact()
      elif action=='3':
        view_All_contact()
      elif action=='4':
        delete_contact()
      elif action=='5':
        delete_all_contact()
      elif action=='6':
        home()

      else:
        print("Enter Valid Number--")

home()