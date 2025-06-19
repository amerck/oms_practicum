from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError


class GraphDB:

    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri=uri, auth=(username, password))


    def store_sn_ticket(self, data):

        def sn_ticket(tx):
            sys_id = data.get('sys_id', '') #
            number = data.get('number', '') #
            opened_by = data.get('opened_by', '') #
            opened_at = data.get('opened_at', '') #
            closed_at = data.get('closed_at', '') #
            sys_created_by = data.get('sys_created_by', '') #
            priority = data.get('priority', '') #
            short_description = data.get('short_description', '') #
            description = data.get('description', '') #
            urgency = data.get('urgency', '') #

            query = ('MERGE (s:SNTicket {sys_id: $sys_id, number: $number}) '
                     'SET s.opened_by = $opened_by, s.opened_at = $opened_at, s.closed_at = $closed_at, '
                     's.sys_created_by = $sys_created_by, s.priority = $priority, '
                     's.short_description = $short_description, s.description = $description, s.urgency = $urgency')
            tx.run(query, sys_id=sys_id, number=number, opened_by=opened_by, opened_at=opened_at, closed_at=closed_at,
                   sys_created_by=sys_created_by, priority=priority, short_description=short_description,
                   description=description, urgency=urgency)

        try:
            with self.driver.session() as session:
                session.execute_write(sn_ticket)
        except Neo4jError as e:
            print(f"[Neo4j Error] {e.__class__.__name__}: {e}")


    def store_sn_work_note(self, data, text):

        def sn_work_note(tx):
            ticket_sys_id = data.get('ticket_sys_id', '')
            number = data.get('number')
            timestamp = data.get('timestamp')
            sender = data.get('sender')
            note_type = data.get('note_type')

            query = ('MERGE (s:SNTicket {sys_id: $ticket_sys_id, number: $number}) '
                     'MERGE (w:WorkNote {number: $number, timestamp: $timestamp, '
                             'sender: $sender, note_type: $note_type, text: $text})'
                     'MERGE (s)-[:CONTAINS]->(w)')
            tx.run(query, ticket_sys_id=ticket_sys_id, number=number, timestamp=timestamp,
                   sender=sender, note_type=note_type, text=text)

        try:
            with self.driver.session() as session:
                session.execute_write(sn_work_note)
        except Neo4jError as e:
            print(f"[Neo4j Error] {e.__class__.__name__}: {e}")

    def store_alert_summary(self, data):

        def teams_summary(tx):
            msg_id = data.get('msg_id', '')
            title = data.get('title', '')

            subject = data.get('subject', '')
            if not subject:
                subject = ''

            summary = data.get('summary', '')
            msg_timestamp = data.get('msg_timestamp', '')
            msg_sender = data.get('msg_sender', '')
            query = ('MERGE (a:TeamsAlert {mId: $msg_id}) '
                     'SET a.title = $title, a.subject = $subject, a.summary = $summary, '
                         'a.timestamp = datetime($msg_timestamp) '
                     'MERGE (u:User {name: $msg_sender})'
                     'MERGE (u)-[:SENT]->(a)')
            tx.run(query, msg_id=msg_id, title=title, subject=subject,
                   summary=summary, msg_timestamp=msg_timestamp, msg_sender=msg_sender)

        try:
            with self.driver.session() as session:
                session.execute_write(teams_summary)
        except Neo4jError as e:
            print(f"[Neo4j Error] {e.__class__.__name__}: {e}")


    def query_alert_summary(self):

        def alert_summary(tx):
            query = ('MATCH (a:TeamsAlert {mId: "2790efe3af9347c3ae77b0cc112fdca1"})'
                     'RETURN a')
            return tx.run(query).data()

        try:
            with self.driver.session() as session:
                return session.execute_read(alert_summary)
        except Neo4jError as e:
            print(f"[Neo4j Error] {e.__class__.__name__}: {e}")


    def store_teams_body(self, data, text):

        def teams_body(tx):
            msg_id = data.get('msg_id', '')
            activity_title = data.get('activity_title', '')
            msg_timestamp = data.get('msg_timestamp', '')
            msg_sender = data.get('msg_sender', '')
            query = ('MERGE (a:TeamsAlert {mId: $msg_id}) '
                     'SET a.activity_title = $activity_title, a.text = $text, a.timestamp = datetime($msg_timestamp) '
                     'MERGE (u:User {name: $msg_sender}) '
                     'MERGE (u)-[:SENT]->(a) ')
            tx.run(query, msg_id=msg_id, activity_title=activity_title, text=text,
                   msg_timestamp=msg_timestamp, msg_sender=msg_sender)

            ip_addresses = data.get('ip_addresses', [])
            if ip_addresses:
                query = ('MATCH (a:TeamsAlert {mId: $msg_id}) '
                         'WITH a '
                         'UNWIND $ip_addresses AS ip '
                         'MERGE (i:IP {value: ip}) '
                         'MERGE (a)-[:REFERENCES]->(i)')
                tx.run(query, msg_id=msg_id, ip_addresses=ip_addresses)

            networks = data.get('networks', [])
            if networks:
                query = ('MATCH (a:TeamsAlert {mId: $msg_id}) '
                         'WITH a '
                         'UNWIND $networks AS network '
                         'MERGE (n:Network {value: network}) '
                         'MERGE (a)-[:REFERENCES]->(n)')
                tx.run(query, msg_id=msg_id, networks=networks)

            mac_addresses = data.get('mac_addresses', [])
            if mac_addresses:
                query = ('MATCH (a:TeamsAlert {mId: $msg_id}) '
                         'WITH a '
                         'UNWIND $mac_addresses AS mac '
                         'MERGE (m:MAC {value: mac}) '
                         'MERGE (a)-[:REFERENCES]->(m)')
                tx.run(query, msg_id=msg_id, mac_addresses=mac_addresses)

            urls = data.get('urls', [])
            if urls:
                query = ('MATCH (a:TeamsAlert {mId: $msg_id}) '
                         'WITH a '
                         'UNWIND $urls AS url '
                         'MERGE (u:URL {value: url}) '
                         'MERGE (a)-[:REFERENCES]->(u)')
                tx.run(query, msg_id=msg_id, urls=urls)

            email_addresses = data.get('email_addresses', [])
            if email_addresses:
                query = ('MATCH (a:TeamsAlert {mId: $msg_id}) '
                         'WITH a '
                         'UNWIND $email_addresses AS email_address '
                         'MERGE (e:EmailAddr {value: email_address}) '
                         'MERGE (a)-[:REFERENCES]->(e)')
                tx.run(query, msg_id=msg_id, email_addresses=email_addresses)

            domains = data.get('domains', [])
            if domains:
                query = ('MATCH (a:TeamsAlert {mId: $msg_id}) '
                         'WITH a '
                         'UNWIND $domains AS domain '
                         'MERGE (d:Domain {value: domain}) '
                         'MERGE (a)-[:REFERENCES]->(d)')
                tx.run(query, msg_id=msg_id, domains=domains)

            netids = data.get('netids', [])
            if netids:
                query = ('MATCH (a:TeamsAlert {mId: $msg_id}) '
                         'WITH a '
                         'UNWIND $netids AS netid '
                         'MERGE (n:NetID {value: netid}) '
                         'MERGE (a)-[:REFERENCES]->(n)')
                tx.run(query, msg_id=msg_id, netids=netids)

            sn_tickets = data.get('sn_tickets', [])
            if sn_tickets:
                query = ('MATCH (a:TeamsAlert {mId: $msg_id}) '
                         'WITH a '
                         'UNWIND $sn_tickets AS sn_ticket '
                         'MATCH (s:SNTicket {number: sn_ticket})'
                         'MERGE (a)-[:REFERENCES]->(s)')
                tx.run(query, msg_id=msg_id, sn_tickets=sn_tickets)

        try:
            with self.driver.session() as session:
                session.execute_write(teams_body)
        except Neo4jError as e:
            print(f"[Neo4j Error] {e.__class__.__name__}: {e}")


    def store_teams_reply(self, data, text):

        def teams_reply(tx):
            reply_id = data.get('reply_id', '')
            msg_id = data.get('msg_id', '')
            reply_timestamp = data.get('reply_timestamp', '')
            reply_sender = data.get('reply_sender', '')
            query = ('MERGE (a:TeamsAlert {mId: $msg_id})'
                     'MERGE (r:Reply {rID: $reply_id, mId: a.mId, text: $text, timestamp: datetime($reply_timestamp)})'
                     'MERGE (u:User {name: $reply_sender})'
                     'MERGE (a)-[:CONTAINS]->(r)'
                     'MERGE (u)-[:SENT]->(r)')
            tx.run(query, msg_id=msg_id, reply_id=reply_id, text=text,
                   reply_timestamp=reply_timestamp, reply_sender=reply_sender)
        try:
            with self.driver.session() as session:
                session.execute_write(teams_reply)
        except Neo4jError as e:
            print(f"[Neo4j Error] {e.__class__.__name__}: {e}")
