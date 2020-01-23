import pandas as pd

class Grama:
    def Show_accounts_GPM(con, bdouname):
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * from GPM where Bdo_id= ? ', (bdouname,))
        accounts = cursorObj.fetchall()
        pd.set_option('display.width', None)
        df = pd.DataFrame(accounts)
        df.columns = ['', 'password', 'name', 'role']
        print(df[['username', 'password', 'name', 'role']])

    def List_of_gpms(con, bdouname):
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * from GPM where Bdo_id= ? ', (bdouname,))

        gpms = cursorObj.fetchall()
        print(gpms)
        return gpms

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

