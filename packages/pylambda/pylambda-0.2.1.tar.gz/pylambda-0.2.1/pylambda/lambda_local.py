from __future__ import print_function
import os.path
import json
import imp
import os

class Lambda(object):
    """
    Class for simulating AWS Lambda call.
    """
    def __init__(self, file_path, event, method):
        """
        Creates a new Lambda.

        Params:
        -------
        file_path : str
            Python file containing the lambda functionality.
        event : str
            JSON file containing the mappings for event data for the lambda function.
        method : str
            The method lambda should call.
        """
        self.file_path = file_path
        self.event = event
        self.method = method
        self.imports = []

        self.__initialize()

    def __initialize(self):
        """
        Initializes that lambda function, ensuring arguments are correct.

        Throws ValueError OR IOError for bad arguments/file paths.
        """
        if self.file_path is None or type(self.file_path) is not str or self.file_path == "" or self.file_path.find(".py") == -1:
            raise ValueError("-f should contain the file path to the lambda function. Example: index.py")

        if self.event is not None and (type(self.event) is not str or self.event == "" or self.event.find(".json") == -1):
            raise ValueError("-e should contain the file path to the event json. Example: event.json")

        if self.method != "handler" and (type(self.method) is not str or self.method == ""):
            raise ValueError("-n should contain a valid method name for the lambda method. Example: 'handler'")

        if not os.path.isfile(self.file_path):
            raise IOError("Unable to locate the lambda file! Path checked: " + self.file_path)

        if self.event is not None and not os.path.isfile(self.event):
            raise IOError("Unable to locate the json file! Path checked: " + self.event)

        # Import the event data
        if self.event is not None:
            tmp = {}
            with open(self.event, "r") as event_file:
                tmp = json.load(event_file)

            self.event = tmp

        # Load the module and function
        i = imp.load_source("index", self.file_path)
        method = getattr(i, self.method)
        self.method = method

    def run(self):
        """
        Returns the result of the Lambda function.

        Raises any/all exceptions caused by the lambda function.
        """
        return self.method(self.event, Context())


class Context(object):
    """
    Context object for AWS Lambda.

    Includes basic functionality for simulating context in lambda.
    """
    def __init__(self):
        """
        Creates a basic context object based on AWS context.

        See: http://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
        """
        self.function_name = "local_lambda_func"
        self.function_version = "1.0"
        self.invoked_function_arn = "NULL"
        self.memory_limit_in_mb = "UNKNOWN"
        self.aws_request_id = "-1"
        self.log_group_name = "NONE"
        self.log_stream_name = "NONE"
        self.identity = None
        self.client_context = None

    def get_remaining_time_in_millis():
        return 10000000
