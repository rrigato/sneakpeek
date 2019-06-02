################################
#Used to create development repository
#Unit tests are run on each commit
#
#This script only needs to be run once
###############################

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
aws cloudformation create-stack --stack-name sneakpeak-pipeline \
 --template-body file://templates/code_pipeline.yml \
 --capabilities CAPABILITY_NAMED_IAM


#makes an output bucket for dev and prod Builds
aws s3 mb s3://codebuild-prod-sneakpeek

#start a code build project
aws codebuild start-build --project-name dev-sneekpeek-tests --source-version dev

#check the code build project status
aws codebuild batch-get-builds --ids dev-sneekpeek:8eb0b978-ae31-444c-bbeb-14ccdd4defa8
