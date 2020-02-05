import sqlite3
import unittest
from sqlite3 import Error
from unittest.mock import patch

from Code.Member import Memberclass


class TestCase(unittest.TestCase):

    con = sqlite3.connect('MGNREGA.db')

    def setUp(self) -> None:
        self.db = self.con

    def tearDown(self) -> None:
        cursorObj = self.con.cursor()


        self.con.commit()

    def test_show_my_details(self):
        show_members_output=Memberclass.show_my_details(self.con, 'member')
        self.assertTrue(show_members_output)

    def test_show_my_details_false(self):
        show_members_output=Memberclass.show_my_details(self.con, 'membereeeee')
        self.assertIsNotNone(show_members_output)

    def test_show_members(self):
        projects_output=Memberclass.show_members(self.con,'gpm')
        self.assertTrue(projects_output)

    def test_show_members_false(self):
        projects_output=Memberclass.show_members(self.con,'newgpm')
        self.assertFalse(projects_output)

    def test_Approval_pending(self):
        approval_pending_output=Memberclass.Approval_pending(self.con, 'gpm')
        self.assertTrue(approval_pending_output)

    def test_Approval_pending_false(self):
        approval_pending_output=Memberclass.Approval_pending(self.con, 'newgpm')
        self.assertFalse(approval_pending_output)

    @patch.object(Memberclass, 'complaint_input')
    def test_complaints(self, complaint_input):

        input_array = ['New complaint']
        complaint_input.return_value = input_array[0]

        Memberclass.complaints(self.con,'member')
        cursorObj = self.con.cursor()
        cursorObj.execute('''SELECT * from Complaints where Memberid =?''', ('member',))
        output = cursorObj.fetchone()
        self.assertIsNotNone(output)

    @patch.object(Memberclass, 'memid_input')
    def test_delete_member(self,memid_input):
        Memberclass.memid_input='member1'
        deletemember_output=Memberclass.delete_member(self.con)
        self.assertTrue(deletemember_output)






if __name__ == '__main__':
    unittest.main()
