![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidkVnSCs4SHNIdmNMREQ4NW9VNk8xaC9zeWNLQkpYaGVqZnM1K0kyQXZpWlE5Z0ZpclRSSElWa29hTFRQVm45NHNkUlFpcTcwbkFNUlc5WDI0d1N5VXNrPSIsIml2UGFyYW1ldGVyU3BlYyI6IjJnY3pJRjVnNkZ2UVJyM2wiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=dev)

Serverless project used to build a web application to
detect trailer numbers on a trailer

### Project Directory Overview
Provides information on each directory/ source file

#### builds
- buildspec_dev.yml = Buildspec to use for the development (QA)
    CodeBuild project

- buildspec_prod.yml = Buildspec to use for the prod deployment CodeBuild project

#### devops
- CI.sh = Establishes CodeCommit Repo and CodeBuild Project
    - For debugging errors go to the Phase details section of the console
    - Or use the batch-get-builds command in the aws cli
#### static
- css = static stylesheet files for web application
- fonts = static fonts to use for web application
- js = static javascript files for web application
- images = static images for web applications
- index.html = homepage for web applciation

#### templates
- static_webpage.yml = builds the S3 bucket enabled for web hosting

#### tests
- test_aws_resources.py = tests that the underlying aws resources were successfully created


#### static
- dev_config.json = Name of the bucket to pass to templates/static_webpage.yml

- dev_build_template.json = codeBuild project definition for devops/CI.sh

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
aws cloudformation deploy --template-file ~/Documents/sneakpeek/templates/static_webpage.yaml --stack-name SneekPeek --capabilities CAPABILITY_IAM \
--parameter-overrides BucketName="dev-sneekpeek"
```
