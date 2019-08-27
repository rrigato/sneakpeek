import boto3
import json
import logging
print('Loading function')
dynamo = boto3.client('dynamodb')

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


def respond(err, res=None):
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
    get_boto_clients(resource='s3')
    import pdb; pdb.set_trace()

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

    write_to_s3_output()
    return (respond(err=None, res=
        {"RideId": "SvLnijIAtg6inAFUBRT+Fg==",
        "Unicorn":
        {"Name":"Rocinante","Color":"Yellow","Gender":"Female"},"Eta":"30 seconds"
        }))
