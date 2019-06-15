import boto3
import json

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

        Returns
        -------

        Raises
        ------
    '''
    """
        the Outputs section of the describe_stacks api
        call returns a list of dicts

        Each dict has a key which is the output name of 'OutputKey'
        And a key for the output value of OutputValue which is
        the outputs value
    """
    for output in output_values:
        if output['OutputKey'] == 'UserPoolClientId':
            print('UserPoolClientId: ' + output['OutputValue'])
        elif output['OutputKey'] == 'UserPoolId':
            print('UserPoolId: ' + output['OutputValue'])

def populate_json(json_key, json_value):
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
    iterate_outputs(output_values = cf_response['Outputs'])

main()
