import sqlite3
import unittest
from unittest.mock import patch

from Code.Gramapanchayat import Grama


class TestCase(unittest.TestCase):

    con = sqlite3.connect('MGNREGA.db')


    def setUp(self) -> None:
        self.db = self.con

    def tearDown(self) -> None:
        cursorObj = self.con.cursor()
        # cursorObj.execute('DELETE from Users')
        # cursorObj.execute('DELETE from Members')
        # cursorObj.execute('DELETE from GPM')
        self.con.commit()


    def test_List_of_gpms(self):
        output_list_of_gpms=Grama.List_of_gpms(self.con, 'admin')
        self.assertIsNotNone(output_list_of_gpms)

    @patch.object(Grama, 'name_input')
    @patch.object(Grama, 'area_input')
    @patch.object(Grama, 'pincode_input')
    def test_update_gpm(self,pincode_input, area_input, name_input):

        input_array = ['name', 'area', 'pincode']
        name_input.return_value = input_array[0]
        area_input.return_value = input_array[1]
        pincode_input.return_value = input_array[2]


        Grama.Update_GPM(self.db, 'admin', 'username')
        cursorObj = self.con.cursor()
        cursorObj.execute('''SELECT * from GPM where username=? and name=?''',('username','name',))
        output=cursorObj.fetchone()
        self.assertIsNotNone(output)


if __name__ == '__main__':
    unittest.main()
