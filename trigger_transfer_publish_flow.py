#!/usr/bin/env python

import argparse
import glob
import os

# This could go into a different file and be invoked without the file watcher
from flows_service import create_flows_client
from user import UserIdentity


def run_flow(event_file):
    # TODO: Specify the flow to run when triggered
    flow_id = "REPLACE_WITH_FLOW_ID"
    fc = create_flows_client(flow_id=flow_id)

    # TODO: Set a label for the flow run
    # Default includes the file name that triggered the run
    flow_label = f"Trigger transfer->publish: {os.path.basename(event_file)}"

    # TODO: Modify source collection ID
    # Source collection must be on the endpoint where this trigger code is running
    source_id = "REPLACE_WITH_SOURCE_COLLECTION_ID"

    # TODO: Modify destination collection ID
    # Destination must be a guest collection so permission can be set
    # Default is "Globus Tutorials on ALCF Eagle"
    destination_id = "a6f165fa-aee2-4fe5-95f3-97429c28bf82"

    # TODO: Modify destination collection path
    # Update path to include your user name e.g. /automate-tutorial/dev1/
    destination_base_path = "/automation-tutorial/USERNAME/"

    # TODO: Modify identity/group ID to share with
    # Default is "Tutorial Users" group
    sharee_id = "50b6a29c-63ac-11e4-8062-22000ab68755"

    # TODO: Specify the search index to publish your metadata
    search_index = "REPLACE_WITH_GLOBUS_SEARCH_INDEX_ID"

    # Get the directory where the triggering file is stored and
    # add trailing '/' to satisfy Transfer requirements for moving a directory
    event_folder = os.path.dirname(event_file)
    source_path = os.path.join(event_folder, "")

    # Get name of monitored folder to use as destination path
    # and for setting permissions
    event_folder_name = os.path.basename(event_folder)

    # Add a trailing '/' to meet Transfer requirements for directory transfer
    destination_path = os.path.join(destination_base_path, event_folder_name, "")

    # Gather some information about the transfer to include in metadata
    file_names = glob.glob(source_path + "*")

    # Use a helper-class to login, to get the user's Globus identity uuid.
    # This ID is used to set access control on search records in the flow below.
    user_identity = UserIdentity()

    # Inputs to the flow
    flow_input = {
        "input": {
            # local endpoint where the event listener is running
            "source": {"id": source_id, "path": source_path},
            "destination": {"id": destination_id, "path": destination_path},
            "recursive_tx": True,
            "principal": {
                "type": "group",
                "id": sharee_id,
            },
            # Metadata to ingest into Globus Search index
            # TODO: Update "search_content_metadata" with your own
            "search_ingest_document": {
                "search_index": search_index,
                "search_subject": event_folder_name,
                "search_entry_id": "PUB00001",
                "search_visible_to": ["public"],
                "search_content_metadata": {
                    "title": event_folder_name,
                    "filecount": len(file_names),
                    "filenames": file_names,
                },
                # Principal URNs look like urn:globus:auth:identity:GLOBUS_AUTH_IDENTITY_UUID
                # Ref: https://docs.globus.org/api/search/overview/#principal_urns
                "search_restricted_entry_id": "RES00001",
                "search_restricted_visible_to": [user_identity.principal_urn],
                "search_content_restricted_metadata": {
                    "secret": "Formula 20220730",
                    "pathogen": "XLKFT-34895",
                    "antidote": "Unavailable",
                },
            },
        }
    }

    flow_run_request = fc.run_flow(
        body=flow_input,
        label=flow_label,
        tags=["Trigger_Tutorial"],
    )
    print(f"Transferring and publishing: {event_folder_name}")
    print(f"Metadata published to search index: {search_index}")
    print(f"https://app.globus.org/runs/{flow_run_request['run_id']}")


# Parse input arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Watch a directory and trigger a transfer-and-share flow."""
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
    from watch import FileTrigger

    trigger = FileTrigger(
        watch_dir=os.path.expanduser(args.watchdir),
        patterns=args.patterns,
        FlowRunner=run_flow,
    )
    trigger.run()
