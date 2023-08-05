#!/usr/bin/env python
from __future__ import print_function
from pylambda.lambda_local import Lambda
from pylambda.deploy import LambdaDeploy
import argparse
import os
import time
import math

parser = argparse.ArgumentParser(description="Run an AWS Lambda function locally.")
subparsers = parser.add_subparsers()

# Parser for the run command
parser_run = subparsers.add_parser("run", help="Runs the local lambda function.")
parser_run.add_argument("file", type=str,
                    help="the file containing your lambda function.")
parser_run.add_argument("-e", "--event", type=str, default=None,
                    help="the json containing the event data. Default None.")
parser_run.add_argument("-n", "--name", type=str, default="handler",
                    help="the name of the method lambda should call. Default 'handler'")

# Parser for the deploy command
parser_deploy = subparsers.add_parser("deploy", help="Deploys the lambda function to S3 as a zip. MUST BE run from within the directory containing the lambda function.")
parser_deploy.add_argument("directory", type=str,
                    help="Directory path to ZIP. Required.")
parser_deploy.add_argument("s3_bucket", type=str,
                    help="the s3 bucket location. IE: s3://my_bucket/my_subfolder/")
parser_deploy.add_argument("-n", "--name", type=str, default=None,
                    help="Name of zipped file. Defaults to 'my_lambda_function'.")

def main():
    args = parser.parse_args()
    args = vars(args)

    # Decide if runnning or deploying
    if "s3_bucket" in args:
        d = LambdaDeploy(args["directory"], args["s3_bucket"], args["name"])
        d.deploy()
    elif "file" in args:
        print("\r\nRunning AWS Lambda Function...")
        test_lambda = Lambda(args["file"], args["event"], args["name"])

        print("\r\nReturn Value:")
        start_time = time.time()
        print(test_lambda.run())
        total_time = (time.time() - start_time) * 1000
        print("\r\nEstimated Runtime: " + str(total_time) + " ms")

        bill_duration = int(math.ceil(total_time / 100.0)) * 100
        print("Estimated Bill Duration: " + str(bill_duration) + " ms")
    else:
        print("Invalid arguments encountered. Please use -h to see help.")

if __name__ == '__main__':
    main()
