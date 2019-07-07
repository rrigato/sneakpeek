from sagemaker import get_execution_role
from sagemaker.amazon.amazon_estimator import get_image_uri

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

    def setup_notebook(self, s3_bucket):
        '''Sets up jupyter notebook instance

            Parameters
            ----------
            s3_bucket : str
                Name of s3 bucket where images are stored in
                Apache MXNET recordIO format

            Returns
            -------

            Raises
            ------
        '''
        role = get_execution_role()

        bucket=s3_bucket

        training_image = get_image_uri(
            boto3.Session().region_name, 'image-classification'
            )

train_file = 'balanced_by_class_20_256_size.rec'
val_file = 'all_images_256_size.rec'
# The algorithm supports multiple network depth (number of layers). They are 18, 34, 50, 101, 152 and 200
# For this training, we will use 18 layers
num_layers = "18"
# we need to specify the input image shape for the training data
image_shape = "3,224,224"
# we also need to specify the number of training samples in the training set
# for caltech it is 15420
num_training_samples = "80"
# specify the number of output classes
num_classes = "4"
# batch size for training
mini_batch_size =  "64"
# number of epochs
epochs = "2"
# learning rate
learning_rate = "0.01"

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
