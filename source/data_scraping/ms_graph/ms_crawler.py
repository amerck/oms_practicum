import json
import asyncio
import configparser
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import (
    MessagesRequestBuilder)
from kiota_abstractions.base_request_configuration import RequestConfiguration


class Graph:

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


def process_attachments(attachments):
    attachments_list = []
    for attachment in attachments:
        id_ = attachment.id
        content_type = attachment.content_type
        content = attachment.content
        attachments_list.append({'id': id_, 'content_type': content_type, 'content': content})
    return attachments_list


def process_reactions(reactions):
    reaction_list = []
    for reaction in reactions:
        created_date_time = reaction.created_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        display_name = reaction.display_name
        reaction_type = reaction.reaction_type
        reaction_list.append({'timestamp': created_date_time,
                              'reaction_name': display_name, 'reaction_type': reaction_type})
    return reaction_list

def process_replies(replies):
    reply_list = []
    for reply in replies:
        content = reply.body.content
        content_type = reply.body.content_type
        created_date_time = reply.created_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        from_ = process_user(reply.from_)
        reactions = process_reactions(reply.reactions)
        reply_list.append({'content': content, 'content_type': content_type, 'timestamp': created_date_time,
                           'user': from_, 'reactions': reactions})
    return reply_list

def process_user(from_):
    user = None
    if not from_:
        return user

    if from_.application:
        user = from_.application.display_name
    elif from_.user:
        user = from_.user.display_name
    return user


def process_result(result):
    attachments = process_attachments(result.attachments)
    content_type = result.body.content_type
    content = result.body.content
    created_date_time = result.created_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    from_ = process_user(result.from_)
    reactions = process_reactions(result.reactions)
    replies = process_replies(result.replies)
    message = {'attachments': attachments, 'content': content, 'content_type': content_type,
              'timestamp': created_date_time, 'user': from_, 'reactions': reactions, 'replies': replies}
    return {'message': message}


async def main():

    # Load settings
    config = configparser.ConfigParser()
    config.read(['./config/config.cfg', './config/config.dev.cfg'])
    azure_settings = config['azure']
    teams_settings = config['teams']

    team_id = teams_settings['teamId']
    channel_id = teams_settings['channelId']
    output_file = teams_settings['outputFile']

    fout = open(output_file, 'w')

    graph = Graph(azure_settings)

    i = 1
    print('query %s' % i)
    results = await graph.list_messages(team_id, channel_id)
    odata_next_link = results.odata_next_link
    for result in results.value:
        r = process_result(result)
        fout.write('%s\n' % json.dumps(r))
    i += 1

    while odata_next_link:
        try:
            print('query %s' % i)
            results = await graph.get_next_messages(team_id, channel_id, odata_next_link)
        except Exception as e:
            print(e)
            continue
        odata_next_link = results.odata_next_link
        i += 1
        for result in results.value:
            r = process_result(result)
            fout.write('%s\n' % json.dumps(r))


if __name__ == '__main__':
    asyncio.run(main())
