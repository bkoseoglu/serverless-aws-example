This is an example of aws serverless architecure. 
--------------------------------------------------------

Environment variables and plugings required for successful deployment are in serverless.yml
In order to deploy the code on local machine run the following in 2 seperate command lines.

sls wsgi serve

sls dynamodb start --migrate

The former is wsgi plugin, which sets the local environment IS_OFFLINE and lets you run code locally. 
The latter provides a local dynamodb, which uses no sql.

In order to run the same code on aws, run the following

sls deploy