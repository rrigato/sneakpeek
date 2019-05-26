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

aws codebuild create-project --cli-input-json file://util/dev_build_template.json


aws codebuild start-build --project-name dev-sneekpeek --source-version dev
