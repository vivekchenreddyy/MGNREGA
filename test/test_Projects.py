import sqlite3
import unittest
from sqlite3 import Error
from unittest.mock import patch

from test.Projects import Projects


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

    def test_show_projects(self):
        projects_output=Projects.show_projects(self.con)
        self.assertTrue(projects_output)

    def test_delete_account(self):
        Projects.Delete_project(self.con, 13)
        cursorObj = self.con.cursor()
        cursorObj.execute('Select * from Projects where Projectid=?', (13,))
        output = cursorObj.fetchone()
        self.assertIsNone(output)



    @patch.object(Projects, 'Type_input')
    @patch.object(Projects, 'name_input')
    @patch.object(Projects, 'area_input')
    @patch.object(Projects, 'member_input')
    @patch.object(Projects, 'cost_est_input')
    @patch.object(Projects, 'start_date_input')
    @patch.object(Projects, 'end_date_input')
    def test_sign_up(self, end_date_input, start_date_input, cost_est_input, member_input, area_input, name_input,
                     Type_input):

        input_array = ['2019-02-22', '2019-02-21', 2000, 200, 'area', 'name', 'type']
        end_date_input.return_value = input_array[0]
        start_date_input.return_value = input_array[1]
        cost_est_input.return_value = input_array[2]
        member_input.return_value = input_array[3]
        area_input.return_value = input_array[4]
        name_input.return_value = input_array[5]
        Type_input.return_value = input_array[6]

        Projects.Create_project(self.db)
        cursorObj = self.con.cursor()
        cursorObj.execute('''SELECT * from Projects where area=?''', (input_array[4],))
        output = cursorObj.fetchone()
        self.assertIsNotNone(output)

if __name__ == '__main__':
    unittest.main()
