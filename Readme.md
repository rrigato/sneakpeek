![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiZnR3cHhDRFhrcWYyMGNrRGoyeXkzZDFjbm05MVlIcDBPZktxV01Fc2RtTFJ2V1N6aHQ5Q1cwUlF6Nlp2ZkNzODEwY3RzUkxSSEpVRjYydnJkQzJDcHMwPSIsIml2UGFyYW1ldGVyU3BlYyI6Ikd6dDNtRmp3T21iSmZTdkIiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=dev)

Serverless project used to build a web application to
detect trailer utilization from an uploaded image

### Code Pipeline Deployment process

Below is a high level description of the automated CI/CD pipeline:

1) When new code is pushed to the dev branch this triggers a code pipeline revision

2) Multiple cloudformation stacks will be spun up to enable a clean environment that replicates production


3) Any build errors that occur testing on this qa environment will halt the pipeline before any changes are made to production

![QA Code Build Failes](devops/images/pipeline_demo_3.jpg "Title")


4) Once all unit tests are passed the qa environment cloudformation stacks are deleted and the changes are migrated to production. Code Build tests are run on prod and once successfully passed the changes are merged into the master branch

### Project Directory Overview
#### cfn-lint (cloudformation Linting)
[cfn-lint](https://github.com/aws-cloudformation/cfn-python-lint.git) Provides yaml/json cloudformation validation and checks for best practices

- Install

```
    pip install cfn-lint
```

- Run on a file
```
    cfn-lint <filename.yml>

    cfn-lint templates/code_pipeline.yml
```

- Run on all files in Directory
```
    cfn-lint templates/*.yml
```


#### Git Secrets Scan

[git secrets](https://github.com/awslabs/git-secrets.git) is a command line utility for validating that you do not have any git credentials stored in your git repo commit history

This is useful for not only open source projects, but also to make sure best practices are being followed with limited duration credentials (IAM roles) instead of long term access keys

- Global install

```
    git init

    git remote add origin https://github.com/awslabs/git-secrets.git

    git fetch origin

    git merge origin/master

    sudo make install
```

- Web Hook install

Configuring git secrets as a web hook will ensure that git secrets runs on every commit, scanning for credentials
```
    cd ~/Documents/sneakpeek

    git secrets --install

    git secrets --register-aws
```


- Run a git secrets check recursively on all files in directory

```
git secrets --scan -r .
```


### Project Directory Overview
Provides information on each directory/ source file

#### builds

##### py
    Directory for custom python scripts that setup build configuration
- buildspec_dev.yml = Buildspec to use for the development (QA)
    CodeBuild project

- buildspec_prod.yml = Buildspec to use for the prod deployment CodeBuild project

#### devops
- CI.sh = Establishes CodeCommit Repo and CodeBuild Project
    - For debugging errors go to the Phase details section of the console
    - Or use the batch-get-builds command in the aws cli

#### lambda
- Used to build lambda functions
- Note that each folder can be bundled into a deployment package if it has a dependency other than the standard template libraries or the aws sdk (Boto3)

- Deployment packages = zip archive with lambda function code and dependencies

More on deployment packages can be found here:

https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html


It may be best practice to bundle deployments using code build, as some of the compiled C dependencies may not transfer over on your local even if you are running linux

For example I have had issues in the past with installing pandas on ubuntu, bundling and trying to use in a lambda function.

-t tells pip to install function locally
```
    cd lambda/<project>

    pip install -r requirements.txt -t .


```

#### logs
- directory for python log files

#### models
- directory for image classification models

#### static
- css = static stylesheet files for web application
- fonts = static fonts to use for web application
- js = static javascript files for web application
- images = static images for web applications
- index.html = homepage for web applciation

#### templates

- backend.yml = dynamodb, lambda, and api gateway resources

- code_pipeline.yml = Creates CodeBuild/Code Pipeline resources
    necessary for Dev/Prod

- code_pipeline_iam.yml = nested stack for code_pipeline.yml contains iam resources that are used by code_pipeline.yml

Make sure to run the following command before creating a stack with code_pipeline.yml

```
aws s3 cp ./templates s3://sneakpeek-nested-stack --recursive     --exclude "demo*"
```

The reason being that a nested stack has to be in an s3 bucket to be used by the parent

- cognito.yml = user pool and client id to be used for authentication in the webpage

- static_webpage.yml = builds the S3 bucket enabled for web hosting

#### tests
- test_dev_aws_resources.py = after the dev environment is spun up in the CodeBuild project for builds/buildspec_dev.yml this script is run to validate deployment of resources.

If any of the test cases fail, the Pipeline stops before deploying to prod


- test_prod_aws_resources.py = test cases run after the prod environment is spun up in the CodeBuild project for builds/buildspec_prod.yml

#### static

- dev_build_template.json = codeBuild project definition for devops/CI.sh


- dev_config.json = Name of the bucket to pass to templates/static_webpage.yml must be array

- dev_prod.json = Provides production configuration variables

- prod_backend_template_config.json = configuration file for cloudformation template that passes in parameters to the templates/backend.yml cloudformation script for production

#### Setup Continuous Integration
Run the devops/CI.sh shell script to create CodeCommit
Repo and CodeBuild Continuous Integration/Build client once

Create a Code Commit repository and add that repository as a remote

```
git init

git remote add origin <origin_url_or_ssh>

```


Fetch origin repo locally and merge if the remote

has any references you do not

```
    git fetch origin

    git merge origin/<branch_name>
```



#### Setup Infrastructure
Run the


```
aws cloudformation create-stack --template-file ~/Documents/sneakpeek/templates/static_webpage.yaml --stack-name sneakpeek --capabilities CAPABILITY_IAM \
--parameter-overrides BucketName="dev-sneakpeek"
```
