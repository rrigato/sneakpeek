from sagemaker import get_execution_role
from sagemaker.amazon.amazon_estimator import get_image_uri
from time import gmtime, strftime

import boto3
import logging
import os
import time





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

        '''
            Docker container image that has a built in amazon
            sagemaker model for image classification
        '''
        training_image = get_image_uri(
            boto3.Session().region_name, 'image-classification'
            )

role = get_execution_role()

s3_bucket='image-class-repo'

bucket=s3_bucket

'''
    Docker container image that has a built in amazon
    sagemaker model for image classification
'''
training_image = get_image_uri(
    boto3.Session().region_name, 'image-classification'
    )



# s3_train_key = 'train_balanced_by_class_15_resize_256.rec'
# s3_validation_key = 'val_balanced_by_class_15_resize_256.rec'
s3_train_key = 'train'
s3_validation_key = 'validation'
# The algorithm supports multiple network depth (number of layers). They are 18, 34, 50, 101, 152 and 200
# For this training, we will use 18 layers
num_layers = "34"
# we need to specify the input image shape for the training data
image_shape = "3,256,256"
# we also need to specify the number of training samples in the training set
# for caltech it is 15420
num_training_samples = "80"
# specify the number of output classes
num_classes = "4"
# batch size for training
mini_batch_size =  "16"
# number of epochs
epochs = "10"
# learning rate
learning_rate = "0.01"

"""
    Formatting arn for train/validation
"""
s3_train = 's3://{}/{}/'.format(bucket, s3_train_key)
s3_validation = 's3://{}/{}/'.format(bucket, s3_validation_key)


s3 = boto3.client('s3')
# create unique job name
job_name_prefix = 'model-34layers-10epochs'
timestamp = time.strftime('-%Y-%m-%d-%H-%M-%S', time.gmtime())
job_name = job_name_prefix + timestamp
training_params = \
{
    # specify the training docker image
    "AlgorithmSpecification": {
        "TrainingImage": training_image,
        "TrainingInputMode": "File"
    },
    "RoleArn": role,
    "OutputDataConfig": {
        "S3OutputPath": 's3://{}/{}/output'.format(bucket, job_name_prefix)
    },
    "ResourceConfig": {
        "InstanceCount": 1,
        "InstanceType": "ml.p2.xlarge",
        "VolumeSizeInGB": 50
    },
    "TrainingJobName": job_name,
    "HyperParameters": {
        "image_shape": image_shape,
        "num_layers": str(num_layers),
        "num_training_samples": str(num_training_samples),
        "num_classes": str(num_classes),
        "mini_batch_size": str(mini_batch_size),
        "epochs": str(epochs),
        "learning_rate": str(learning_rate)
    },
    "StoppingCondition": {
        "MaxRuntimeInSeconds": 3600
    },
#Training data should be inside a subdirectory called "train"
#Validation data should be inside a subdirectory called "validation"
#The algorithm currently only supports fullyreplicated model (where data is copied onto each machine)
    "InputDataConfig": [
        {
            "ChannelName": "train",
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": s3_train,
                    "S3DataDistributionType": "FullyReplicated"
                }
            },
            "ContentType": "application/x-recordio",
            "CompressionType": "None"
        },
        {
            "ChannelName": "validation",
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": s3_validation,
                    "S3DataDistributionType": "FullyReplicated"
                }
            },
            "ContentType": "application/x-recordio",
            "CompressionType": "None"
        }
    ]
}
print('Training job name: {}'.format(job_name))
print('\nInput Data Location: {}'.format(training_params['InputDataConfig'][0]['DataSource']['S3DataSource']))

# create the Amazon SageMaker training job
sagemaker = boto3.client(service_name='sagemaker')
sagemaker.create_training_job(**training_params)


# confirm that the training job has started
status = sagemaker.describe_training_job(TrainingJobName=job_name)
print('Training job current status: {}'.format(status))

########################
#Writes model output
#
#
########################
import datetime
import json
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

with open('15_4_10epoch_34layers_results.json', 'w') as fp:
    json.dump(status, fp, default=datetime_handler)
#json.dumps(status, default=datetime_handler)

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

    utilization.setup_notebook(s3_bucket='image-class-repo-sagemaker')
if __name__ == "__main__":
    main()
