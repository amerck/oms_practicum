import json
import uuid
import markdownify


class TeamsParser:

    def __init__(self, msg, metadata_finder):
        self.metadata_finder = metadata_finder
        self.msg_id = uuid.uuid4().hex
        self.msg = json.loads(msg).get('message')
        self.sender = self.msg.get('user', '')
        self.timestamp = self.msg.get('timestamp')
        self.attachment = self.process_attachments()
        self.replies = self.msg.get('replies', [])


    def process_attachments(self):
        attachments = self.msg.get('attachments', [])
        for attachment in attachments:
            if attachment.get('content_type') != 'application/vnd.microsoft.teams.card.o365connector':
                continue
            attachment_dict = json.loads(attachment.get('content'))
            return attachment_dict
        return dict()


    def get_summary(self):
        subject = self.msg.get('subject', '')
        title = self.attachment.get('title', '')
        summary = self.attachment.get('summary', '')

        text = 'Title: %s, Subject: %s, Summary: %s' % (title, subject, summary)
        summary_dict = {'text': text,
                        'metadata': {
                            'type': 'summary',
                            'msg_id': str(self.msg_id),
                            'msg_timestamp': str(self.timestamp),
                            'msg_sender': self.sender,
                            'subject': subject,
                            'title': title,
                            'summary': summary,
                        }}
        return summary_dict


    def get_replies(self):
        timestamp = self.timestamp
        msg_sender = self.sender

        reply_list = []
        for reply in self.replies:
            if reply.get('content_type') == 'html':
                try:
                    content = markdownify.markdownify(reply.get('content'))
                except RecursionError:
                    content = "ERROR"
            else:
                content = reply.get('content')

            reply_id = uuid.uuid4().hex
            reply_sender = reply.get('user', '')
            reply_timestamp = reply.get('timestamp', '')
            text = "Reply by %s at %s: %s" % (reply_sender, reply_timestamp, content)
            reply_dict = {'text': text,
                          'metadata': {
                              'type': 'reply',
                              'reply_id': str(reply_id),
                              'msg_id': str(self.msg_id),
                              'reply_timestamp': str(reply_timestamp),
                              'reply_sender': reply_sender,
                              'msg_timestamp': str(timestamp),
                              'msg_sender': msg_sender
                          }}
            reply_list.append(reply_dict)

        return reply_list


    def get_body(self):
        # Process the content of the message
        if self.msg.get('content_type') == 'html':
            content = markdownify.markdownify(self.msg.get('content')).strip()
        elif not self.msg.get('content'):
            content = ''
        else:
            content = self.msg.get('content').strip()

        attachment = ''
        activity_title = ''
        for section in self.attachment.get('sections', []):
            activity_title = section.get('activityTitle', '')
            if 'text' in section.keys():
                attachment += markdownify.markdownify(section['text']) + "\n"

        text = 'ActivityTitle: %s, Content: %s, Attachment: %s' % (activity_title, content, attachment)

        metadata = self.metadata_finder.find_metadata(text)

        body_dict = {'text': text,
                     'metadata': {
                         'type': 'body',
                         'msg_id': self.msg_id,
                         'msg_sender': self.sender,
                         'msg_timestamp': self.timestamp,
                         'activity_title': activity_title,
                         'ip_addresses': metadata.get('ip_addresses', []),
                         'networks': metadata.get('networks', []),
                         'domains': metadata.get('domains', []),
                         'urls': metadata.get('urls', []),
                         'email_addresses': metadata.get('email_addresses', []),
                         'mac_addresses': metadata.get('mac_addresses', []),
                         'netids': metadata.get('netids', []),
                         'sn_tickets': metadata.get('sn_tickets', [])
                     }}

        return body_dict