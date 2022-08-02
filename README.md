# Examples of Triggers for Globus Flows

We provide three examples of triggering flows. We start with a single-action flow that trasnfers data (as defined in [`def_transfer_flow.json`](https://github.com/globus/globus-flows-trigger-examples/blob/main/def_transfer_flow.json)), then add an action that sets permissions for sharing the data (as defined in [`def_transfer_share_flow.json`](https://github.com/globus/globus-flows-trigger-examples/blob/main/def_transfer_share_flow.json)), and finally add an action that ingests metadata into a Globus Search index (as defined in [`def_transfer_publish_flow.json`](https://github.com/globus/globus-flows-trigger-examples/blob/main/def_transfer_publish_flow.json)).

## Installation
The examples require the `globus_automate_client` and `watchdog` packages. They can be installed by creating a Python virtual environment and running:

     pip install -r requirements.txt

## Deploying the flows
You can deploy each flow by running `./deploy_flow --defs FLOW_DEFINITION_FILE --title FLOW_TITLE`. For example, to deploy the transfer-and-share flow, run:

     ./deploy_flow.py --defs def_transfer_share_flow.json --title "My Transfer and Share Flow Example"
 
## Running the watcher to trigger a flow
A separate watcher script is provided for triggering each flow. Each script must be modified to provide the required inputs to the flow, but all three scripts are run the same way, by specifying two arguments:

1. `--watchdir` specifies the directory path to watch
1. `--paterns` specifies the file suffix pattern(s) to watch for (this can be a list of multiple suffixes, separated by spaces).

For example, to trigger the transfer-and-share flow when a file with suffix `.done` is created in directory `/my/experiment/data`, run:

     ./trigger_transfer_share_flow.py --watchdir /my/experiment/data --patterns .done

## Modifying the trigger logic
The trigger logic can be modified by editing the `Handler` class in `watch.py`. By default, the trigger logic will run the flow every time a file is created that ends with one of the suffixes specified in `--patterns`.
