from bs4 import BeautifulSoup
import logging
import os
import pandas as pd
import requests
import unittest

WORKING_DIRECTORY = os.getcwd()
logging.basicConfig(
filename=os.path.join(WORKING_DIRECTORY, 'tests/runlog.txt'),
format='%(asctime)s %(message)s',
 datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logging.info('\n')
class WebappLive(unittest.TestCase):
    '''Tests that the aws resources necessary for the webpage are running

        Note that if any of the below unit tests fail,
        The python script will have a non-zero exit code

        This will cause any CodeBuild Builds to fail out

        Preventing the Code Pipeline from continuing to delivery
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
        logging.info("Testing if the website is alive")
        r = requests.get(
            'http://dev-sneekpeek.s3-website-us-east-1.amazonaws.com/'
        )
        self.assertEqual(r.status_code, 200)
        logging.info("The website is live")
        
    @unittest.skip("Skipping until Cognito user pool is live")
    def test_login(self):
        '''Tests that we are able to login to the webpage

            Parameters
            ----------

            Returns
            -------

            Raises
            ------
        '''
        """
            Starting a request session for the
            user login
        """
        logging.info("Started a requests session")
        with requests.Session() as s:
            login_homepage = s.get(
                "http://dev-sneekpeek.s3-website-us-east-1.amazonaws.com/register.html"
                )
            # bsObj = BeautifulSoup(login_homepage.text, "lxml")
            links =( bsObj.find("div", {"id":"noCognitoMessage"})
					.find("div", {"class":"panel"})
					.find("h3", {"class":"panel-title"}))
        """
        This should be None once the cognito user pool is
        added for login
        """
        self.assetIsNone(links)
        import pdb; pdb.set_trace()

if __name__ == '__main__':
    unittest.main()
