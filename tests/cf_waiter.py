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
        description='Process some integers.'
        )
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                       help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                       const=sum, default=max,
                       help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))

def main():
    '''Main function for script
        Parameters
        ----------


        Returns
        -------


        Raises
        ------
    '''
if __name__ == '__main__':
    define_parser()
