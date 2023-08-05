import unittest2 as unittest
from pylambda import Lambda
import os

class Test_AWS_Lambda(unittest.TestCase):
    """
    Test class for local lambda service.
    """

    def test_create_success(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), None, "handler")
            test_lambda_2 = Lambda(os.path.join(path, "test", "fake_lambda.py"), os.path.join(path, "test", "event.json"), "handler")

            self.assertTrue(test_lambda_2.event["event1"] == "1", "Did not load event json!")
        except Exception as e:
            print(e)
            self.assertTrue(False, "Unable to create!")

    def test_none_file_argument(self):
        try:
            test_lambda = Lambda(None, None, "handler")
            self.assertTrue(False, "Created a Lambda with a None file!")
        except ValueError as e:
            pass

    def test_bad_type_file_argument(self):
        try:
            test_lambda = Lambda(123, None, "handler")
            self.assertTrue(False, "Created a Lambda with a int type file name!")
        except ValueError as e:
            pass

    def test_empty_file_argument(self):
        try:
            test_lambda = Lambda("", None, "handler")
            self.assertTrue(False, "Created a Lambda with an empty string!")
        except ValueError as e:
            pass

    def test_bad_file_type_argument(self):
        try:
            test_lambda = Lambda("bad.txt", None, "handler")
            self.assertTrue(False, "Created a Lambda with a non .py file!")
        except ValueError as e:
            pass

    def test_bad_type_event_argument(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), 123, "handler")
            self.assertTrue(False, "Created a Lambda with a int event")
        except ValueError as e:
            pass

    def test_empty_event_argument(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), "", "handler")
            self.assertTrue(False, "Created a Lambda with an empty string event file path!")
        except ValueError as e:
            pass

    def test_bad_file_type_argument(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), "event.txt", "handler")
            self.assertTrue(False, "Created a Lambda with a non .json event file!")
        except ValueError as e:
            pass

    def test_none_handler_argument(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), None, None)
            self.assertTrue(False, "Created a Lambda without a handler!")
        except ValueError as e:
            pass

    def test_empty_handler_argument(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), None, "")
            self.assertTrue(False, "Created a Lambda with an empty handler!")
        except ValueError as e:
            pass

    def test_bad_type_handler_argument(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), None, 123)
            self.assertTrue(False, "Created a Lambda with a int type handler!")
        except ValueError as e:
            pass

    def test_non_existent_handler_argument(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), None, "asdasd")
            self.assertTrue(False, "Created a Lambda with a non existent handler!")
        except AttributeError as e:
            pass

    def test_non_existent_lambda_file(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake.py"), None, "handler")
            self.assertTrue(False, "Created a Lambda with a non existent lambda file!")
        except IOError as e:
            pass

    def test_non_existent_event_file(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), os.path.join(path, "test", "eventaaaa.json"), "handler")
            self.assertTrue(False, "Created a Lambda with a non existent lambda file!")
        except IOError as e:
            pass

    def test_run_lambda_success(self):
        try:
            path = os.getcwd()
            test_lambda = Lambda(os.path.join(path, "test", "fake_lambda.py"), os.path.join(path, "test", "event.json"), "handler")
            result = test_lambda.run()

            self.assertTrue(type(result) is dict, "Lambda result was not a dict object!")
            self.assertTrue(len(result) == 3, "Incorrect number of results returned!")
            self.assertTrue(("event1" in result) and ("event2" in result) and ("event3" in result),
                            "Returned result does not have correct keys!")
            self.assertTrue(result["event1"] == "1" and result["event2"] == "2" and result["event3"] == "3",
                            "Returned result has the wrong values!")
        except Exception as e:
            print(e)
            self.assertTrue(False, "An unexpected error occurred!")
