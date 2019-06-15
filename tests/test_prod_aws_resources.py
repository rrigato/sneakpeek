from bs4 import BeautifulSoup
import argparse
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

HOMEPAGE_URL = 'http://prod-sneakpeek.s3-website-us-east-1.amazonaws.com/'
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
    @classmethod
    def setUpClass(self):
        '''Unitest function that is run once for the class
            Gets the arguements passed from the user

            Parameters
            ----------

            Returns
            -------

            Raises
            ------
        '''
        pass

    def test_home_page(self):
        '''Tests that the aws resources necessary for the webpage are running

            Parameters
            ----------
                request_url : str
                    Url string to send the request to
            Returns
            -------

            Raises
            ------
        '''
        logging.info("Testing if the website is alive")
        r = requests.get(
            HOMEPAGE_URL
        )
        self.assertEqual(r.status_code, 200)
        logging.info("The website is live")

    def test_cognito_json(self):
        '''Tests json file containing cognito config is present

            Parameters
            ----------

            Returns
            -------

            Raises
            ------
        '''
        logging.info("Testing if cognito json config is present")
        r = requests.get(
            HOMEPAGE_URL + "js/cognito_config.json"
        )
        self.assertEqual(r.status_code, 200)

        """
            Tests that the json response for the cognito
            config file is not empty

        """
        self.assertNotEqual(
                r.json()['cognito']['userPoolId'], ''
                )

        logging.info("Cognito config is present")


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
                HOMEPAGE_URL + "register.html"
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


if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    args = parser.parse_args()

    print(args.integers)
    '''
    unittest.main()
