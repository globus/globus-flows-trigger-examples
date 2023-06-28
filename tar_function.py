""" The function below is used by the tar-and-transfer flow.
In order to use it, you must first register it with the
Globus Compute service, as described here:
https://globus-compute.readthedocs.io/en/latest/Tutorial.html#registering-a-function
(code is also provided below).

This function uses the tarfile module, which is part of the standard
Python library (it also assumes the gzip module is available). It accepts a
list of files/paths (as strings) and the name of the resulting archive file.
'inputs' is a list of absolute paths and 'output' is the absolute path to
the resulting archive file.
"""


def tar_files(inputs=None, output=None):
    import tarfile

    try:
        with tarfile.open(output, "w:gz") as tar:
            for input_file in inputs:
                tar.add(input_file)
    except Exception as e:
        return str(e)


"""Code to register the function with the Globus Compute service
"""

from globus_compute_sdk import Client


def deploy_function():
    client = Client()

    try:
        func_uuid = client.register_function(tar_files)
        print(f"Registered 'tar_files' function with ID {func_uuid}")
    except Exception as e:
        print(f"Failed to register function: {e}")


def main():
    deploy_function()


if __name__ == "__main__":
    main()

### EOF
