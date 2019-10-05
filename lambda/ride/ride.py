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
        boto_client : boto3
            python 3 boto client for aws resource
            resource_name in region region_name


        Raises
        ------
    '''
    logging.info("Got the following boto client: ")
    logging.info(resource_name)

    return(boto3.client(resource_name, region_name))


def respond(err, res=None):
    '''Sets http headers returns dict for response

        Note the required fields needed for a lambda
        proxy integration here:

        Must be in order
        https://aws.amazon.com/premiumsupport/knowledge-center/malformed-502-api-gateway/

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
    return ({
        'isBase64Encoded': False,
        'statusCode': '400' if err else '201',
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': err.message if err else json.dumps(res),
    })

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

def scan_load_table(boto_client, table_name):
    '''Returns all items in dynamodb db load table

        Parameters
        ----------
        boto_client : boto3
            python 3 boto client for dynamodb

        table_name : str
            name of the dynamodb table

        Returns
        -------
        all_items : list
            List where each element is a dict referring to
            an item

        Raises
        ------
    '''
    """
        Querying all attributes in a the dynamo table
    """
    all_items = boto_client.scan(
        TableName=table_name,
        Select='ALL_ATTRIBUTES'
    )
    logging.info("DynamoDB load table scan results")
    logging.info(all_items)

    return(all_items['Items'])

def determine_environment(context):
    '''Determines whether lambda is in prod or not

        Parameters
        ----------
        context : dict
            Contains metadata involving python call,
            Full list of environment variables available here:
            https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

        Returns
        -------
        ENVIRON_NAME : str
            'prod' or 'dev' depending on the environment

        Raises
        ------
        ValueError
            Raises a value error if prod or dev
            are not included

    '''
    """
        Raises an assertion error if it is
        unable to find the correct environment
    """
    ENVIRON_NAME = None
    if 'dev' in context.function_name:
        logging.info("dev function")
        ENVIRON_NAME = 'dev'
    if 'prod' in context.function_name:
        logging.info("prod function")
        ENVIRON_NAME = 'prod'
    if ENVIRON_NAME is None:
        raise( ValueError("Unable to determine environment"))

    return(ENVIRON_NAME)


def get_table_name(environ_name):
    '''Gets the table name from the ssm parameter store

        Parameters
        ----------
        environ_name : str
            'prod' or 'dev' depending on the environment

        Returns
        -------
        ddb_table_name : str
            Name of the dynamo db table that
            contains image output results

        Raises
        ------


    '''
    ssm_client = get_boto_clients(resource_name='ssm')

    logging.info("Got ssm client")

    """
        Forms the fully qualified path to
        the name of the parameter.

        Example:
        /dev/DynamoTableName
    """
    ddb_table_name = ssm_client.get_parameter(
        Name = "/" + environ_name + "/BucketName")

    logging.info("Dynamo Db table name ssm parameter response: ")
    logging.info(ddb_table_name)

    return(ddb_table_name['Parameter']['Value'])



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

    logging.info("Received event: " + json.dumps(event, indent=2))


    ENVIRON_NAME = determine_environment(context)
    """
        Creates dynamodb resource and
        puts an item in the table
    """
    dynamo_client = get_boto_clients(resource_name='dynamodb',
    region_name='us-east-1')


    ddb_table_name = get_table_name(
        environ_name=ENVIRON_NAME)
    #to-do figure out how to pass table name
    #for different environments

    all_items = scan_load_table(boto_client=dynamo_client,
    table_name = ENVIRON_NAME + '-sneakpeek-table')


    return (respond(err=None, res=
        {"RideId": "SvLnijIAtg6inAFUBRT+Fg==",
        "Unicorn":
        {"Name":"Rocinante","Color":"Yellow","Gender":"Female"},"Eta":"30 seconds"
        }))

# if __name__ == '__main__':
#     """Local testing
#     """
#     class Context(object):
#         pass
#     context = Context()
#     context.function_name = 'dev'
#     lambda_handler(event="hello",context = context)
