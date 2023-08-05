Python AWS Local Lambda
=======================
Easily test and deploy your AWS Lambda function.

**Requirements**

* Python 2.7.x
* pip
* AWS CLI
* AWS Account (For deploying)

Since AWS currently only supports Python 2.7, you must ensure your function is tested and working in Python 2.7 before deploying.

**Installation**

Installation should be done using pip: ``pip install pylambda``

Once installed, make sure you setup the AWS CLI by following: http://docs.aws.amazon.com/cli/latest/userguide/installing.html


**Getting Started**

Once installed you can run pylambda from the console.

Run ``pylambda -h`` to see help options.

**Running Your Lambda**

To run your lambda function, use the following command:

``pylambda run my_lambda_function.py -e event.json -n handler``

* my_lambda_function.py = The python file containing your lambda function.
* event.json = The json event sent to your python function. See http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
* handler = The name of the function that lambda should call. The event.json is passed to this function if provided.

Arguments:

* file : the name of the python file that contains the lambda function. REQUIRED
* -e, --event : the json file that contains the event data. Must be a parsable json file. OPTIONAL
* -n, --name : the name of the function that should be called by lambda. Default 'handler'. OPTIONAL

**Deploying to S3**

To deploy your code as a zip to S3 navigate to the folder where your lambda function is contained and run:

``pylambda deploy my_lambda_directory_path s3://mybucket -n my_lambda_function``

* my_lambda_directory_path = The path to the directory that contains your lambda function and requirements.txt file.
* s3://mybucket = The location of your S3 bucket. This should follow the AWS CLI for S3 locations.
* my_lambda_function = The name of the zip file.

*NOTE: you must have a proper requirements.txt within the same folder as your lambda function if you are using external libraries installed with pip. The deploy functionality will automatically bundle in these dependencies before uploading.*

Arguments:

* directory : the directory path that contains your lambda.
* s3_bucket : the location of your S3 bucket. Must follow the AWS CLI format. REQUIRED
* -n, --name : the name of the zip file that will be uploaded to S3.


