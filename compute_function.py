''' The function below is used by the transfer-and-compute flow.
In order to use it, you must first register it with the funcX service,
as described here: https://funcx.readthedocs.io/en/latest/index.html
(code is also provided below).

Before invoking the function, ensure that you have the Pillow library
(https://python-pillow.org) installed on your funcX endpoint.
'''

def process_images(input_path=None, result_path=None):

    import os
    import glob
    from PIL import Image
    
    files = (file for file in glob.glob(os.path.join(input_path,'*')) \
        if os.path.isfile(os.path.join(input_path, file)))

    if not os.path.exists(result_path):
        os.makedirs(result_path)
    
    for file in files:
        image = Image.open(file)

        # Generate thumbnail
        image.thumbnail((200, 200))

        # Save thumbnail image
        image.save(f"{result_path}/thumb_{os.path.basename(file)}")


'''Code to register the function with the funcX service
'''

from funcx import FuncXClient

def deploy_function():
    fxc = FuncXClient()
    func_uuid = fxc.register_function(process_images)

    # Register a function and allow a Globus group of users to invoke it
    func_uuid = fxc.register_function(process_images, group="GLOBUS_GROUP_ID")

    print(f"Registered function with ID {func_uuid}")

### EOF