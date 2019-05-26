################################
#Used to create development repository
#Unit tests are run on each commit
#
#This script only needs to be run once
###############################

#note that the cli user needs to have https for username/password setup
#or ssh public key uploaded to codecommit
aws codecommit create-repository --repository-name sneakpeek
