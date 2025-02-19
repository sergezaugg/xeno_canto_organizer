import unittest

import xco 


# define the root path 
xc = xco.XCO(start_path = './tests')
# check where data will be retrieved

# create a template json parameter file (to be edited)
xc.make_param(filename = 'test.json')

# download mp3 files with metadata  
xc.get(params_json = 'test.json', download = True)



class TestCalculations(unittest.TestCase):

    def test_sum(self):
        calculation = Calculations(8, 2)
        self.assertEqual(calculation.get_sum(), 10, 'The sum is wrong.')

if __name__ == '__main__':
    unittest.main()