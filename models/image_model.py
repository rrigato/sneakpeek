import boto3

class utilization:
    '''Image Classification Model for trailer utilization
    '''
    def __init__:
        '''
        '''

def get_logger(self):
    '''Returns a logging instance for the script
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
