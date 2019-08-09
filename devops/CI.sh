################################
#Used to create development repository
#Unit tests are run on each commit
#
#This script only needs to be run once
###############################

#bucket used for nested stacks
#excludes all templates that start with demo
aws s3 mb sneakpeek-nested-stack


aws s3 cp ./templates s3://sneakpeek-nested-stack --recursive \
    --exclude "demo*"


#note that the cli user needs to have https for username/password setup
#or ssh public key uploaded to codecommit
aws codecommit create-repository --repository-name sneakpeek

#get the arn for the repository
aws codecommit get-repository --repository-name sneakpeek \
--query 'repositoryMetadata.Arn'

#get the https for the repository
aws codecommit get-repository --repository-name sneakpeek \
--query 'repositoryMetadata.cloneUrlHttp'

#Creates the CodeBuild and Code Pipeline Cloudformation stack
aws cloudformation create-change-set --stack-name sneakpeak-pipeline \
 --template-body file://templates/code_pipeline.yml \
 --change-set-name CodePipelineAddition \
 --capabilities CAPABILITY_NAMED_IAM
 #aws cloudformation execute-change-set --change-set-name
 #<change_set_arn>
aws cloudformation execute-change-set --change-set-name \
arn:aws:cloudformation:us-east-1:350255258796:changeSet/CodePipelineAddition/2326ac23-8154-49d4-a328-7edc708a2b53

#Update code pipeline
aws cloudformation update-stack --stack-name sneakpeek-pipeline \
 --template-body file://templates/code_pipeline.yml \
 --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND


##allows for much more detailed error logging for stack
#creation events
 aws cloudformation describe-stack-events --stack-name backend-prod-sneakpeek2 \
 > output2.json

#makes an output bucket for dev and prod Builds
aws s3 mb s3://codebuild-prod-sneakpeek

#start a code build project
aws codebuild start-build --project-name dev-sneakpeek-tests --source-version dev

#check the code build project status
aws codebuild batch-get-builds --ids dev-sneakpeek:8eb0b978-ae31-444c-bbeb-14ccdd4defa8
