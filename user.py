import globus_sdk

class UserIdentity:
    def __init__(self):
        """
        This uses the Globus SDK Client tutorial to fetch the id of the user. The ID is
        saved in memory as a principal URN so it can be used to secure Globus Search records.
        """

        # This client is based on the Globus SDK Tutorial.
        CLIENT_ID = "61338d24-54d5-408f-a10d-66c06b59f6d2"

        client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
        client.oauth2_start_flow(requested_scopes=globus_sdk.AuthClient.scopes.openid)

        authorize_url = client.oauth2_get_authorize_url()
        print("Please go to this URL and login: \n {0}".format(authorize_url))

        auth_code = input("\n Please enter the code you get after login here: ").strip()
        token_response = client.oauth2_exchange_code_for_tokens(auth_code)

        # Set the principal URN so it can be referenced at a later time.
        self.principal_urn = (
            f"urn:globus:auth:identity:{token_response.decode_id_token()['sub']}"
        )
