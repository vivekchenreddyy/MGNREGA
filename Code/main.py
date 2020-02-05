import sqlite3
import pandas as pd
from Code.Gramapanchayat import Grama
from Code.Projects import Projects
from Code.User import User
from Code.Member import Memberclass

"""Sql function with the database."""
def sql_connection():

    con = sqlite3.connect('MGNREGA.db')
    return con



con = sql_connection()

"""ProjectMain class."""
class main:
    def choice_input(con):
        choice = input(">>> ").lower().rstrip()
        return choice
    def login_input_uname(con):
        uname = input("Please enter the username : ")
        return uname

    def login_input_password(con):

        passwd = input("Please enter the password : ")
        return passwd

    """Login function to log into the portal."""
    def Login(con):
        print('Welcome to MGNREGA Login')
        uname = main.login_input_uname(con)
        passwd = main.login_input_password(con)
        cursorObj = con.cursor()
        cursorObj.execute('''Select * from Users where username=? and password= ?''', (uname, passwd))
        user = cursorObj.fetchone()
        if user==None:
            print('No users found with the credentials')
            print('Please login again with correct credentials')
            return main.Login(con)

        if user[3] == 'admin':
            print('Welcome BDO here is your console')
            main.BDO(uname)
        elif user[3] == 'gpm':
            print('Welcome GPM here is your console')
            main.GPM(uname)
        elif user[3] == 'member':
            print('Welcome to the employees portal')
            main.Member(uname)

    """BDO is a sub function to call all the functionalities corresponding to BDO."""

    def BDO(buname):
        while True:
            print("\nMenu\n(1)Create GPM accounts\n(2)Delete GPM accounts\n(3)Update GPM\n(4)Create Project\n(5)Update "
                  "Project\n(6)Delete Project\n(7)Show GPM accounts\n(8)Show Projects\n(9)Show member accounts\n(10)See "
                  "the complaints\n(11)Approve Pending Requests\n(12)Previous Menu")
            choice = input(">>> ").lower().rstrip()
            if choice == "1":
                print('Here you can add new GPM accounts')
                bdoid = buname

                User.sign_up(con, 'gpm', bdoid)

            elif choice == "2":
                print('Here you can delete GPM accounts')
                gpms = Grama.List_of_gpms(con, buname)
                pd.set_option('display.width', None)
                df = pd.DataFrame(gpms)
                df.columns = ['name', 'username', 'area', 'pincode', 'BdoUsername']
                print(df)
                uname = input("Please enter a username to be deleted : ")
                User.delete_account(con, uname, 'gpm')

            elif choice == "3":
                print('Here you can Update GPM accounts')
                gpms = Grama.List_of_gpms(con, buname)
                pd.set_option('display.width', None)
                df = pd.DataFrame(gpms)
                df.columns = ['name', 'username', 'area', 'pincode', 'BdoUsername']
                print(df)
                gpmid = input('Enter the GpmId you want to update : ')
                Grama.Update_GPM(con,buname, gpmid)

            elif choice == "4":
                print('Here you can Create a project')
                Projects.Create_project(con)

            elif choice == "5":
                cursorObj = con.cursor()

                print('Here you can Update a ProjectMain')
                Projects.show_projects(con)
                projid = input('Enter the id of the project you want to edit : ')
                cursorObj.execute('SELECT * from Projects where Projectid=?', (projid,))
                projects=cursorObj.fetchone()
                if projects is not None:
                    Projects.Update_project(con, projid)
                else:
                    print('No project found with the id',projid)

            elif choice == "6":
                print('Here you can Delete a project')
                Projects.show_projects(con)
                projid = input('Enter the id of the project you want to delete : ')
                Projects.Delete_project(con, projid)

            elif choice == "7":
                print('Here you can see all the accounts')
                gpms = Grama.List_of_gpms(con, buname)
                pd.set_option('display.width', None)
                df = pd.DataFrame(gpms)
                df.columns = ['name', 'username', 'area', 'pincode', 'BdoUsername']
                print(df)

            elif choice == "8":
                print('Here you can see all the projects')
                Projects.show_projects(con)
            elif choice == "9":
                print('Here you can see all the member accounts')
                cursorObj = con.cursor()
                cursorObj.execute('SELECT Members.username,Members.Gpmapproved,Members.Bdoapproved,Members.WorkingDays,'
                                  'Members.pincode,Members.wage,Members.attendance,Members.projectid from GPM INNER JOIN '
                                  'Members on GPM.username=Members.Gpmid '
                                  'where GPM.Bdo_id=?', (buname,))
                member_under_bdos=cursorObj.fetchall()
                pd.set_option('display.width', None)
                df = pd.DataFrame(member_under_bdos)
                df.columns = ['Username', 'Gpm_Approved', 'Bdo_Approved', 'WorkingDays', 'Pincode','Wage','Attendance','ProjectId']
                print(df)

            elif choice == "10":
                print('Here you can see all the issues raised by the member under you')
                cursorObj = con.cursor()
                cursorObj.execute('SELECT Members.username from GPM INNER JOIN Members on GPM.username=Members.Gpmid '
                                  'where GPM.Bdo_id=?', (buname,))
                memberid = cursorObj.fetchall()
                for member in memberid:
                    cursorObj.execute('SELECT * from Complaints where memberid= ? ', (member[0],))
                    Complaints_received=cursorObj.fetchall()
                    pd.set_option('display.width', None)
                    df = pd.DataFrame(Complaints_received)
                    try:
                        df.columns = ['Id', 'Issue', 'MemberId','Bdo_remarks','Gpm_remarks']
                        print(df)
                    except:
                        print('')
                        main.BDO(buname)
            elif choice == "11":
                Projects.show_projects(con)
                cursorObj = con.cursor()
                cursorObj.execute('SELECT Members.username,Members.Gpmapproved,Members.Bdoapproved,Members.WorkingDays,'
                                  'Members.pincode,Members.wage,Members.attendance,Members.projectid from GPM INNER JOIN '
                                  'Members on GPM.username=Members.Gpmid '
                                  'where GPM.Bdo_id=?', (buname,))
                member_under_bdos = cursorObj.fetchall()
                pd.set_option('display.width', None)
                df = pd.DataFrame(member_under_bdos)
                df.columns = ['Username', 'Gpm_Approved', 'Bdo_Approved', 'WorkingDays', 'Pincode', 'Wage', 'Attendance',
                              'ProjectId']
                print(df)
                memuname = input('Enter the member username you want to approve : ')
                Projects.Approve_Projects(con,memuname)

            elif choice == "12":
                main.Login_master(con)

            else:
                print("Invalid choice, please choose again\n")

    """GPM is a sub function to call all the functionalities corresponding to GPM."""

    def GPM(guname):
        while True:
            print("\nMenu\n(1)Add Members\n(2)Show Members\n(3)Assign the members to projects\n(4)Pending approvals\n"
                  "(5)Delete Members\n(6)Previous Menu\n")
            choice = input(">>> ").lower().rstrip()

            if choice == "1":
                print('Welcome Please enter the details to signup')
                User.sign_up(con, 'member', guname)

            elif choice == "2":
                Memberclass.show_members(con, guname)

            elif choice == "3":
                print('Here you can assign projects to members')
                Projects.show_projects(con)
                Memberclass.show_members(con, guname)
                Projects.Assign_projects(con)

            elif choice == "4":
                print('Here you can see all the pending approvals')
                Memberclass.Approval_pending(con, guname)

            elif choice == "6":
                main.Login_master(con)
            elif choice == "5":
                Memberclass.show_members(con,guname)
                Memberclass.delete_member(con)
            else:
                print("Invalid choice, please choose again\n")

    """Member is a sub function to call all the functionalities corresponding to Member."""

    def Member(muname):
        while True:
            print("\nMenu\n(1)View Details\n(2)File complaints\n(3)Previous Menu")
            choice = input(">>> ").lower().rstrip()
            if choice == "1":
                print('Welcome You can check your details here')
                Memberclass.show_my_details(con, muname)

            elif choice == "2":
                print('Here you can file complaints against your BDO and GPM')
                Memberclass.complaints(con, muname)

            elif choice == "3":
                main.Login_master(con)

            else:
                print("Invalid choice, please choose again\n")

    """This is the outer function which calls Login function."""

    def Login_master(con):
        while True:
            print('Welcome to MGNREGA console portal')
            print('===========================')
            print('||        Menu           ||')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

            print('||      (1)Login         ||')
            print('||      (2)Quit          ||')
            print('===========================')

            choice=main.choice_input(con)
            if choice == "1":
                main.Login(con)
            elif choice == "2":
                print('Thank you visit again')
                exit()
            else:
                print('Invalid Input')


main.Login_master(con)
