class User:
    def delete_account(con, username, role):
        cursorObj = con.cursor()

        cursorObj.execute('DELETE from Users where role=? and username=?', (role, username))
        cursorObj.execute('DELETE from GPM where username=?',(username,))
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
