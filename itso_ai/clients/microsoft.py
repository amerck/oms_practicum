from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import (
    MessagesRequestBuilder)
from kiota_abstractions.base_request_configuration import RequestConfiguration


class MSGraphAPIClient:

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.graph_client = GraphServiceClient(self.device_code_credential, graph_scopes)

    async def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token

    async def list_joined_teams(self):
        # https://learn.microsoft.com/en-us/graph/api/user-list-joinedteams?view=graph-rest-1.0&tabs=python
        results = await self.graph_client.me.joined_teams.get()
        return results

    async def list_channels(self, team_id):
        # https://learn.microsoft.com/en-us/graph/api/channel-list?view=graph-rest-1.0&tabs=http
        results = await self.graph_client.teams.by_team_id(team_id).channels.get()
        return results

    async def list_messages(self, team_id, channel_id):
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            top=5,
            expand=["replies"],
        )

        request_configuration = RequestConfiguration(
            query_parameters=query_params,
        )

        # https://learn.microsoft.com/en-us/graph/api/channel-list-messages?view=graph-rest-1.0&tabs=python
        results = await self.graph_client.teams.by_team_id(team_id).channels.by_channel_id(channel_id).messages.get(request_configuration = request_configuration)
        return results

    async def get_next_messages(self, team_id, channel_id, url):
        results = await self.graph_client.teams.by_team_id(team_id).channels.by_channel_id(channel_id).messages.with_url(url).get()
        return results