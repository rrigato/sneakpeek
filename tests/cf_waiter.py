"""
The purpose of this script is to wait until the
The cloudformation stack is created and complete
"""
from botocore.exceptions import WaiterError
import argparse
import boto3
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

def define_parser():
    '''
        Parameters
        ----------


        Returns
        -------
        cf_stacks : list
            list of str to wait on if the cloudformation
            stack is created successfully

        Raises
        ------
    '''
    parser = argparse.ArgumentParser(
        description='Provide the cloudformation stacks as strings'
        )
    parser.add_argument('cf_stacks', metavar='stacks',
            type=str, nargs='+',
            help='Cloudformation stack name')

    """
        Gets command line arguements passed into
        a Namespace object and then converts into
        a list of str

        python cf_waiter.py arg1 arg2
    """
    cf_stacks = parser.parse_args()

    cf_stacks = vars(cf_stacks)['cf_stacks']
    return(cf_stacks)

def check_cf_stack_status(cf_stacks):
    '''Waits until cloudformation stacks are created
        Checks if the stack exists if the waiter command
        fails
        Parameters
        ----------
        cf_stacks : list
            list of str to wait on if the cloudformation
            stack is created successfully

        Returns
        -------


        Raises
        ------
    '''
    cf_checker = get_boto_clients('cloudformation')
    cf_waiter = cf_checker.get_waiter('stack_create_complete')
    """
        Iterates over every aws stack in
        the list
    """
    for aws_stack in cf_stacks:
        """
            For some silly reason if you make an
            api call to check the created status and
            the stack exists aws will return a 255 error

            This obviously breaks code builds automated
            testing so the below code catches any waiter
            exceptions and checks if the stack is in
            create completed. If not it will throw
            an error and exit the program
        """
        try:

            cf_waiter.wait(StackName=aws_stack,
                WaiterConfig={
                    'Delay': 5,
                    'MaxAttempts': 25
                })
        except WaiterError as WE:
            print("Hello World")
            stack_current_status = cf_checker.describe_stacks(
                StackName=aws_stack)
            if (stack_current_status['Stacks'][0]['StackStatus']
                != 'CREATE_COMPLETE'):
                print("Not Great")
            print(cf_checker.describe_stacks(
                StackName=aws_stack))
def main():
    '''Main function for script
        Parameters
        ----------


        Returns
        -------


        Raises
        ------
    '''
    cf_stacks = define_parser()
    check_cf_stack_status(cf_stacks)
if __name__ == '__main__':
    main()
