import sqlite3
from sqlite3 import Error
import pandas as pd
from Gramapanchayat import Grama
from Projects import Projects
from User import User
from Member import Memberclass
def sql_connection():
    try:
        con = sqlite3.connect('MGNREGA.db')
        return con

    except Error:
        print(Error)

con = sql_connection()


def Login(con):
    print('Welcome to MGNREGA Login')
    uname = input("Please enter the username : ")
    passwd = input("Please enter the password : ")
    cursorObj = con.cursor()
    cursorObj.execute('''Select * from Users where username=? and password= ?''', (uname, passwd))
    user = cursorObj.fetchone()
    if user==None:
        print('No users found with the credentials')
        print('Please login again with correct credentials')
        return Login(con)



    if user[3] == 'admin':
        print('Welcome BDO here is your console')
        BDO(uname)
    elif user[3] == 'gpm':
        print('Welcome GPM here is your console')
        GPM(uname)
    elif user[3] == 'member':
        print('Welcome to the employees portal')
        Member(uname)


def Assign_projects(con):
    cursorObj = con.cursor()
    memuname = input('Enter the username of the person you want to assign the project for :  ')
    projectid = input('Enter the projectId you want to tag to the member : ')

    cursorObj.execute('UPDATE Members SET projectid = ? , Gpmapproved= ? where username = ?', (projectid, 1, memuname))

    print('Successfully tagged the project to the member')
    con.commit()


def Approval_pending(con, gpmuname):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from Members where Gpmid= ? OR Bdoapproved!=1 and Gpmapproved!=1', (gpmuname,))
    members = cursorObj.fetchall()
    pd.set_option('display.width', None)
    df = pd.DataFrame(members)
    df.columns = ['Gpmid', 'Gpm_approved', 'WorkingDays', 'Bdo_approved', 'pincode', 'wage', 'attendance', 'username',
                  'projectid']
    print(df[['Gpm_approved', 'Bdo_approved', 'username']])


def Approve_Projects(memuname):
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE Members SET  Bdoapproved= ? where username = ?', (1, memuname))
    con.commit()
    print('Project assign request approved successfully')


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
            Grama.Update_GPM(con, gpmid)

        elif choice == "4":
            print('Here you can Create a project')
            Projects.Create_project(con)

        elif choice == "5":
            print('Here you can Update a Project')
            Projects.show_projects(con)
            projid = input('Enter the id of the project you want to edit : ')
            Projects.Update_project(con, projid)

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
                df.columns = ['Id', 'Issue', 'MemberId','Bdo_remarks','Gpm_remarks']
                print(df)

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
            Approve_Projects(memuname)

        elif choice == "12":
            Login_master()

        else:
            print("Invalid choice, please choose again\n")


def GPM(guname):
    while True:
        print("\nMenu\n(1)Add Members\n(2)Show Members\n(3)Assign the members to projects\n(4)Pending approvals\n("
              "5)Previous Menu")
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
            Assign_projects(con)

        elif choice == "4":
            print('Here you can see all the pending approvals')
            Approval_pending(con, guname)

        elif choice == "5":
            Login_master()
        else:
            print("Invalid choice, please choose again\n")


def Member(muname):
    while True:
        print("\nMenu\n(1)View Details\n(2)File complaints\n(3)Previous Menu")
        choice = input(">>> ").lower().rstrip()
        if choice == "1":
            print('Welcome You can check your details here')
            Projects.show_my_details(con, muname)

        elif choice == "2":
            print('Here you can file complaints against your BDO and GPM')
            Memberclass.complaints(con, muname)

        elif choice == "3":
            Login_master()

        else:
            print("Invalid choice, please choose again\n")


def Login_master():
    while True:
        print('Welcome to MGNREGA console portal')
        print('===========================')
        print('||        Menu           ||')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        print('||      (1)Login         ||')
        print('||      (2)Quit          ||')
        print('===========================')

        choice = input(">>> ").lower().rstrip()
        if choice == "1":
            Login(con)
        elif choice == "2":
            print('Thank you visit again')
            return False
        else:
            print('Invalid Input')


Login_master()
