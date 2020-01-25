class User:
    def delete_account(con, username, role):
        cursorObj = con.cursor()
        try:
            cursorObj.execute('DELETE from Users where role=? and username=?', (role, username))
            cursorObj.execute('DELETE from GPM where username=?',(username,))
        except:
            print('Something wrong while deleting the user please try again')
        con.commit()
        print('Successfully deleted the user ', username)
        return True

    def username_input(con):
        cursorObj1=con.cursor()

        uname = str(input("Enter your desired username : "))
        cursorObj1.execute('SELECT * from Users where username=?', (uname,))
        if cursorObj1.fetchone() is not None:
            print('Username unavailable please try different combination')
            return False
        return uname
    def password_input(con):
        passwd = str(input("Please enter a password : "))
        return passwd

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



    def sign_up(con, role, id):
        cursorObj = con.cursor()
        cursorObj1=con.cursor()
        uname=User.username_input(con)
        cursorObj1.execute('SELECT * from Users where username=?', (uname,))
        if cursorObj1.fetchone() is not None:
            print('Username unavailable please try different combination')
            return False
        passwd = User.password_input(con)
        name=User.name_input(con)
        pincode=User.pincode_input(con)
        while pincode is None:
            print('Please try again')
            pincode=User.pincode_input(con)
        area=User.area_input(con)
        signupentity = (uname, passwd, name, role)

        cursorObj.execute('''INSERT INTO Users(username, password, name, role) VALUES(?, ?, ? ,?)''', signupentity)
        if role == 'gpm':
            gpmentity = (uname, pincode, name, area, id)
            cursorObj.execute('''INSERT INTO GPM(username, pincode, name, area,Bdo_id) VALUES(?, ?, ?, ?, ? )''',
                              gpmentity)
            print('Successfully added a new GPM')
        if role == 'member':
            memberentity = (id, 0, 0, 0, pincode, 0, 0, uname, "NULL")
            cursorObj.execute('''INSERT INTO Members(Gpmid, Gpmapproved, Bdoapproved, Workingdays,pincode,wage,
            attendance,username,projectid) VALUES(?, ?, ?, ? ,?,?,?,?,?)''', memberentity)
            print('Successfully added a new member')

        con.commit()

