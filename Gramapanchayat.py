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

    def name_input(con):
        name = str(input("Enter the name : "))
        return name

    def pincode_input(con):
        try:
            pincode = int(input("Enter the pincode : "))
            return pincode

        except:
            print('Wrong pincode entered Please enter correct format')
            return None

    def area_input(con):
        area = str(input("Enter the area of residence : "))
        return area

    def Update_GPM(con,buname, gpmid):
        cursorObj = con.cursor()
        cursorObj1 = con.cursor()
        cursorObj1.execute('Select * from GPM where username=?',(gpmid,))
        if cursorObj1.fetchone() is None:
            print('No GPMs with the username exists')
            return False
        cursorObj.execute('SELECT * from GPM where Bdo_id= ? ', (buname,))
        name = Grama.name_input(con)
        area = Grama.area_input(con)
        pincode = Grama.pincode_input(con)
        while pincode is None:
            print('Please try again')
            pincode = Grama.pincode_input(con)

        updateGpmentity = (name, area, pincode, gpmid)
        cursorObj.execute(
            'UPDATE GPM SET name = ? ,area=? , pincode=? where username=?',
            updateGpmentity)
        print('GPM details updated successfully')
        con.commit()

