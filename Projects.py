import datetime
import pandas as pd

class Projects:

    def Type_input(con):
        Type = input("Enter the type of the project : ")
        return Type
    def name_input(con):
        name = input("Enter the name of the project : ")
        return name
    def area_input(con):
        area = input("Enter the area of the project : ")
        return area

    def member_input(con):
        try:
            total_members = int(input("Enter the total members required of the project : "))
            return total_members

        except:
            print('Wrong format entered ')
            return None

    def cost_est_input(con):
        try:
            cost_est = int(input("Enter the estimated amount of the project : "))
            return cost_est

        except:
            print('Wrong format entered .Please try again')
            return None
    def start_date_input(con):
        start_date_entry = input("Enter the start date of the project of the project in YYYY-MM-DD format : ")
        try:
            year, month, day = map(int, start_date_entry.split('-'))

            start_date = datetime.date(year, month, day)
            return start_date
        except:
            print('Please enter a valid date')
            return None

    def end_date_input(con):

        end_date_entry = input("Enter the end date of the project of the project in YYYY-MM-DD format : ")
        try:
            year, month, day = map(int, end_date_entry.split('-'))
            end_date = datetime.date(year, month, day)
            return end_date
        except:
            print('Please enter a valid date')
            return None

    def Create_project(con):
        cursorObj = con.cursor()
        Type = Projects.Type_input(con)
        name = Projects.name_input(con)
        area = Projects.area_input(con)
        total_members=Projects.member_input(con)

        while total_members is None:
            total_members=Projects.member_input(con)
        cost_est=Projects.cost_est_input(con)

        while cost_est is None:
            cost_est=Projects.cost_est_input(con)
        start_date=Projects.start_date_input(con)
        while start_date is None:
            start_date = Projects.start_date_input(con)
        end_date=Projects.end_date_input(con)

        while end_date is None:
            end_date = Projects.end_date_input(con)
        if end_date<start_date:
            print('End date should be greater than start date.Please enter correct end date again')
            end_date=Projects.end_date_input(con)


        createprojentity = (Type, name, area, total_members, cost_est, start_date, end_date)

        cursorObj.execute('''INSERT INTO Projects( Type, name,area,total_members,cost_est,start_date,end_date) VALUES(?, 
        ?,?, ?,?,?,?)''', createprojentity)
        print('Project created successfully')
        con.commit()

    def Update_project(con, projid):
        cursorObj = con.cursor()
        projname = Projects.name_input(con)
        projtype = Projects.Type_input(con)
        projarea = Projects.area_input(con)
        totalmembers = Projects.member_input(con)

        while totalmembers is None:
            totalmembers = Projects.member_input(con)

        cost_est = Projects.cost_est_input(con)

        while cost_est is None:
            cost_est = Projects.cost_est_input(con)

        start_date = Projects.start_date_input(con)
        while start_date is None:
            start_date = Projects.start_date_input(con)
        end_date = Projects.end_date_input(con)

        while end_date is None:
            end_date = Projects.end_date_input(con)
        if end_date < start_date:
            print('End date should be greater than start date.Please enter correct end date again')
            end_date = Projects.end_date_input(con)
        updateprojentity = (projname, projtype, projarea, totalmembers, cost_est, start_date, end_date, projid)
        cursorObj.execute(
            'UPDATE Projects SET name = ? ,Type=? ,area=? , total_members=? , cost_est=? , start_date=? , '
            'end_date=? where Projectid = ?', updateprojentity)
        print('Project details updated successfully')
        con.commit()

    def Delete_project(con, projid):
        cursorObj = con.cursor()
        cursorObj.execute('DELETE from Projects where Projectid=?', (projid,))
        print('Project deleted successfully')
        con.commit()

    def show_projects(con):
        print('Here is the list of all the projects')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * from Projects')

        projects = cursorObj.fetchall()
        if projects is not None:
            pd.set_option('display.width', None)
            df = pd.DataFrame(projects)
            df.columns = ['projid', 'type', 'name', 'area', 'total_members', 'cost_est', 'start_date', 'end_date']
            print(df)
            return True
        else:
            print('No projects found')
            return False




