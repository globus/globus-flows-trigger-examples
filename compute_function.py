''' The function below is used by the transfer-and-compute flow.
In order to use it, you must first register it with the 
Globus Compute service, as described here:
https://globus-compute.readthedocs.io/en/latest/Tutorial.html#registering-a-function
(code is also provided below).

Before invoking the function, ensure that you have the Pillow library
(https://python-pillow.org) installed on your Globus Compute endpoint.
'''

GLOBUS_GROUP_ID = '50b6a29c-63ac-11e4-8062-22000ab68755'  # Tutorial Users group

def process_images(input_path=None, result_path=None):

    import os
    import glob
    from PIL import Image
    
    files = (file for file in glob.glob(os.path.join(input_path,'*.png')) \
        if os.path.isfile(os.path.join(input_path, file)))

    if not os.path.exists(result_path):
        os.makedirs(result_path)
    
    for file in files:
        image = Image.open(file)

        # Generate thumbnail
        image.thumbnail((200, 200))

        # Save thumbnail image
        image.save(f"{result_path}/thumb_{os.path.basename(file)}")


'''Code to register the function with the Globus Compute service
'''

from globus_compute_sdk import Client

def deploy_function():
    client = Client()
    func_uuid = client.register_function(process_images)

    # Register a function and allow a Globus group of users to invoke it
    func_uuid = client.register_function(process_images, group=GLOBUS_GROUP_ID)

    print(f"Registered function with ID {func_uuid}")

### EOF
