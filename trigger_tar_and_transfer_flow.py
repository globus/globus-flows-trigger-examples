#!/usr/bin/env python

import os
import argparse

# This could go into a different file and be invoked without the file watcher
from globus_automate_client import create_flows_client


def run_flow(event_file):
    fc = create_flows_client()

    # TODO: Specify the flow to run when triggered
    flow_id = ''
    flow_scope = fc.get_flow(flow_id).data['globus_auth_scope']

    # TODO: Set a label for the flow run
    flow_label = f"Trigger transfer: {os.path.basename(event_file)}"

    # TODO: Modify source collection ID
    # Source collection must be on the endpoint where this trigger code is running
    source_id = ''
   
    # TODO: Modify destination collection ID
    destination_id = ''

    # TODO: Modify destination collection path
    # Update path to include your user name e.g. /automate-tutorial/dev1/
    destination_base_path = ''

    # TODO: Modify list of tar inputs
    # May contain files or directories
    tar_inputs = ["/path/to/files"]

    # TODO: Modify tar filename
    tar_output = "/path/to/output/mydata.tgz"

    # TODO: Modify Globus Compute endpoint ID where tar will run
    compute_endpoint_id = 'REPLACE_WITH_COMPUTE_ENDPOINT_ID'

    # TODO: Specify the tar function id
    # The tar function has already been deployed as 081eb4c1-ecce-445c-880e-8488bed6698a
    # If you would like to make changes to this function, see tar_function.py, compute_function.py, and update here
    compute_function_id = "c55330d8-e788-4416-8697-995d2237add9"

    # Get the directory where the triggering file is stored and 
    # add trailing '/' to satisfy Transfer requirements for moving a directory
    event_folder = os.path.dirname(event_file)

    # Get name of monitored folder to use as destination path
    # and for setting permissions
    event_folder_name = os.path.basename(event_folder)
    destination_path = os.path.join(destination_base_path, os.path.basename(tar_output))

    # Inputs to the flow
    flow_input = {
        "tar": {
            "compute_endpoint_id": compute_endpoint_id,
            "compute_function_id": compute_function_id,
            "compute_function_kwargs": {
                "inputs": tar_inputs,
                "output": tar_output
            }
        }
        "transfer": {
            "source_collection": source_id,
            "source_path": tar_output,
            "destination_collection": destination_id,
            "destination_path": destination_path,
            "label": flow_label
        }
    }

    flow_run_request = fc.run_flow(
        flow_id=flow_id,
        flow_scope=flow_scope,
        flow_input=flow_input,
        label=flow_label,
        tags=['Trigger_Tutorial']
    )
    print(f"Transferring: {event_folder_name}")
    print(f"https://app.globus.org/runs/{flow_run_request['run_id']}")


# Parse input arguments
def parse_args():
    parser = argparse.ArgumentParser(description='''
        Watch a directory and trigger a simple transfer flow.''')
    parser.add_argument('--watchdir',
                        type=str,
                        default=os.path.abspath('.'),
                        help=f'Directory path to watch. [default: current directory]')
    parser.add_argument('--patterns',
                        type=str,
                        default='',
                        nargs='*',
                        help='Filename suffix pattern(s) that will trigger the flow. [default: ""]')
    parser.set_defaults(verbose=True)
    
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    
    # Creates and starts the watcher
    from watch import FileTrigger
    trigger = FileTrigger(
        watch_dir=os.path.expanduser(args.watchdir),
        patterns=args.patterns,
        FlowRunner=run_flow
    )
    trigger.run()
