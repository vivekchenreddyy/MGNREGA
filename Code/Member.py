import pandas as pd

"""Member class is where all the functions corresponding to Member are present."""


class Memberclass:

    """Complaints input is entered here."""

    def complaint_input(con):
        Issue = input('Please mention your issues that you would like to pass on to your BDO and GPM : ')
        return Issue

    """List of complaints can be seen using this function."""
    def memid_input(con):
        memuname=input('Enter the username of the member which you want to delete : ')
        return memuname


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
    """List of members can be seen here."""

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
    """Member can see his details here."""

    def show_my_details(con, muname):
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * from Members where username=?', (muname,))
        members = cursorObj.fetchall()
        if members is not None:
            if members == []:
                return 'Not none'
            else:
                pd.set_option('display.width', None)
                df = pd.DataFrame(members)
                df.columns = ['Gpmid', 'Gpm_approved', 'WorkingDays', 'Bdo_approved', 'pincode', 'wage', 'attendance',
                          'username',
                          'projectid']
                print(df)
                return df
        else:
            print('Empty list')
            return None
    """Pending approvals can be seen here"""
    def delete_member(con):
        cursorObj = con.cursor()
        cursorObj1 = con.cursor()
        memuname=Memberclass.memid_input(con)
        cursorObj.execute('DELETE from Members where username = ?',
                          (memuname,))
        cursorObj1.execute('DELETE from Users where username = ?',
                          (memuname,))
        print('User deleted successfully')
        return True

    def Approval_pending(con, gpmuname):
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * from Members where Gpmid= ? and Bdoapproved!=1 OR Gpmapproved!=1', (gpmuname,))
        members_approval = cursorObj.fetchall()
        if members_approval is not None:

            pd.set_option('display.width', None)
            df = pd.DataFrame(members_approval)
            df.columns = ['Gpmid', 'Gpm_approved', 'WorkingDays', 'Bdo_approved', 'pincode', 'wage', 'attendance', 'username',
                      'projectid']
            print(df[['Gpm_approved', 'Bdo_approved', 'username']])
            return True
        else:
            print('Empty list')
            return False

