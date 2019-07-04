from bs4 import BeautifulSoup
import argparse
import boto3
import logging
import os
import pandas as pd
import requests
import unittest

WORKING_DIRECTORY = os.getcwd()

def get_logger():
    '''Returns a logging instance for the script
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

DYNAMO_TABLE_NAME = "prod-sneakpeek-table"

HOMEPAGE_URL = 'http://prod-sneakpeek.s3-website-us-east-1.amazonaws.com/'


def get_boto_clients(resource_name, region_name='us-east-1'):
    '''Returns the boto client for various cloudformation resources
        Parameters
        ----------
        resource_name : str
            Name of the resource for the client

        region_name : str
                aws region you are using, defaults to
                us-east-1

        Returns
        -------


        Raises
        ------
    '''
    return(boto3.client(resource_name, region_name))


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

    def test_dynamodb(self):
        '''Tests json file containing cognito config is present

            Parameters
            ----------

            Returns
            -------

            Raises
            ------
        '''

        """
            Dict that will be put in the dynamodb table
        """
        test_dict = {"id":{"S":"1"}, "load_id":{"N":"100000"},
        "output_class":{"N":"1"}}


        """
            Creates dynamodb resource and
            puts an item in the table
        """
        dynamo_client = get_boto_clients(resource_name='dynamodb',
        region_name='us-east-1')


        put_response = dynamo_client.put_item(TableName=DYNAMO_TABLE_NAME,
        Item=test_dict)

        logging.info("successfully put the item in dynamodb")
        logging.info(put_response)

        """
            Removes non-primary key fields and gets the item inserted
            from the put item command

            Tests the response against the original put_item
        """
        output_class = test_dict.pop('output_class')

        dummy_item = dynamo_client.get_item(TableName=DYNAMO_TABLE_NAME,
        Key=test_dict)

        logging.info("Dummy item returned: ")

        logging.info(dummy_item)

        self.assertEqual(
            int(dummy_item['Item']['output_class']['N']),
            int(output_class['N'])
            )


        """
            deletes the dummy item and tests to make sure it
            was successfully deleted
        """
        removed_item = dynamo_client.delete_item(TableName=DYNAMO_TABLE_NAME,
        Key=test_dict)

        logging.info("Deletion Response:")
        logging.info(removed_item)

        """
            Making another get call after the item
            was deleted
        """
        self.assertEqual(
            removed_item['ResponseMetadata']['HTTPStatusCode'], 200
            )






if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    args = parser.parse_args()

    print(args.integers)
    '''
    unittest.main()
