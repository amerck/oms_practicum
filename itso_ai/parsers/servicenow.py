import re
import string
import markdownify


class SNParser:

    def __init__(self, ticket_template):
        """
        Initialize new ticket object

        :param ticket_template: Template for Ticket output string
        """
        self.ticket_template = ticket_template
        self.assigned_to = ''
        self.assignment_group = ''
        self.close_notes = ''
        self.closed_at = ''
        self.description = ''
        self.impact = ''
        self.number = ''
        self.opened_by = ''
        self.opened_at = ''
        self.priority = ''
        self.service_offering = ''
        self.short_description = ''
        self.sys_created_by = ''
        self.sys_created_on = ''
        self.sys_id = ''
        self.sys_updated_on = ''
        self.u_application = ''
        self.u_it_service = ''
        self.u_service_provider = ''
        self.urgency = ''
        self.ticket = None

    def process_ticket(self, ticket):
        """
        Process ticket dictionary from sn_crawler.py

        :param ticket: Ticket dictionary
        :return: None
        """
        self.ticket = ticket
        self.assigned_to = ticket.get('assigned_to')
        self.assignment_group = ticket.get('assignment_group')
        self.closed_at = ticket.get('closed_at')
        self.impact = ticket.get('impact')
        self.number = ticket.get('number')
        self.opened_by = ticket.get('opened_by')
        self.opened_at = ticket.get('opened_at')
        self.priority = ticket.get('priority')
        self.service_offering = ticket.get('service_offering')
        self.short_description = ticket.get('short_description')
        self.sys_created_by = ticket.get('sys_created_by')
        self.sys_created_on = ticket.get('sys_created_on')
        self.sys_id = ticket.get('sys_id')
        self.sys_updated_on = ticket.get('sys_updated_on')
        self.u_application = ticket.get('u_application')
        self.u_it_service = ticket.get('u_it_service')
        self.u_service_provider = ticket.get('u_service_provider')
        self.urgency = ticket.get('urgency')

        self.description = self.handle_markdown(ticket.get('description'))
        self.close_notes = self.handle_markdown(ticket.get('close_notes'))


    @staticmethod
    def handle_markdown(text):
        """
        Convert HTML to Markdown in ticket text.

        :param text: Text to convert to Markdown
        :return: Updated text
        """
        code_regex = r'\[code\](.+?)\[/code\]'
        r = re.search(code_regex, text, re.DOTALL)
        if not r:
            return text
        span = r.span()
        prefix = text[:span[0]]
        code = text[span[0]:span[1]]
        suffix = text[span[1]:]
        code_md = markdownify.markdownify(code)
        return prefix + code_md + suffix


    def to_string(self):
        """
        Output Ticket object as string per Template specifications.

        :return: String representation of Ticket object
        """
        output_str = string.Template(self.ticket_template).substitute({'assigned_to': self.assigned_to,
                                                                       'assignment_group': self.assignment_group,
                                                                       'close_notes': self.close_notes,
                                                                       'closed_at': self.closed_at,
                                                                       'description': self.description,
                                                                       'impact': self.impact,
                                                                       'number': self.number,
                                                                       'opened_by': self.opened_by,
                                                                       'opened_at': self.opened_at,
                                                                       'priority': self.priority,
                                                                       'service_offering': self.service_offering,
                                                                       'short_description': self.short_description,
                                                                       'sys_created_by': self.sys_created_by,
                                                                       'sys_created_on': self.sys_created_on,
                                                                       'sys_id': self.sys_id,
                                                                       'sys_updated_on': self.sys_updated_on,
                                                                       'u_application': self.u_application,
                                                                       'u_it_service': self.u_it_service,
                                                                       'u_service_provider': self.u_service_provider,
                                                                       'urgency': self.urgency})
        return output_str