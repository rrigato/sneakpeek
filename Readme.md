Serverless project used to build a web application to
detect trailer numbers on a trailer


###Setup Infrastructure
Create an S3 bucket

```
aws s3 mb s3://dev-sneekpeek
```


```
aws cloudformation deploy --template-file ~/Documents/sneakpeek/templates/static_webpage.yaml --stack-name SneekPeek --capabilities CAPABILITY_IAM \
--parameter-overrides BucketName="dev-sneekpeek"
```
