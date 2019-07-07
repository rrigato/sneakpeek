import boto3
import logging
import os

class utilization:
    '''Image Classification Model for trailer utilization
    '''
    def __init__(self):
        '''Initializes the trailer utilization model
        '''
        self.get_logger()

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
            filename=os.path.join(".", 'logs/',
            os.path.basename(__file__).split('.')[0]),
            format='%(asctime)s %(message)s',
             datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG
             )
        logging.info('\n')

def main():
    '''
        Parameters
        ----------

        Returns
        -------

        Raises
        ------
    '''
    model_build = utilization()

if __name__ == "__main__":
    main()
