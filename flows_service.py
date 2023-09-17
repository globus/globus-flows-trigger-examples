# flows_service.py
#
# Utility functions for interacting with the Globus Flows service
#

import os
import sys

import globus_sdk
from globus_sdk.tokenstorage import SimpleJSONFileAdapter

# Tokens and refresh tokens will be stored in this file; secure it!!
TOKEN_FILE_ADAPTER = SimpleJSONFileAdapter(
    os.path.expanduser("~/.globus-flows-trigger-tokens.json")
)

SERVICE_SCOPES = [
    globus_sdk.FlowsClient.scopes.manage_flows,
    globus_sdk.FlowsClient.scopes.run,
    globus_sdk.FlowsClient.scopes.run_status,
    globus_sdk.FlowsClient.scopes.run_manage,
    globus_sdk.FlowsClient.scopes.view_flows,
]
RESOURCE_SERVER = globus_sdk.FlowsClient.resource_server

# Replace this with your own client ID; register a native application
# client at https://app.globus.org/settings/developers
CLIENT_ID = "61338d24-54d5-408f-a10d-66c06b59f6d2"  # tutorial client ID

NATIVE_CLIENT = globus_sdk.NativeAppAuthClient(CLIENT_ID)


def get_tokens(scopes=None):
    # Initiate login flow
    NATIVE_CLIENT.oauth2_start_flow(
        requested_scopes=scopes, refresh_tokens=True
    )
    authorize_url = NATIVE_CLIENT.oauth2_get_authorize_url()
    print(f"Log in at this URL and get authorization code:\n\n{authorize_url}\n")
    auth_code = input("Enter authorization code here: ").strip()

    tokens = NATIVE_CLIENT.oauth2_exchange_code_for_tokens(auth_code)

    return tokens


def get_authorizer(flow_id=None):
    if flow_id:
        scopes = globus_sdk.SpecificFlowClient(flow_id).scopes.user
        resource_server = flow_id
    else:
        scopes = SERVICE_SCOPES
        resource_server = RESOURCE_SERVER

    # Try to load saved tokens
    if TOKEN_FILE_ADAPTER.file_exists():
        tokens = TOKEN_FILE_ADAPTER.get_token_data(resource_server)
    else:
        tokens = None

    if tokens is None:
        # Log into Globus Auth and get tokens
        response = get_tokens(scopes=scopes)
        # Store tokens and extract token for Globus Flows service
        TOKEN_FILE_ADAPTER.store(response)
        tokens = response.by_resource_server[resource_server]

    return globus_sdk.RefreshTokenAuthorizer(
        tokens["refresh_token"],
        NATIVE_CLIENT,
        access_token=tokens["access_token"],
        expires_at=tokens["expires_at_seconds"],
        on_refresh=TOKEN_FILE_ADAPTER.on_refresh,
    )


def create_flows_client(flow_id=None):
    if flow_id:
        return globus_sdk.SpecificFlowClient(
            flow_id, 
            authorizer=get_authorizer(flow_id=flow_id)
        )
    else:
        return globus_sdk.FlowsClient(
            authorizer=get_authorizer()
        )
