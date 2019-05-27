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

#makes an output bucket for dev and prod Builds
aws s3 mb s3://codebuild-dev-sneakpeek

aws s3 mb s3://codebuild-prod-sneakpeek

#create a code build project with the formatted json input
aws codebuild create-project --cli-input-json file://util/dev_build_template.json

#start a code build project
aws codebuild start-build --project-name dev-sneekpeek --source-version dev

#check the code build project status
aws codebuild batch-get-builds --ids
