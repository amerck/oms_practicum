import json
import asyncio
import configparser
from itso_ai.clients.microsoft import MSGraphAPIClient


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
    id_ = result.id
    attachments = process_attachments(result.attachments)
    content_type = result.body.content_type
    content = result.body.content
    created_date_time = result.created_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    from_ = process_user(result.from_)
    subject = result.subject
    reactions = process_reactions(result.reactions)
    replies = process_replies(result.replies)
    message = {'id': id_, 'subject': subject, 'attachments': attachments, 'content': content, 'content_type': content_type,
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

    f_out = open(output_file, 'w')

    client = MSGraphAPIClient(azure_settings)

    i = 1
    print('query %s' % i)
    results = await client.list_messages(team_id, channel_id)
    odata_next_link = results.odata_next_link
    for result in results.value:
        r = process_result(result)
        f_out.write('%s\n' % json.dumps(r))
    i += 1

    while odata_next_link:
        try:
            print('query %s' % i)
            results = await client.get_next_messages(team_id, channel_id, odata_next_link)
        except Exception as e:
            print(e)
            continue
        odata_next_link = results.odata_next_link
        i += 1
        for result in results.value:
            r = process_result(result)
            f_out.write('%s\n' % json.dumps(r))

    f_out.close()

if __name__ == '__main__':
    asyncio.run(main())
