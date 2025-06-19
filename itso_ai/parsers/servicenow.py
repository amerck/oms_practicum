import re
import string
import markdownify


class SNParser:

    def __init__(self, ticket):
        """
        Initialize new ticket object
        """
        self.ticket = ticket
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
        self.work_notes = []

        self._process_ticket()
        self._process_work_notes()


    def _process_ticket(self):
        """
        Process ticket dictionary from sn_crawler.py

        :return: None
        """
        assigned_to = self.ticket.get('assigned_to')
        if isinstance(assigned_to, dict):
            self.assigned_to = assigned_to.get('display_value')
        else:
            self.assigned_to = assigned_to

        assignment_group = self.ticket.get('assignment_group')
        if isinstance(assignment_group, dict):
            self.assignment_group = assignment_group.get('display_value')
        else:
            self.assignment_group = assignment_group

        self.closed_at = self.ticket.get('closed_at')
        self.impact = self.ticket.get('impact')
        self.number = self.ticket.get('number')

        opened_by = self.ticket.get('opened_by')
        if isinstance(opened_by, dict):
            self.opened_by = opened_by.get('display_value')
        else:
            self.opened_by = opened_by

        self.opened_at = self.ticket.get('opened_at')
        self.priority = self.ticket.get('priority')

        service_offering = self.ticket.get('service_offering')
        if isinstance(service_offering, dict):
            self.service_offering = service_offering.get('display_value')
        else:
            self.service_offering = service_offering

        self.short_description = self.ticket.get('short_description')
        self.sys_created_by = self.ticket.get('sys_created_by')
        self.sys_created_on = self.ticket.get('sys_created_on')
        self.sys_id = self.ticket.get('sys_id')
        self.sys_updated_on = self.ticket.get('sys_updated_on')
        self.u_application = self.ticket.get('u_application')

        u_it_service = self.ticket.get('u_it_service')
        if isinstance(u_it_service, dict):
            self.u_it_service = u_it_service.get('display_value')
        else:
            self.u_it_service = u_it_service

        u_service_provider = self.ticket.get('u_service_provider')
        if isinstance(u_service_provider, dict):
            self.u_service_provider = u_service_provider.get('display_value')
        else:
            self.u_service_provider = u_service_provider

        self.urgency = self.ticket.get('urgency')

        self.description = self.handle_markdown(self.ticket.get('description'))
        self.close_notes = self.handle_markdown(self.ticket.get('close_notes'))


    def _process_work_notes(self):
        pattern = (
            r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - '  # timestamp
            r'(?P<sender>.+?) '  # sender
            r'\((?P<type>Work notes|User communication)\)\n'  # type in ()
            r'(?P<message>.*?)(?=(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) -|\Z)'  # message until next timestamp or end
        )

        work_note_list = list()

        comments_and_work_notes = self.ticket.get('comments_and_work_notes', '')
        matches = re.finditer(pattern, comments_and_work_notes, re.DOTALL)
        for m in matches:
            message = m.group('message')
            work_note = {'timestamp': m.group('timestamp'),
                         'sender': m.group('sender'),
                         'type': m.group('type'),
                         'message': self.handle_markdown(message)}
            work_note_list.append(work_note)
        self.work_notes = work_note_list


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


    def get_ticket_body(self):
        """
        Convert ticket into embeddable dictionary.

        :return: ticket dictionary
        """
        text = "Short Description: %s, Description: %s\n" % (self.short_description, self.description)
        ticket_body_dict = {'text': text,
                            'metadata': {
                                'type': 'ticket_body',
                                'sys_id': self.sys_id,
                                'number': self.number,
                                'assigned_to': self.assigned_to,
                                'assignment_group': self.assignment_group,
                                'closed_at': self.closed_at,
                                'description': self.description,
                                'impact': self.impact,
                                'opened_by': self.opened_by,
                                'opened_at': self.opened_at,
                                'priority': self.priority,
                                'service_offering': self.service_offering,
                                'short_description': self.short_description,
                                'sys_created_by': self.sys_created_by,
                                'sys_created_on': self.sys_created_on,
                                'u_application': self.u_application,
                                'u_it_service': self.u_it_service,
                                'u_service_provider': self.u_service_provider,
                                'urgency': self.urgency
                            }}
        return ticket_body_dict


    def get_work_notes(self):
        """
        Convert work notes into embeddable dictionary.

        :return: work note dictionary
        """
        work_note_list = []
        for work_note in self.work_notes:
            work_note_dict = {'text': work_note.get('message'),
                              'metadata': {
                                  'type': 'work_note',
                                  'ticket_sys_id': self.sys_id,
                                  'number': self.number,
                                  'timestamp': work_note.get('timestamp'),
                                  'sender': work_note.get('sender'),
                                  'note_type': work_note.get('type')
                              }}
            work_note_list.append(work_note_dict)
        return work_note_list


    def to_dict(self):
        """
        Convert ticket data to dict.

        :return: Ticket dictionary
        """
        output_dict = {'assigned_to': self.assigned_to,
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
                       'urgency': self.urgency,
                       'work_notes': self.work_notes}
        return output_dict


    def to_string(self, template):
        """
        Output Ticket object as string per Template specifications.

        :return: String representation of Ticket object
        """
        output_str = string.Template(template).substitute({'assigned_to': self.assigned_to,
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
