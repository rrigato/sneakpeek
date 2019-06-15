from bs4 import BeautifulSoup
import argparse
import logging
import os
import pandas as pd
import requests
import unittest

WORKING_DIRECTORY = os.getcwd()

def get_logger():
    '''Returns a boto cloudformation describe_stacks api call
        Parameters
        ----------
        stack_name: str
            Name of the stack

        Returns
        -------
        cf_response : dict
                Dictionary output of the describe_stacks api call

        Raises
        ------
    '''
    """
        Adds the file name to the logs/ directory without
        the extension
    """
    logging.basicConfig(
        filename=os.path.join(WORKING_DIRECTORY, 'logs/',
        os.path.basename(__file__).split('.')[0]),
        format='%(asctime)s %(message)s',
         datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG
         )
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
        get_logger()

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
            bsObj = BeautifulSoup(login_homepage.text, "html.parser")

            links =( bsObj.find("div", {"id":"noCognitoMessage"})
					)

            logging.info("Checking to make sure cognito is found")
        """
        Testing that the warning message for no authentication
        is hidden
        """
        self.assertEqual(links['style'], 'display: none;')


if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    args = parser.parse_args()

    print(args.integers)
    '''
    unittest.main()
