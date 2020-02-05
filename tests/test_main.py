# import sqlite3
# import unittest
# from sqlite3 import Error
# from unittest.mock import patch
#
# from Code.main import main
#
#
# class TestCase(unittest.TestCase):
#     try:
#         con = sqlite3.connect('MGNREGA.db')
#     except Error:
#         print(Error)
#
#     def setUp(self) -> None:
#         self.db = self.con
#
#     def tearDown(self) -> None:
#         cursorObj = self.con.cursor()
#
#         self.con.commit()
#
#     @patch.object(main, 'choice_input')
#     def test_Login_master(self,choice_input):
#         choice_input.return_value =2
#         output=main.Login_master(self.con)
#         self.assertIsNone(output)
#
#
#
# if __name__ == '__main__':
#     unittest.main()
