import sqlite3
import unittest
from sqlite3 import Error
from unittest.mock import patch

from test.Member import Memberclass


class TestCase(unittest.TestCase):
    try:
        con = sqlite3.connect('MGNREGA.db')
    except Error:
        print(Error)

    def setUp(self) -> None:
        self.db = self.con

    def tearDown(self) -> None:
        cursorObj = self.con.cursor()


        self.con.commit()

    def test_show_my_details(self):
        show_members_output=Memberclass.show_my_details(self.con, 'member')
        self.assertTrue(show_members_output)

    def test_show_members(self):
        projects_output=Memberclass.show_members(self.con,'gpm')
        self.assertTrue(projects_output)

    # def test_delete_account(self):
    #     Projects.Delete_project(self.con, 13)
    #     cursorObj = self.con.cursor()
    #     cursorObj.execute('Select * from Projects where Projectid=?', (13,))
    #     output = cursorObj.fetchone()
    #     self.assertIsNone(output)

    @patch.object(Memberclass, 'complaint_input')
    def test_complaints(self, complaint_input):

        input_array = ['New complaint']
        complaint_input.return_value = input_array[0]

        Memberclass.complaints(self.con,'member')
        cursorObj = self.con.cursor()
        cursorObj.execute('''SELECT * from Complaints where Memberid =?''', ('member',))
        output = cursorObj.fetchone()
        self.assertIsNotNone(output)

if __name__ == '__main__':
    unittest.main()
