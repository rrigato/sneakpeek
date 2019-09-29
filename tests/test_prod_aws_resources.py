from bs4 import BeautifulSoup
import argparse
import boto3
import json
import logging
import os
import pandas as pd
import requests
import unittest

ENVIRON_DEF = "prod"
DYNAMO_TABLE_NAME = ENVIRON_DEF + "-sneakpeek-table"

HOMEPAGE_URL = 'http://prod-sneakpeek.s3-website-us-east-1.amazonaws.com/'

LAMBDA_FUNCTION_NAME = ENVIRON_DEF + "lambda-ride-sneakpeek"
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


    def test_lambda_ride(self):
        '''Tests that the lambda function called for /ride is live

            Parameters
            ----------

            Returns
            -------

            Raises
            ------
        '''
        logging.info("Testing the following lambda function: ")
        logging.info(LAMBDA_FUNCTION_NAME)

        """
            Opens the json file to be used as payload
            for invoking the lambda function
        """
        with open("tests/events/ride_event.json",
            "r") as ride_event:
            ride_payload = json.load(ride_event)

        logging.info("Test event json")
        logging.info(ride_payload)
        lambda_client = get_boto_clients('lambda')

        logging.info("Calling lambda function")
        """
            Invoke the lambda function with the
            provided json event
            Syncronous event call
        """
        ride_response = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,

            InvocationType="RequestResponse",
            Payload=json.dumps(ride_payload)

        )
        ride_payload = json.load(ride_response['Payload'])

        logging.info("Lambda function response")
        logging.info(ride_response)

        self.assertEqual(
            ride_payload['body']['Unicorn']['Name'],
            "Rocinante"
        )


    def test_cognito_config(self):
        '''Tests that the user identification is populated

            The static/js/cognito_config.json is populated at
            build time for the cloudformation stack.
            This test ensures elements of that json are not empty

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
            HOMEPAGE_URL + "js/cognito_config.json"
        )

        logging.info("Got the cognito configuration response")
        json_response = r.json()

        logging.info(json_response)

        """
            Checking that all key javascript configuration
            values are populated
        """
        self.assertNotEqual(
            json_response['cognito']['IdentityPoolId'],
            "")

        self.assertNotEqual(
            json_response['cognito']['userPoolId'],
            "")

        self.assertNotEqual(
            json_response['cognito']['IdentityAuthorizedRoleArn'],
            "")

        self.assertNotEqual(
            json_response['cognito']['userPoolClientId'],
            "")

        self.assertNotEqual(
            json_response['backend']['ImageUploadBucket'],
            "")

        logging.info("All key config values are populated")

    #@unittest.skip("Skipping for now")
    def test_ssm_parameters(self, parameter_dict={
        "/prod/UserPoolClientId":"Default",
        "/prod/IdentityAuthorizedRoleArn":"Default",
        "/prod/IdentityPoolId":"Default",
        "/prod/UserPoolId":"Default"
        }):
        '''Tests the ssm parameters store values are not empty

            These parameters are dynamically populated
            When they are created in the cloudformation script
            They have a value of Default.

            CodeBuild populates these parameters in
            the build stage

            Parameters
            ----------
            parameter_dict : dict
                Key value pair where the key is the
                ssm parameter name and the value is
                what we expect the ssm parameter to be


            Returns
            -------

            Raises
            ------
        '''
        """
            Gets the boto client for parameter store
            and tests the value of various parameters
        """
        ssm_client = get_boto_clients('ssm')

        logging.info("Got the boto client for ssm")
        """
            Iterating over each key/value in the dict
            to compare parameter store values
        """
        for ssm_name in parameter_dict.keys():

            logging.info("Comparing the following parameter: ")
            logging.info(ssm_name)
            logging.info(parameter_dict[ssm_name])

            """
                Gets the parameter value
                And tests to make sure it is not the
                same as the Value provided for the test
                as that is presumably the default value

                That should be overriden at build time
            """
            ssm_value = ssm_client.get_parameter(
                Name=ssm_name
            )
            self.assertNotEqual(
                ssm_value['Parameter']['Value'],
                parameter_dict[ssm_name]
             )

            logging.info("To this ssm value: ")
            logging.info(ssm_value)

if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    args = parser.parse_args()

    print(args.integers)
    '''
    unittest.main()
