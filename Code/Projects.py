import datetime
import pandas as pd
"""Projects class where Create update delete and show projects are done."""
class Projects:
    """Input functions."""
    def memuname_input(con):
        memuname = input('Enter the username of the person you want to assign the project for :  ')
        return memuname
    def project_id_input(con):
        projectid = input('Enter the projectId you want to tag to the member : ')
        return projectid
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

    """Create project function."""
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

    """Update project function."""
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
        return True

    """Delete project function."""
    def Delete_project(con, projid):
        cursorObj = con.cursor()
        cursorObj1 = con.cursor()
        cursorObj1.execute('SELECT * from Projects where Projectid=?', (projid,))
        projects=cursorObj1.fetchone()
        if projects is not None:
            cursorObj.execute('DELETE from Projects where Projectid=?', (projid,))
            cursorObj.execute('UPDATE Members SET projectid = NULL where projectid = ?',
                              (projid,))
            print('Project deleted successfully')
            con.commit()
        else:
            print('No project found with Id : ',projid)
    """List of all projects can be seen using this function."""

    def show_projects(con):
        print('Here is the list of all the projects')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * from Projects ')

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
    """Gpm will be able to assign the projects with this function."""

    def Assign_projects(con):
        cursorObj = con.cursor()
        cursorObj1 = con.cursor()
        cursorObj2 = con.cursor()

        memuname = Projects.memuname_input(con)
        cursorObj1.execute('Select * from Members where username = ?',
                          (memuname,))
        members=cursorObj1.fetchone()
        projectid = Projects.project_id_input(con)
        cursorObj2.execute('Select * from Projects where Projectid = ?',
                           (projectid,))
        projects = cursorObj2.fetchone()

        if members and projects is not None:


            cursorObj.execute('UPDATE Members SET projectid = ? , Gpmapproved= ? where username = ?',
                          (projectid, 1, memuname))

            print('Successfully tagged the project to the member')
            con.commit()
            return True
        else:
            print('Project or member not found with given input . Please try again')
            return False
    """Bdo will be able to approve the projects with this function."""
    def Approve_Projects(con,memuname):
        cursorObj = con.cursor()
        cursorObj.execute('UPDATE Members SET  Bdoapproved= ? where username = ?', (1, memuname))
        con.commit()
        print('Project assign request approved successfully')
        return True



