# """
# Author : Serge Zaugg
# Description : 
# """

import unittest
import xco 
import os
import pandas as pd
import shutil

class Test01(unittest.TestCase):

    # re-initialize the dir for temporary test files 
    temp_test_path = './tests_temp'
    if os.path.exists(temp_test_path):
        shutil.rmtree(temp_test_path)
    if not os.path.exists(temp_test_path):
        os.makedirs(temp_test_path)

    # basic tests 
    @classmethod
    def setUpClass(self):
        xc = xco.XCO(start_path = './tests_temp')
        xc.make_param(filename = 'test.json', template = "mini")
        df_records = xc.get_summary(params_json = 'test.json')
        xc.download(df_recs = df_records)
        
    def test_json_created(self):
        self.assertTrue(os.path.isfile('./tests_temp/test.json'), 'JSON file not created')

    def test_num_mp3(self):
        num_files_realized = len(os.listdir('tests_temp/downloaded_data_orig'))
        num_files_expected = 10
        self.assertEqual(num_files_realized, num_files_expected, 'Files are not equal')

    def test_summary_csv(self):   
        df = pd.read_csv('tests_temp/downloaded_data_meta.csv')
        df_shape_realized = df.shape
        df_shape_expected = (10, 39)
        self.assertEqual(df_shape_realized, df_shape_expected, 'Files are not equal')
    

if __name__ == '__main__':
    unittest.main()

# python -m unittest -v

