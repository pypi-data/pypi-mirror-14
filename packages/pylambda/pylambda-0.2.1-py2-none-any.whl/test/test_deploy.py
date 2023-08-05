import unittest2 as unittest
from pylambda import LambdaDeploy
import os
from mock import patch, Mock

class Test_Deploy_Lambda(unittest.TestCase):
    """
    Test class for deploy to S3 for lambda.
    """

    def test_create_success(self):
        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(path, "s3://my_bucket", None)
            test_deploy_2 = LambdaDeploy(path, "s3://my_bucket", "test")

            self.assertTrue(test_deploy.directory == os.path.abspath(path), "Did not create full path for directory!")
            self.assertTrue(test_deploy.bucket == "s3://my_bucket", "Did not set correct s3 bucket!")
            self.assertTrue(test_deploy_2.name == "test", "Did not create name with 'test'!")
        except Exception as e:
            print(e)
            self.assertTrue(False, "Unable to create!")

    def test_create_fail_cwd(self):
        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(os.path.join(path, "asdasdasd", "asdasd"), "s3://my_bucket", None)
            self.assertTrue(False, "Created with bad directory!")
        except IOError as e:
            pass

        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy("", "s3://my_bucket", None)
            self.assertTrue(False, "Created with bad directory!")
        except ValueError as e:
            pass

        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(None, "s3://my_bucket", None)
            self.assertTrue(False, "Created with bad directory!")
        except ValueError as e:
            pass

        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(123, "s3://my_bucket", None)
            self.assertTrue(False, "Created with bad directory!")
        except ValueError as e:
            pass

    def test_create_fail_s3(self):
        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(path, "my_bucket", None)
            self.assertTrue(False, "Created with bad s3 format!")
        except ValueError as e:
            pass

        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(path, "", None)
            self.assertTrue(False, "Created with bad s3 format!")
        except ValueError as e:
            pass

        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(path, None, None)
            self.assertTrue(False, "Created with bad s3 format!")
        except ValueError as e:
            pass

        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(path, 123, None)
            self.assertTrue(False, "Created with bad s3 format!")
        except ValueError as e:
            pass

    @patch('subprocess.Popen') # Mocks the Popen object from subprocess
    @patch('shutil.make_archive') # Mocks the zip function
    def test_deploy_success(self, archive_func, popen_func):
        popen_mock = Mock()

        popen_attrs = {'wait.return_value': 0}
        popen_mock.configure_mock(**popen_attrs)
        popen_func.return_value = popen_mock

        shutil_attrs = {'make_archive.return_value': True}
        archive_func.configure_mock(**shutil_attrs)

        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(path, "s3://my_bucket", None)
            test_deploy.deploy()

            popen_mock.wait.assert_any_call()
            self.assertTrue(popen_mock.wait.call_count == 4, "Popen.wait has the incorrect number of calls!")
            self.assertTrue(archive_func.call_count == 1, "Did not call make_archive!")

        except Exception as e:
            print(e)
            self.assertTrue(False, "Unable to deploy!")

    @patch('subprocess.Popen') # Mocks the Popen object from subprocess
    def test_deploy_fail_process(self, popen_func):
        popen_mock = Mock()
        attrs = {'wait.return_value': 1}
        popen_mock.configure_mock(**attrs)
        popen_func.return_value = popen_mock
        try:
            path = os.getcwd()
            test_deploy = LambdaDeploy(path, "s3://pb-gravity", None)
            test_deploy.deploy()
        except Exception as e:
            popen_mock.wait.assert_any_call()
            self.assertTrue(popen_mock.wait.call_count == 1, "Popen.wait was called more than once before failing!")

