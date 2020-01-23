import pandas as pd

class Memberclass:
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
        df.columns = ['Gpmid', 'Gpm_approved', 'WorkingDays', 'Bdo_approved', 'pincode', 'wage', 'attendance',
                      'username',
                      'projectid']
        print(df)

    def show_my_details(con, muname):
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * from Members where username=?', (muname,))
        members = cursorObj.fetchall()
        pd.set_option('display.width', None)
        df = pd.DataFrame(members)
        df.columns = ['Gpmid', 'Gpm_approved', 'WorkingDays', 'Bdo_approved', 'pincode', 'wage', 'attendance',
                      'username',
                      'projectid']
        print(df)


