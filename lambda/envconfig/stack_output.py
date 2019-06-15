import boto3
import json
import logging
import os

WORKING_DIRECTORY = os.getcwd()
logging.basicConfig(
filename=os.path.join(WORKING_DIRECTORY, 'logs/',
os.path.basename(__file__)),
format='%(asctime)s %(message)s',
 datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

def describe_stacks_response(stack_name):
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
    cf_client = boto3.client('cloudformation')
    """
        , =unpacks the list as a dictionary for searching
    """
    cf_response, = cf_client.describe_stacks(
        StackName=stack_name)['Stacks']

    return (cf_response)

def iterate_outputs(output_values):
    '''Iterates over every OutputKey for the stack

        Parameters
        ----------
        output_values : dict
            dict of output value from the cloudformation stack

        Returns
        -------
        output_dict : dict
            dict of values for UserPoolId and UserPoolClientId

        Raises
        ------
    '''
    output_dict = {}
    """
        the Outputs section of the describe_stacks api
        call returns a list of dicts

        Each dict has a key which is the output name of 'OutputKey'
        And a key for the output value of OutputValue which is
        the outputs value
    """
    for output in output_values:
        if output['OutputKey'] == 'UserPoolClientId':
            output_dict['UserPoolClientId'] = output['OutputValue']

        elif output['OutputKey'] == 'UserPoolId':
            output_dict['UserPoolId'] = output['OutputValue']

    print(output_dict)
    return(output_dict)

def populate_json(input_dict):
    '''Populates cognito_config.json file

        Parameters
        ----------
        input_dict : str
            input dict that needs to be applied to json

        Returns
        -------

        Raises
        ------
    '''
    import pdb; pdb.set_trace()

def main():
    '''Entry point into the script
        Parameters
        ----------

        Returns
        -------

        Raises
        ------
    '''
    cf_response = describe_stacks_response(
            stack_name='cognito-prod-sneakpeek'
            )
    import pdb; pdb.set_trace()
    iterate_outputs(output_values = cf_response['Outputs'])

main()
