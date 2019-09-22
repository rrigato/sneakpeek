import boto3
import json
import logging
import os

WORKING_DIRECTORY='.'
def get_logger():
    '''Adds basic logging

        Parameters
        ----------

        Returns
        -------

        Raises
        ------
    '''
    """
        Removes any basic logging configuration
        that may have been setup by the lambda container
    """
    default_lambda_logging = logging.getLogger()
    if default_lambda_logging.handlers:
        for handler in default_lambda_logging.handlers:
            default_lambda_logging.removeHandler(handler)

    """
        Configures logging formatting
    """
    logging.basicConfig(
        format='%(levelname)s - %(asctime)s %(message)s',
         datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO
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
    logging.info("Got the following boto client: ")
    logging.info(resource_name)

    return(boto3.client(resource_name, region_name))


def respond(err, res=None):
    '''Sets http headers returns dict for response

        Parameters
        ----------
        err : str
            Any errors encountered for the lambda call

        Returns
        -------
        http_response : dict
            The http response returned from
            the lamdba client

        Raises
        ------
    '''
    return {
        'statusCode': '400' if err else '201',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def write_to_s3_output():
    '''writes output csv to s3 bucket
        Parameters
        ----------

        Returns
        -------


        Raises
        ------
    '''
    get_boto_clients(resource_name='s3')

def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    get_logger()
    """
        Creates dynamodb resource and
        puts an item in the table
    """
    dynamo_client = get_boto_clients(resource_name='dynamodb',
    region_name='us-east-1')
    #print("Received event: " + json.dumps(event, indent=2))


    return (respond(err=None, res=
        {"RideId": "SvLnijIAtg6inAFUBRT+Fg==",
        "Unicorn":
        {"Name":"Rocinante","Color":"Yellow","Gender":"Female"},"Eta":"30 seconds"
        }))

if __name__ == '__main__':
    lambda_handler(event="hello",context = "world")
