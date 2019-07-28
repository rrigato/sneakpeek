"""
The purpose of this script is to wait until the
The cloudformation stack is created and complete
"""
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
        parser : argparse.ArgumentParser
            Returns what the program enters as args
            to the command line

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


def main():
    '''Main function for script
        Parameters
        ----------


        Returns
        -------


        Raises
        ------
    '''
    pass
if __name__ == '__main__':
    cf_stacks = define_parser()
    for aws_stack in cf_stacks:
        print(aws_stack)

    cf_checker = get_boto_clients('cloudformation')
    cf_waiter = cf_checker.get_waiter('stack_create_complete')
    cf_waiter.wait(StackName=cf_stacks[0],
        WaiterConfig={
            'Delay': 5,
            'MaxAttempts': 25
        })
