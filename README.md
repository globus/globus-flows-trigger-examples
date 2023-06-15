# Examples of Triggers for Globus Flows

We provide three examples of triggering flows:

* We start with a single-action flow that transfers data (as defined in [`transfer_flow_definition.json`](https://github.com/globus/globus-flows-trigger-examples/blob/main/transfer_flow_definition.json))
* Next we add an action that sets permissions for sharing the data (as defined in [`transfer_share_flow_definition.json`](https://github.com/globus/globus-flows-trigger-examples/blob/main/transfer_share_flow_definition.json))
* And then we add an action that ingests metadata into a Globus Search index (as defined in [`transfer_publish_flow_definition.json`](https://github.com/globus/globus-flows-trigger-examples/blob/main/transfer_publish_flow_definition.json))

## Installation
The examples require the `globus_automate_client` and `watchdog` packages. They can be installed by creating a Python virtual environment and running:

     pip install -r requirements.txt

## Deploying the flows
You can deploy each flow by running `./deploy_flow --flowdef FLOW_DEFINITION_FILE --schema FLOW_INPUT_SCHEMA_FILE --title FLOW_TITLE`. For example, to deploy the transfer-and-share flow, run:

     ./deploy_flow.py --flowdef transfer_share_flow_definition.json --schema transfer_share_flow_schema.json --title "My Transfer and Share Flow Example"

## Running the watcher to trigger a flow
A separate watcher script is provided for triggering each flow. Each script must be modified to provide the required inputs to the flow, but all three scripts are run the same way, by specifying two arguments:

1. `--watchdir` specifies the directory path to watch
1. `--patterns` specifies the file suffix pattern(s) to watch for (this can be a list of multiple suffixes, separated by spaces).

For example, to trigger the transfer-and-share flow when a file with suffix `.done` is created in directory `/my/experiment/data`, run:

     ./trigger_transfer_share_flow.py --watchdir /my/experiment/data --patterns .done

## Modifying the trigger logic
The trigger logic can be modified by editing the `Handler` class in `watch.py`. By default, the trigger logic will run the flow every time a file is created that ends with one of the suffixes specified in `--patterns`.

## Modifying a deployed flow
A deployed flow may be updated by running:

     ./deploy_flow.py --flowid <FLOW_ID> --flowdef <UPDATED_FLOW_DEFINITION> --schema <UPDATED_FLOW_INPUT_SCHEMA> --title <UPDATED_FLOW_TITLE>

Note: This is just a convenience extension for these examples, and is limited to updating only the flow/schema definition and/or flow title; refer to the [Globus Flows API](https://globusonline.github.io/flows/) reference for the full-featured `PUT`.

## From the future
Also included in this repository are two flows that introduce the use of [funcX](https://funcx.org). _Please note that funcX is currently in development, and is not a production Globus service (although it's already used extensively at some large facilities), hence the "future"_.

[`transfer_compute_flow_definition.json`](https://github.com/globus/globus-flows-trigger-examples/blob/main/transfer_compute_flow_definition.json) defines a flow that transfers files and then runs a function to process them. It's intended as a simple illustration of a very common pattern: move data to a compute resource and run a job to process the data. [`transfer_compute_share_flow_definition.json`](https://github.com/globus/globus-flows-trigger-examples/blob/main/transfer_compute_share_flow_definition.json) extends this flow by adding a subsequent transfer to a guest collection and setting permissions for sharing.

The corresponding trigger code assumes you have registered a funcX endpoint and a Python function with the funcX service (see the [funcX tutorial](https://funcx.readthedocs.io/en/latest/Tutorial.html) for a quick overview). [`compute_function.py`](https://github.com/globus/globus-flows-trigger-examples/blob/main/compute_function.py) is an example of such a function; it generates thumbnails for all files in `input_path` and saves them in `results_path`. Feel free to replace it with your own (more useful!) function.
