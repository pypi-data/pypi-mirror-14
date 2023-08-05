from __future__ import print_function
import subprocess
import os
import platform
import shutil
import tempfile

class LambdaDeploy(object):
    """
    Deploys a zip to S3 that is ready for use with lambda.
    """
    def __init__(self, directory, bucket, name):
        """
        Creates a new deploy object for deploying to S3.

        Params:
        -------
        directory : str
            Location of the lambda function to zip. This should include pip files.
        bucket : str
            The S3 bucket to send the file to.
        name : str
            The name of the zipped file. Defaults to my_lambda_function
        """
        self.directory = directory
        self.bucket = bucket
        self.name = name

        self.cmd = "where" if platform.system() == "Windows" else "which"

        self.__initialize()

    def __initialize(self):
        """
        Initializes the object and ensures data integrity.

        Raises:
        -------
        ValueError:
            If the provided directory, bucket name or filename are not valid.

        IOError:
            When the provided directory cannot be found on the system.
        """
        if self.directory is None or type(self.directory) is not str or self.directory == "":
            raise ValueError("Please provide a valid directory.")
        if self.bucket is None or type(self.bucket) is not str or self.bucket == "":
            raise ValueError("Please provide a valid S3 bucket location.")
        if self.name is not None and (type(self.name) is not str or self.name == ""):
            raise ValueError("Please provide a valid name for the zip file.")

        # Check for valid paths for the directory and S3
        if not os.path.isdir(self.directory):
            raise IOError(self.directory + " is not a valid directory!")

        self.directory = os.path.abspath(self.directory)

        if self.bucket.find("s3://") == -1:
            raise ValueError("Invalid S3 bucket location! Should start with 's3://'")

        if self.name is None:
            self.name = "my_lambda_function"

    def deploy(self):
        """
        Deploys to AWS based on the internal state of the object.

        Raises:
        -------
        Exception:
            When 'awscli' is not installed or if unable to zip the directory.
        """
        args = [self.cmd, "aws"]
        p = subprocess.Popen(args, shell=True)
        result = p.wait()
        if result != 0:
            raise Exception("'aws' cli is not installed on the system!")

        self.check_pip_packages()

        # ZIP file
        try:
            shutil.make_archive(os.path.join(tempfile.gettempdir(), self.name), "zip", self.directory)
        except OSError as e:
            raise Exception(str(e))

        # Send to aws
        args = ["aws", "s3", "cp", os.path.join(tempfile.gettempdir(), self.name + ".zip"), self.bucket]
        p = subprocess.Popen(args, shell=True)
        result = p.wait()
        if result != 0:
            raise Exception("Unable to upload to S3!")

    def check_pip_packages(self):
        """
        Checks if the directory uses pip packages. If so, downloads to correct folder within directory.

        Raises:
        -------
        Exception:
            When 'pip' is not installed or when unable to install from requirements.txt
        """
        if not os.path.isfile(os.path.join(self.directory, "requirements.txt")):
            print("WARNING: No 'requirements.txt' was found within the directory. Skipping automatic pip packaging.")
        else:
            args = [self.cmd, "pip"]
            p = subprocess.Popen(args, shell=True)
            result = p.wait()
            if result != 0:
                raise Exception("'pip' is not installed on the system!")

            args = ["pip", "install", "-r", os.path.join(self.directory, "requirements.txt"), "-t", self.directory]
            p = subprocess.Popen(args, shell=True)
            result = p.wait()
            if result != 0:
                raise Exception("Unable to pip install packages from requirements.txt!")
