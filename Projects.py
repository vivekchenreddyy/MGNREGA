import datetime
import pandas as pd

class Projects:
    def Create_project(con):
        cursorObj = con.cursor()
        Type = input("Enter the type of the project : ")
        name = input("Enter the name of the project : ")
        area = input("Enter the area of the project : ")
        total_members = input("Enter the total members required of the project : ")
        cost_est = input("Enter the estimated amount of the project : ")
        start_date_entry = input("Enter the start date of the project of the project in YYYY-MM-DD format : ")
        year, month, day = map(int, start_date_entry.split('-'))
        try:
            start_date = datetime.date(year, month, day)
        except:
            print('Please enter a valid date')
        end_date_entry = input("Enter the end date of the project of the project in YYYY-MM-DD format : ")
        year, month, day = map(int, end_date_entry.split('-'))
        try:
            end_date = datetime.date(year, month, day)
        except:
            print('Please enter a valid date')
        createprojentity = (Type, name, area, total_members, cost_est, start_date, end_date)

        cursorObj.execute('''INSERT INTO Projects( Type, name,area,total_members,cost_est,start_date,end_date) VALUES(?, 
        ?,?, ?,?,?,?)''', createprojentity)
        print('Project created successfully')
        con.commit()

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
        cursorObj.execute(
            'UPDATE Projects SET name = ? ,Type=? ,area=? , total_members=? , cost_est=? , start_date=? , '
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




