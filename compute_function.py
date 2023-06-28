""" The function below is used by the transfer-and-compute flow.
In order to use it, you must first register it with the 
Globus Compute service, as described here:
https://globus-compute.readthedocs.io/en/latest/Tutorial.html#registering-a-function
(code is also provided below).

This function generates thumbnail images for all PNG files in the
input_path and places them in result_path. Before invoking the function, 
ensure that you have the Pillow library (https://python-pillow.org) 
installed on your Globus Compute endpoint.
"""


def process_images(input_path=None, result_path=None):
    import os
    import glob
    from PIL import Image

    files = (
        file
        for file in (
            glob.glob(os.path.join(input_path, "*.png"))
            + glob.glob(os.path.join(input_path, "*.jpg"))
        )
        if os.path.isfile(file)
    )

    if not os.path.exists(result_path):
        os.makedirs(result_path)

    for file in files:
        image = Image.open(file)

        # Generate thumbnail
        image.thumbnail((200, 200))

        # Save thumbnail image
        image.save(f"{result_path}/thumb_{os.path.basename(file)}")


"""Code to register the function with the Globus Compute service
"""

from globus_compute_sdk import Client


def deploy_function():
    client = Client()

    try:
        func_uuid = client.register_function(process_images)
        print(f"Registered 'process_images' function with ID {func_uuid}")
    except Exception as e:
        print(f"Failed to register function: {e}")


def main():
    deploy_function()


if __name__ == "__main__":
    main()

### EOF
