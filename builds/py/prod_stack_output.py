import boto3
import json
import logging
import os
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
    logging.info("Creating aws python client")
    cf_client = boto3.client('cloudformation')
    """
        , =unpacks the list as a dictionary for searching
    """
    cf_response, = cf_client.describe_stacks(
        StackName=stack_name)['Stacks']

    return (cf_response)

def iterate_outputs(output_values, output_key, input_dict):
    '''Iterates over every OutputKey for the stack

        Parameters
        ----------
        output_values : list
            list of dicts of output value from the cloudformation stack

        output_key : str
            The output name from the cloudformation stack we are
            trying to find

        input_dict : dict
            Dict that will be appended with new output_key
            and value

        Returns
        -------
        input_dict : dict
            dict of values for UserPoolId and UserPoolClientId

        Raises
        ------
    '''
    logging.info(input_dict)
    logging.info(output_key)

    logging.info("Begining list parse")
    """
        the Outputs section of the describe_stacks api
        call returns a list of dicts

        Each dict has a key which is the output name of 'OutputKey'
        And a key for the output value of OutputValue which is
        the outputs value
    """
    for output in output_values:
        if output['OutputKey'] == output_key:
            input_dict[output_key] = output['OutputValue']

    logging.info("Description of input key")
    logging.info(input_dict)
    return(input_dict)

def iterate_stack(cf_output_dict, cf_output_list,
    cf_response):
    '''Populates cognito_config.json file

        Parameters
        ----------
        cf_output_dict : dict
            Dict that needs to be appended with cloudformation
            output names and values

        cf_output_list : list
            List of cloudformation output names to
             iterate over

        cf_response : dict
            Json returned by the describe stacks api call

        Returns
        -------
        cf_output_dict : dict
            Dict where the key is the cloudformation
            output name and the value is the cloudformation
            output value

        Raises
        ------
    '''

    for cf_output in cf_output_list:
        """
            iterates over every output name in
            the list

        """
        logging.info("Processed cloudformation output value:")
        logging.info(cf_output)
        cf_output_dict = iterate_outputs(
                output_values = cf_response['Outputs'],
                output_key = cf_output,
                input_dict = cf_output_dict)

    return(cf_output_dict)


def populate_json(input_dict, webpage_config_dir):
    '''Populates cognito_config.json file

        Parameters
        ----------
        input_dict : dict
            input dict that needs to be applied to json

        webpage_config_dir : str
            Relative directory and file extension to json file
            When running CodeBuild this will populate the json file
            which will get pushed to s3

        Returns
        -------

        Raises
        ------
    '''
    with open(webpage_config_dir) as json_file:
        original_file = json.load(json_file)
    logging.info("Read in JSON from the following directory: ")
    logging.info(WORKING_DIRECTORY + webpage_config_dir)


    """
        Assigning fields based on queried output file
        And writing that json file to the web page static
        directory
    """
    original_file['cognito']['userPoolId'] = input_dict['UserPoolId']
    original_file['cognito']['userPoolClientId'] = (
        input_dict['UserPoolClientId'])


    original_file['cognito']['IdentityPoolId'] = (
        input_dict['IdentityPoolId'])

    original_file['cognito']['IdentityAuthorizedRoleArn'] = (
        input_dict['IdentityAuthorizedRoleArn'])

    logging.info("Assigned outputs from cloudformation template")

    with open(webpage_config_dir, 'w') as modified_config:
        json.dump(original_file, modified_config, indent=4)

    logging.info("Wrote the new cognito credientials to the config file")



def main():
    '''Entry point into the script
        Parameters
        ----------

        Returns
        -------

        Raises
        ------
    '''
    get_logger()
    cf_response = describe_stacks_response(
            stack_name='cognito-prod-sneakpeek'
            )
    cf_backend_response = describe_stacks_response(
            stack_name='backend-prod-sneakpeek'
            )

    output_dict = {}

    """
        Cloudformation outputs that need to be iterated over
    """
    cf_output_values = [
        'UserPoolClientId', 'UserPoolId',
        'IdentityAuthorizedRoleArn', 'IdentityPoolId'
    ]

    for cf_output in cf_output_values:
        """
            First getting output values from
            /templates/cognito.yml

            Then getting output values from
            /templates/backend.yml
        """
        logging.info("Processed cloudformation output value:")
        logging.info(cf_output)
        output_dict = iterate_outputs(
                output_values = cf_response['Outputs'],
                output_key = cf_output,
                input_dict = output_dict)


    """
        Populates the /static/js/cognito_config.json
        file
    """
    populate_json(input_dict=output_dict,
        webpage_config_dir="static/js/cognito_config.json")


main()
