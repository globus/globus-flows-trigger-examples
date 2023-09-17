#!/usr/bin/env python

import argparse
import os

# This could go into a different file and be invoked without the file watcher
from flows_service import create_flows_client

from watch import FileTrigger, translate_local_path_to_globus_path


def run_flow(event_file):
    fc = create_flows_client()

    # TODO: Specify the flow to run when triggered
    flow_id = "REPLACE_WITH_FLOW_ID"
    flow_scope = fc.get_flow(flow_id).data["globus_auth_scope"]

    # TODO: Set a label for the flow run
    # Default includes the file name that triggered the run
    flow_label = f"Trigger transfer: {os.path.basename(event_file)}"

    # TODO: Modify source collection ID
    # Source collection must be on the endpoint where this trigger code is running
    source_id = "REPLACE_WITH_SOURCE_COLLECTION_ID"

    # TODO: Modify destination collection ID
    # Default is "Globus Tutorials on ALCF Eagle"
    destination_id = "a6f165fa-aee2-4fe5-95f3-97429c28bf82"

    # TODO: Modify destination collection path
    # Update path to include your user name e.g. /automate-tutorial/dev1/
    destination_base_path = "/automation-tutorial/USERNAME/"

    # Get the Globus-compatible directory name where the triggering file is stored.
    event_folder = os.path.dirname(event_file)
    source_path = translate_local_path_to_globus_path(event_folder)

    # Get name of monitored folder to use as destination path
    # and for setting permissions
    event_folder_name = os.path.basename(event_folder)

    # Add a trailing '/' to meet Transfer requirements for directory transfer
    destination_path = os.path.join(destination_base_path, event_folder_name, "")
    # Convert Windows path separators to forward slashes.
    destination_path = destination_path.replace("\\", "/")

    # Inputs to the flow
    flow_input = {
        "input": {
            "source": {
                "id": source_id,
                "path": source_path,
            },
            "destination": {
                "id": destination_id,
                "path": destination_path,
            },
            "recursive_tx": True,
        }
    }

    flow_run_request = fc.run_flow(
        flow_id=flow_id,
        flow_scope=flow_scope,
        flow_input=flow_input,
        label=flow_label,
        tags=["Trigger_Tutorial"],
    )
    print(f"Transferring: {event_folder_name}")
    print(f"https://app.globus.org/runs/{flow_run_request['run_id']}")


# Parse input arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Watch a directory and trigger a simple transfer flow."""
    )
    parser.add_argument(
        "--watchdir",
        type=str,
        default=os.path.abspath("."),
        help=f"Directory path to watch. [default: current directory]",
    )
    parser.add_argument(
        "--patterns",
        type=str,
        default="",
        nargs="*",
        help='Filename suffix pattern(s) that will trigger the flow. [default: ""]',
    )
    parser.set_defaults(verbose=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Creates and starts the watcher
    trigger = FileTrigger(
        watch_dir=os.path.expanduser(args.watchdir),
        patterns=args.patterns,
        FlowRunner=run_flow,
    )
    trigger.run()
