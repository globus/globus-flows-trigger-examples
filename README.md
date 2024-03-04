# Examples of Triggers for Globus Flows

We provide examples of triggering flows with the following actions:

* [Tar and Transfer](https://github.com/globus/globus-flows-trigger-examples/tree/main/tar_transfer): A flow that creates a tar archive (using Globus Compute) and transfers the resulting tar file to the destination collection.
* [Transfer](https://github.com/globus/globus-flows-trigger-examples/tree/main/transfer): A single-action flow that transfers data.
* [Transfer and Compute](https://github.com/globus/globus-flows-trigger-examples/tree/main/transfer_compute): A flow that transfers data and invokes a Globus Compute function on the destination collection to process the transferred files.
* [Transfer, Compute and Share](https://github.com/globus/globus-flows-trigger-examples/tree/main/transfer_compute_share): A flow that transfers data, invokes a Globus Compute function on the destination collection to process the transferred files, transfers the processed files to another collection, and sets permissions for sharing the data.
* [Transfer and Publish](https://github.com/globus/globus-flows-trigger-examples/tree/main/transfer_publish): A flow that transfers data, sets permissions for accessing the data, and ingests metadata (both fully accessible and restricted) into a Globus Search index.
* [Transfer and Share](https://github.com/globus/globus-flows-trigger-examples/tree/main/transfer_share): A flow that transfers data and sets permissions for sharing the data.

Each folder contains three files:

* definition.json - the flow definition
* schema.json - the flow input schema
* trigger_*.py - a Python script that will trigger the flow

## Installation
The examples require the `globus_sdk` and `watchdog` packages. They can be installed by creating a Python virtual environment and running:

     pip install -r requirements.txt

You will also need the Globus CLI to create and update your flow. Installation instructions can be found [here](https://docs.globus.org/cli/).

## Deploying the flows
You can deploy each flow by running `globus flows create FLOW_TITLE FLOW_DEFINITION_FILE --input-schema FLOW_INPUT_SCHEMA_FILE`. For example, to deploy the transfer-and-share flow, run:

     globus flows create "My Transfer and Share Flow Example" transfer_share/definition.json --input-schema transfer_share/schema.json

## Running the watcher to trigger a flow
A separate watcher script is provided for triggering each flow. The trigger script must be modified before running, by defining values for the flow ID, collection ID and other variables (varies by script). Look for placeholders like `"REPLACE_WTIH_...` and provide values for each before running the trigger script. All trigger scripts are run by specifying two arguments:

1. `--watchdir` specifies the directory path to watch
1. `--patterns` specifies the file suffix pattern(s) to watch for (this can be a list of multiple suffixes, separated by spaces).

For example, to trigger the transfer-and-share flow when a file with suffix `.done` is created in directory `/my/experiment/data`, run:

     ./trigger_transfer_share_flow.py --watchdir /my/experiment/data --patterns .done

## Modifying the trigger logic
The trigger logic can be modified by editing the `Handler` class in `watch.py`. By default, the trigger logic will run the flow every time a file is created that ends with one of the suffixes specified in `--patterns`.

## Modifying a deployed flow
A deployed flow may be updated by running:

     globus flows update FLOW_ID --definition UPDATED_FLOW_DEFINITION_FILE --input-schema UPDATED_FLOW_INPUT_SCHEMA_FILE --title UPDATED_FLOW_TITLE

Note: This is just a convenience extension for these examples, and is limited to updating only the flow/schema definition and/or flow title; refer to the [Globus Flows API](https://globusonline.github.io/globus-flows/) reference for the full-featured `PUT`.

## Flows including compute actions
Some of the flows include a compute action that uses the [Globus Compute service](https://globus-compute.readthedocs.io/en/latest/index.html). In order for these flows to succeed you must first create a Globus Compute endpoint and ensure that the compute endpoint has a Python environment with any required packages already installed. You must also register the function to run in the compute step with the Globus Compute service; we provide two scripts for deploying the required Globus Compute functions:

* [compute_function.py](https://github.com/globus/globus-flows-trigger-examples/functions/blob/main/compute_function.py) - contains a simple image manipulation function that creates thumbnail images for any `.png` and `.jpg` files transferred by the flow. The compute endpoint environment for running this function must include the [`Pillow` package](https://pillow.readthedocs.io/en/stable/). This function is used in the [transfer_compute](https://github.com/globus/globus-flows-trigger-examples/tree/main/transfer_compute) and [transfer_compute_share](https://github.com/globus/globus-flows-trigger-examples/tree/main/transfer_compute_share) flows.
* [tar_function.py](https://github.com/globus/globus-flows-trigger-examples/functions/blob/main/tar_function.py) - contains a function for archiving all files in the specified directory to a tar file, which will then be transferred by the flow. The compute endpoint environment for running this function must include the [`tarfile` package](https://docs.python.org/3/library/tarfile.html). This function is used in the  [tar_transfer](https://github.com/globus/globus-flows-trigger-examples/tree/main/tar_transfer) flow.
