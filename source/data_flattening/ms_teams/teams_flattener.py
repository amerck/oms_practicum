import argparse
import json
import string
import markdownify


class Attachment:
    """
    Microsoft Teams Attachment Class
    """

    def __init__(self, attachment_template):
        """
        Initialize new message attachment object

        :param attachment_template: Template for output string
        """
        self.attachment_template = attachment_template
        self.title = ""
        self.summary = ""
        self.body = ""
        self.attachment = None


    def process_attachment(self, attachment):
        """
        Process attachment dictionary from ms_crawler.py

        :param attachment: Attachment dictionary
        :return: None
        """
        self.attachment = attachment
        self.title = self.attachment.get('title')
        self.summary = self.attachment.get('summary')
        for section in self.attachment.get('sections', []):
            if 'text' in section.keys():
                self.body += markdownify.markdownify(section.get('text'))


    def to_string(self):
        """
        Output Attachment object as string per Template specifications.

        :return: string representation of Attachment object
        """
        attachment_str = string.Template(self.attachment_template).substitute({'title': self.title,
                                                                               'summary': self.summary,
                                                                               'body': self.body})
        return attachment_str


class Reply:
    """
    Microsoft Teams Reply Class
    """

    def __init__(self, reply_template):
        """
        Initialize new message reply object

        :param reply_template: Template for output string
        """
        self.reply_template = reply_template
        self.timestamp = ""
        self.user = ""
        self.content = ""
        self.reply = None


    def process_reply(self, reply):
        """
        Process reply dictionary from ms_crawler.py

        :param reply: Reply dictionary
        :return: None
        """
        self.reply = reply
        self.timestamp = reply.get('timestamp')
        self.user = reply.get('user')

        if self.reply.get('content_type') == 'html':
            try:
                self.content = markdownify.markdownify(self.reply.get('content'))
            except RecursionError:
                self.content = "ERROR"
        else:
            self.content = self.reply.get('content')


    def to_string(self):
        """
        Output Reply object as string per Template specifications.

        :return: string representation of Reply object
        """
        reply_str = string.Template(self.reply_template).substitute({'timestamp': self.timestamp,
                                                                     'user': self.user,
                                                                     'content': self.content})
        return reply_str


class TeamsMessage:

    def __init__(self, message_template, attachment_template, reply_template):
        """
        Initialize new message object

        :param message_template: Template for Message output string
        :param attachment_template: Template for Attachment output string
        :param reply_template: Template for Reply output string
        """
        self.message_template = message_template
        self.attachment_template = attachment_template
        self.reply_template = reply_template
        self.id = ""
        self.subject = ""
        self.timestamp = ""
        self.sender = ""
        self.content = ""
        self.attachments = []
        self.replies = []
        self.msg = None


    def process_message(self, msg):
        """
        Process message dictionary from ms_crawler.py

        :param msg: Message dictionary
        :return: None
        """
        self.msg = msg
        self.sender = self.msg.get('user')
        self.timestamp = self.msg.get('timestamp')

        # Process the content of the message
        if self.msg.get('content_type') == 'html':
            self.content = markdownify.markdownify(self.msg.get('content')).strip()
        elif self.msg.get('content') == None:
            self.content = ''
        else:
            self.content = self.msg.get('content').strip()

        for attachment_dict in self.msg.get('attachments', []):
            if attachment_dict.get('content_type') != 'application/vnd.microsoft.teams.card.o365connector':
                continue
            attachment = Attachment(self.attachment_template)
            attachment.process_attachment(json.loads(attachment_dict.get('content')))
            self.attachments.append(attachment)

        for reply_dict in self.msg.get('replies', []):
            reply = Reply(self.reply_template)
            reply.process_reply(reply_dict)
            self.replies.append(reply)


    def to_string(self):
        """
        Output Message object as string per Template specifications.

        :return: String representation of Message object
        """
        attachment_str = ""
        for attachment in self.attachments:
            attachment_str += attachment.to_string() + "\n"

        reply_str = ""
        for reply in self.replies:
            reply_str += reply.to_string() + "\n"

        output_str = string.Template(self.message_template).substitute({'subject': self.subject,
                                                                        'timestamp': self.timestamp,
                                                                        'sender': self.sender,
                                                                        'content': self.content,
                                                                        'attachments': attachment_str,
                                                                        'replies': reply_str
                                                                        })
        return output_str


def main():
    parser = argparse.ArgumentParser(description="Microsoft Teams Message Flattener")
    parser.add_argument('-i', '--input', required=True,
                        help='JSON Teams Message file from ms_crawler.py output')
    parser.add_argument('-o', '--output', required=True,
                        help='Output filename')
    parser.add_argument('-t', '--template-dir', required=True,
                        help='Directory containing output template files')
    args = parser.parse_args()

    f_in = open(args.input, 'r')
    f_out = open(args.output, 'w')
    message_template = open("%s/message.template" % args.template_dir, 'r').read()
    attachment_template = open("%s/attachment.template" % args.template_dir, 'r').read()
    reply_template = open("%s/reply.template" % args.template_dir, 'r').read()

    for line in f_in.readlines():
        msg_dict = json.loads(line).get('message')
        msg = TeamsMessage(message_template=message_template,
                           attachment_template=attachment_template,
                           reply_template=reply_template)
        msg.process_message(msg_dict)
        f_out.write(msg.to_string() + "\n\n")
    f_in.close()
    f_out.close()
    return


if __name__ == "__main__":
    main()
