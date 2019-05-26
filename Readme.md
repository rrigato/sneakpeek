Serverless project used to build a web application to
detect trailer numbers on a trailer

####Project Directory Overview
######devops
- CI.sh = Establishes CodeCommit Repo and CodeBuild Project

######static
- css = static stylesheet files for web application
- fonts = static fonts to use for web application

####Setup Continuous Integration
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



####Setup Infrastructure
Run the


```
aws cloudformation deploy --template-file ~/Documents/sneakpeek/templates/static_webpage.yaml --stack-name SneekPeek --capabilities CAPABILITY_IAM \
--parameter-overrides BucketName="dev-sneekpeek"
```
