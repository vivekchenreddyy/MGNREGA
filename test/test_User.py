import builtins
import sqlite3
import unittest
from sqlite3 import Error
from unittest.mock import patch

from User import User


class TestCase(unittest.TestCase):
    try:
        con = sqlite3.connect('MGNREGA.db')
    except Error:
        print(Error)

    def setUp(self) -> None:
        self.db = self.con

    def tearDown(self) -> None:
        cursorObj = self.con.cursor()
        cursorObj.execute('DELETE from Users')
        cursorObj.execute('DELETE from Members')
        cursorObj.execute('DELETE from GPM')
        self.con.commit()


    #
    #
    # def test_delete_account():
    #     assert User.delete_account(con, 'bdo', 'admin')

    @patch.object(User, 'username_input')
    @patch.object(User, 'password_input')
    @patch.object(User, 'name_input')
    @patch.object(User, 'pincode_input')
    @patch.object(User, 'area_input')
    def test_sign_up(self, area_input, pincode_input, name_input, password_input, username_input):

        input_array = ['username', 'password', 'name', 302943, 'area']
        username_input.return_value = input_array[0]
        password_input.return_value = input_array[1]
        name_input.return_value = input_array[2]
        pincode_input.return_value = input_array[3]
        area_input.return_value = input_array[4]

        User.sign_up(self.db, 'gpm', 'admin')
        cursorObj = self.con.cursor()
        cursorObj.execute('''SELECT * from Users where username=?''',(input_array[0],))
        output=cursorObj.fetchone()
        self.assertIsNotNone(output)


if __name__ == '__main__':
    unittest.main()
