import unittest
import pandas as pd
import requests


class WebappLive(unittest.TestCase):
    '''Tests that the aws resources necessary for the webpage are running

        Parameters
        ----------
        Returns
        -------
        Raises
        ------
    '''
    def test_home_page(self):
        '''Tests that the aws resources necessary for the webpage are running

            Parameters
            ----------

            Returns
            -------

            Raises
            ------
        '''
        r = requests.get(
            'http://dev-sneekpeek.s3-website-us-east-1.amazonaws.com/'
        )
        self.assertEqual(r.status_code, 200)
        logging.info("The website is live")
        import pdb; pdb.set_trace()
print("Hello World - First Unit Test")
if __name__ == '__main__':
    unittest.main(exit=False)
    print ("Hello World 2")
