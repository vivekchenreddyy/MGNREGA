import sqlite3
import datetime
from sqlite3 import Error
import pandas as pd



def sql_connection():
    try:
        con = sqlite3.connect('MGNREGA.db')
        return con

    except Error:
        print(Error)


def Create_project(con):
    cursorObj = con.cursor()
    Type = input("Enter the type of the project : ")
    name = input("Enter the name of the project : ")
    area = input("Enter the area of the project : ")
    total_members = input("Enter the total members required of the project : ")
    cost_est = input("Enter the estimated amount of the project : ")
    start_date_entry = input("Enter the start date of the project of the project in YYYY-MM-DD format : ")
    year, month, day = map(int, start_date_entry.split('-'))
    start_date = datetime.date(year, month, day)
    end_date_entry = input("Enter the end date of the project of the project in YYYY-MM-DD format : ")
    year, month, day = map(int, end_date_entry.split('-'))
    end_date = datetime.date(year, month, day)
    createprojentity = (Type, name, area, total_members, cost_est, start_date, end_date)

    cursorObj.execute('''INSERT INTO Projects( Type, name,area,total_members,cost_est,start_date,end_date) VALUES(?, 
    ?,?, ?,?,?,?)''', createprojentity)
    print('Project created successfully')
    con.commit()


def List_of_gpms(con, bdouname):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from GPM where Bdo_id= ? ', (bdouname,))
    gpms = cursorObj.fetchall()
    return gpms


def Show_accounts_GPM(con, bdouname):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from GPM where Bdo_id= ? ', (bdouname,))
    accounts = cursorObj.fetchall()
    pd.set_option('display.width', None)
    df = pd.DataFrame(accounts)
    df.columns = ['', 'password', 'name', 'role']
    print(df[['username', 'password', 'name', 'role']])


def Update_GPM(con, uname):
    cursorObj = con.cursor()
    name = input('Enter the updated GPM name : ')
    area = input('Enter the updated GPM area : ')
    pincode = input('Enter the updated GPM pincode : ')

    updateGpmentity = (name, area, pincode, uname)
    cursorObj.execute(
        'UPDATE GPM SET name = ? ,area=? , pincode=? where username=?',
        updateGpmentity)
    print('GPM details updated successfully')
    con.commit()


def delete_account(con, username, role):
    cursorObj = con.cursor()

    cursorObj.execute('DELETE from Users where role=? and username=?', (role, username))
    con.commit()
    print('Successfully deleted the user ', username)


def sign_up(con, role, id):
    cursorObj = con.cursor()
    uname = input("Enter your desired username : ")
    passwd = input("Please enter a password : ")

    name = input("Enter the name : ")
    pincode = input("Enter the pincode : ")
    area = input("Enter the area of residence : ")
    signupentity = (uname, passwd, name, role)
    cursorObj.execute('''INSERT INTO Users(username, password, name, role) VALUES(?, ?, ? ,?)''', signupentity)
    if role == 'gpm':
        gpmentity = (uname, pincode, name, area, id, '')
        cursorObj.execute('''INSERT INTO GPM(username, pincode, name, area,Bdo_id,complaints) VALUES(?, ?, ?, ?, ? ,
        ?)''', gpmentity)
        print('Successfully added a new GPM')
    if role == 'member':
        memberentity = (id, 0, 0, 0, pincode, 0, 0, uname, "NULL")
        cursorObj.execute('''INSERT INTO Members(Gpmid, Gpmapproved, Bdoapproved, Workingdays,pincode,wage,
        attendance,username,projectid) VALUES(?, ?, ?, ? ,?,?,?,?,?)''', memberentity)
        print('Successfully added a new member')
    con.commit()


con = sql_connection()


def Login(con):
    print('Welcome to MGNREGA Login')
    uname = input("Please enter the username : ")
    passwd = input("Please enter the password : ")
    cursorObj = con.cursor()
    try:
        cursorObj.execute('''Select * from Users where username=? and password= ?''', (uname, passwd))
    except:
        print('No users found with the credentials')

    user = cursorObj.fetchone()
    try:
        if user[3] == 'admin':
            print('Welcome BDO here is your console')
            BDO(uname)
        elif user[3] == 'gpm':
            print('Welcome GPM here is your console')
            GPM(uname)
        elif user[3] == 'member':
            print('Welcome to the employees portal')
            Member(uname)
    except:
        print('No account found please login with correct credentials')


def Update_project(con, projid):
    cursorObj = con.cursor()
    projname = input('Enter the updated project name : ')
    projtype = input('Enter the updated project type : ')
    projarea = input('Enter the updated project area : ')
    totalmembers = input('Enter the updated required members for the project : ')
    cost_est = input("Enter the updated estimated amount of the project : ")
    start_date_entry = input("Enter the updated start date of the project of the project in YYYY-MM-DD format : ")
    year, month, day = map(int, start_date_entry.split('-'))
    start_date = datetime.date(year, month, day)
    end_date_entry = input("Enter the updated end date of the project of the project in YYYY-MM-DD format : ")
    year, month, day = map(int, end_date_entry.split('-'))
    end_date = datetime.date(year, month, day)
    updateprojentity = (projname, projtype, projarea, totalmembers, cost_est, start_date, end_date, projid)
    cursorObj.execute('UPDATE Projects SET name = ? ,Type=? ,area=? , total_members=? , cost_est=? , start_date=? , '
                      'end_date=? where Projectid = ?', updateprojentity)
    print('Project details updated successfully')
    con.commit()


def Delete_project(con, projid):
    cursorObj = con.cursor()
    cursorObj.execute('DELETE from Projects where Projectid=?', (projid))
    print('Project deleted successfully')
    con.commit()


def show_projects(con):
    print('Here is the list of all the projects')
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from Projects')
    projects = cursorObj.fetchall()
    pd.set_option('display.width', None)
    df = pd.DataFrame(projects)
    df.columns = ['projid', 'type', 'name', 'area', 'total_members', 'cost_est', 'start_date', 'end_date']
    print(df)


def complaints(con, muname):
    cursorObj = con.cursor()
    Issue = input('Please mention your issues that you would like to pass on to your BDO and GPM : ')
    complaints_entity = (Issue, muname)
    cursorObj.execute(
        '''INSERT INTO Complaints(Issue, MemberId) VALUES(?,?)''',
        complaints_entity)
    con.commit()
    print('Successfully notified the complaint')


def show_members(con, gpmuname):
    print(gpmuname)
    print('Here is the list of all the members working under you. ')
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from Members where Gpmid=?', (gpmuname,))
    members = cursorObj.fetchall()
    pd.set_option('display.width', None)
    df = pd.DataFrame(members)
    df.columns = ['Gpmid', 'Gpm_approved', 'WorkingDays', 'Bdo_approved', 'pincode', 'wage', 'attendance', 'username',
                  'projectid']
    print(df)


def show_my_details(con, muname):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from Members where username=?', (muname,))
    members = cursorObj.fetchall()
    pd.set_option('display.width', None)
    df = pd.DataFrame(members)
    df.columns = ['Gpmid', 'Gpm_approved', 'WorkingDays', 'Bdo_approved', 'pincode', 'wage', 'attendance', 'username',
                  'projectid']
    print(df)


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


def BDO(uname):
    while True:
        print("\nMenu\n(1)Create GPM accounts\n(2)Delete GPM accounts\n(3)Update GPM\n(4)Create Project\n(5)Update "
              "Project\n(6)Delete Project\n(7)Show GPM accounts\n(8)Show Projects\n(9)Show member accounts\n(10)See "
              "the complaints\n(11)Approve Pending Requests\n(12)Previous Menu")
        choice = input(">>> ").lower().rstrip()
        if choice == "1":
            print('Here you can add new GPM accounts')
            bdoid = uname
            sign_up(con, 'gpm', bdoid)

        elif choice == "2":
            print('Here you can delete GPM accounts')
            gpms = List_of_gpms(con, uname)
            pd.set_option('display.width', None)
            df = pd.DataFrame(gpms)
            df.columns = ['name', 'username', 'area', 'pincode', 'BdoUsername', 'complaints']
            print(df)
            uname = input("Please enter a username to be deleted : ")
            delete_account(con, uname, 'gpm')

        elif choice == "3":
            print('Here you can Update GPM accounts')
            gpms = List_of_gpms(con, uname)
            pd.set_option('display.width', None)
            df = pd.DataFrame(gpms)
            df.columns = ['name', 'username', 'area', 'pincode', 'BdoUsername', 'complaints']
            print(df)
            gpmid = input('Enter the GpmId you want to update : ')
            Update_GPM(con, gpmid)

        elif choice == "4":
            print('Here you can Create a project')
            Create_project(con)

        elif choice == "5":
            print('Here you can Update a Project')
            show_projects(con)
            projid = input('Enter the id of the project you want to edit : ')
            Update_project(con, projid)

        elif choice == "6":
            print('Here you can Delete a project')
            show_projects(con)
            projid = input('Enter the id of the project you want to delete : ')
            Delete_project(con, projid)

        elif choice == "7":
            print('Here you can see all the accounts')
            gpms = List_of_gpms(con, uname)
            pd.set_option('display.width', None)
            df = pd.DataFrame(gpms)
            df.columns = ['name', 'username', 'area', 'pincode', 'BdoUsername', 'complaints']
            print(df)

        elif choice == "8":
            print('Here you can see all the projects')
            show_projects(con)
        elif choice == "9":
            print('Here you can see all the member accounts')
            gpms = List_of_gpms(con, uname)
            for gpm in gpms:
                show_members(con, gpm[1])

        elif choice == "10":
            print('Here you can see all the issues raised by the member under you')
            cursorObj = con.cursor()
            cursorObj.execute('SELECT Members.username from GPM INNER JOIN Members on GPM.username=Members.Gpmid '
                              'where GPM.Bdo_id=?', (uname,))
            memberid = cursorObj.fetchall()
            for member in memberid:
                print(member)
                cursorObj.execute('SELECT * from Complaints where memberid= ? ', (member[0],))
                print(cursorObj.fetchall())

        elif choice == "11":
            show_projects(con)
            gpms = List_of_gpms(con, uname)
            for gpm in gpms:
                show_members(con, gpm[1])
            memuname = input('Enter the member username you want to approve : ')

            Approve_Projects(memuname)

        elif choice == "12":
            Login_master()

        else:
            print("Invalid choice, please choose again\n")


def GPM(uname):
    while True:
        print("\nMenu\n(1)Add Members\n(2)Show Members\n(3)Assign the members to projects\n(4)Pending approvals\n("
              "5)Previous Menu")
        choice = input(">>> ").lower().rstrip()

        if choice == "1":
            print('Welcome Please enter the details to signup')
            sign_up(con, 'member', uname)

        elif choice == "2":
            show_members(con, uname)

        elif choice == "3":
            print('Here you can assign projects to members')
            show_projects(con)
            show_members(con, uname)
            Assign_projects(con)

        elif choice == "4":
            print('Here you can see all the pending approvals')
            Approval_pending(con, uname)

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
            show_my_details(con, muname)

        elif choice == "2":
            print('Here you can file complaints against your BDO and GPM')
            complaints(con, muname)

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
