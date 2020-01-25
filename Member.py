import pandas as pd

class Memberclass:
    def complaint_input(con):
        Issue = input('Please mention your issues that you would like to pass on to your BDO and GPM : ')
        return Issue
    def complaints(con, muname):
        cursorObj = con.cursor()
        Issue=Memberclass.complaint_input(con)
        complaints_entity = (Issue, muname)
        cursorObj.execute(
            '''INSERT INTO Complaints(Issue, MemberId) VALUES(?,?)''',
            complaints_entity)
        con.commit()
        print('Successfully notified the complaint')
        return True

    def show_members(con, gpmuname):
        print(gpmuname)
        print('Here is the list of all the members working under you. ')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * from Members where Gpmid=?', (gpmuname,))
        members = cursorObj.fetchall()
        if members is not None:
            pd.set_option('display.width', None)
            df = pd.DataFrame(members)
            df.columns = ['Gpmid', 'Gpm_approved', 'WorkingDays', 'Bdo_approved', 'pincode', 'wage', 'attendance','username','projectid']
            print(df)
            return True
        else:
            print('No projects found')
            return False

    def show_my_details(con, muname):
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * from Members where username=?', (muname,))
        members = cursorObj.fetchall()
        if members is not None:
            pd.set_option('display.width', None)
            df = pd.DataFrame(members)
            df.columns = ['Gpmid', 'Gpm_approved', 'WorkingDays', 'Bdo_approved', 'pincode', 'wage', 'attendance',
                          'username',
                          'projectid']
            print(df)
            return True
        else:
            return False


