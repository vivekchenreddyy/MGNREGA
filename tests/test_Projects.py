import sqlite3
import unittest
from sqlite3 import Error
from unittest.mock import patch

from Code.Projects import Projects


class TestCase(unittest.TestCase):
    con = sqlite3.connect('MGNREGA.db')

    def setUp(self) -> None:
        self.db = self.con

    def tearDown(self) -> None:
        cursorObj = self.con.cursor()

        self.con.commit()

    @patch.object(Projects, 'memuname_input')
    @patch.object(Projects, 'project_id_input')
    def test_Assign_projects(self, project_id_input, memuname_input):
        project_id_input.return_value = 3
        memuname_input.return_value = 'member'
        Projects.project_id_input(self.db)
        cursorObj = self.con.cursor()
        cursorObj.execute('Select * from Members where projectid=? and username=? and Gpmapproved =?',
                          (2, 'member', 1,))
        test_assignproject_output = cursorObj.fetchall()
        self.assertIsNotNone(test_assignproject_output)

    def test_show_projects(self):
        projects_output = Projects.show_projects(self.db)
        self.assertTrue(projects_output)

    def test_delete_project(self):
        Projects.Delete_project(self.con, 13)
        cursorObj = self.con.cursor()
        cursorObj.execute('Select * from Projects where Projectid=?', (13,))
        output = cursorObj.fetchone()
        self.assertIsNone(output)

    def test_Approve_Projects(self):
        approve_projects_output = Projects.Approve_Projects(self.db, 'member')
        self.assertTrue(approve_projects_output)

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

    @patch.object(Projects, 'name_input')
    @patch.object(Projects, 'Type_input')
    @patch.object(Projects, 'area_input')
    @patch.object(Projects, 'member_input')
    @patch.object(Projects, 'cost_est_input')
    @patch.object(Projects, 'start_date_input')
    @patch.object(Projects, 'end_date_input')
    def test__project_update(self, end_date_input, start_date_input, cost_est_input, member_input, area_input,
                             Type_input, name_input):
        input_array = ['2019-02-22', '2019-02-21', 2000, 200, 'updatedarea', 'type', 'name']
        end_date_input.return_value = input_array[0]
        start_date_input.return_value = input_array[1]
        cost_est_input.return_value = input_array[2]
        member_input.return_value = input_array[3]
        area_input.return_value = input_array[4]
        Type_input.return_value = input_array[5]
        name_input.return_value = input_array[6]

        Projects.Update_project(self.db, 2)
        cursorObj = self.con.cursor()
        cursorObj.execute('''SELECT * from Projects where area=?''', (input_array[4],))
        output = cursorObj.fetchone()
        self.assertIsNotNone(output)

    @patch.object(Projects, 'memuname_input')
    @patch.object(Projects, 'project_id_input')
    def test_Assign_projects(self, project_id_input, memuname_input):
        project_id_input.return_value = 2
        memuname_input.return_value = 'member'
        assign_projects_output = Projects.Assign_projects(self.db)
        self.assertTrue(assign_projects_output)


if __name__ == '__main__':
    unittest.main()
