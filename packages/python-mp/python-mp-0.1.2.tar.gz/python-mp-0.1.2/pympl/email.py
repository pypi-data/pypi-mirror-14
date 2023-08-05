from pympl.exc import (
    EmailError, StateError, AttachmentError, AddRecordError,
    EmailRecordCreationError, AttachFileError, NoRecipientsError,
    RecipientError
)
from pympl.table import Record
from datetime import datetime
import os


def _raise_state_error():
    raise StateError(
        "Cannot modify a Communication that has all ready been sent."
    )


def _require_attributes(obj, *attributes):
    for attribute in attributes:
        if not getattr(obj, attribute, None):
            raise AttributeError("%s.%s is requied" % (
                type(obj).__name__, attribute
            ))


def _fallback(record, format_string):
    return format_string.format(**record) if record else None


class EmailFactory(object):
    def __init__(self, client):
        self.client = client

    def __call__(self, *args, **kwargs):
        return Communication(self.client, *args, **kwargs)


class Communication(object):
    COMMUNICATION_READY_TO_SEND_ID = 3
    MESSAGE_READY_TO_SEND_ID = 2

    def __init__(
            self, client, subject=None, body=None, from_contact=None,
            from_name=None, from_email=None, reply_to_contact=None,
            reply_to_name=None, reply_to_email=None, author_user_id=None,
            start_date=None):
        self.client = client

        self._subject = subject
        self._body = body
        self._from_contact = self._get_contact(from_contact)
        self._from_name = from_name
        self._from_email = from_email
        self._reply_to_contact = self._get_contact(reply_to_contact)
        self._reply_to_name = reply_to_name
        self._reply_to_email = reply_to_email
        self._author_user_id = author_user_id
        self._start_date = start_date or datetime.now()

        self._sent = False
        self._recipients = []
        self._attachments = []

    @property
    def sent(self):
        return self._sent

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if self.sent:
            _raise_state_error()
        self._subject = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        if self.sent:
            _raise_state_error()
        self._body = value

    @property
    def from_contact(self):
        return self._from_contact

    @from_contact.setter
    def from_contact(self, value):
        if self.sent:
            _raise_state_error()
        self._from_contact = self._get_contact(value)

    @property
    def from_name(self):
        return self._from_name or _fallback(
            self._from_contact, '{First_Name} {Last_Name}')

    @from_name.setter
    def from_name(self, value):
        if self.sent:
            _raise_state_error()
        self._from_name = value

    @property
    def from_email(self):
        return self._from_email or _fallback(
            self._from_contact, '{Email_Address}')

    @from_email.setter
    def from_email(self, value):
        if self.sent:
            _raise_state_error()
        self._from_email = value

    @property
    def reply_to_contact(self):
        return self._reply_to_contact or self.from_contact

    @reply_to_contact.setter
    def reply_to_contact(self, value):
        if self.sent:
            _raise_state_error()
        self._reply_to_contact = self._get_contact(value)

    @property
    def reply_to_name(self):
        return self._reply_to_name or self.from_name

    @reply_to_name.setter
    def reply_to_name(self, value):
        if self.sent:
            _raise_state_error()
        self._reply_to_name = value

    @property
    def reply_to_email(self):
        return self._reply_to_email or self.from_email

    @reply_to_email.setter
    def reply_to_email(self, value):
        if self.sent:
            _raise_state_error()
        self._reply_to_email = value

    @property
    def author_user_id(self):
        return self._author_user_id

    @author_user_id.setter
    def author_user_id(self, value):
        if self.sent:
            _raise_state_error()
        self._author_user_id = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        if self.sent:
            _raise_state_error()
        self._start_date = value

    def _get_contact(self, contact):
        if isinstance(contact, Record):
            return contact
        elif isinstance(contact, int):
            return self.client.table.Contact(Contact_ID=contact)
        else:
            return contact

    def add_recipient(self, contact=None, **kwargs):
        if not isinstance(contact, Record):
            contact = dict(contact) if contact else {}
            contact.update(kwargs)
            contact = self.client.table.Contact(contact)

        if not any((contact.get('Display_Name'), contact.get('First_Name'))):
            raise RecipientError(
                "Recipient must have Display_Name or First_Name")
        elif not contact.get('Last_Name'):
            raise RecipientError("Recipient must have Last_Name")
        elif not contact.get('Email_Address'):
            raise RecipientError("Recipient must have Email_Address")

        self._recipients.append(contact)

        return self

    def add_attachment(
            self, file_obj, name=None, description=None, image=False):
        if name:
            pass
        elif hasattr(file_obj, 'name'):
            name = os.path.basename(file_obj.name)
        else:
            raise AttachmentError("Please provide a name for the attachment.")

        if not self.client.communications_page_id:
            raise AttachmentError(
                "The client has not been configured with a communications "
                "page_id. Without it, there's no way to know which page to "
                "attach files to."
            )

        self._attachments.append({
            'file': file_obj,
            'name': name,
            'description': description,
            'image': image
        })

        return self

    def send(self):
        _require_attributes(
            self, 'subject', 'body', 'from_name', 'from_email',
            'reply_to_contact', 'reply_to_name', 'reply_to_email',
            'start_date', 'author_user_id'
        )

        if not self._recipients:
            raise NoRecipientsError("Cannot send an email without recipients.")

        self._sent = True
        comm_ok, comm_record = self._create_communication_record()
        attachments_ok, attachments = self._attach_files(
            comm_record, comm_ok)
        messages_ok, messages = self._create_message_records(
            comm_record, comm_ok)

        return EmailResponse(
            comm_record,
            messages,
            attachments,
            comm_ok,
            messages_ok,
            attachments_ok
        )

    def _create_communication_record(self):
        ok = True
        comm_record = self.client.table.dp_Communications(
            Author_User_ID=self.author_user_id,
            Subject=self.subject,
            Body=self.body,
            Start_Date=self.start_date,
            Communication_Status_ID=self.COMMUNICATION_READY_TO_SEND_ID,
            From_Contact=self.from_contact.id,
            Reply_to_Contact=self.reply_to_contact.id,
            Template=0,
            Active=0
        )

        try:
            comm_record.save()
        except AddRecordError:
            ok = False

        return ok, comm_record

    def _attach_files(self, comm_record, comm_ok):
        ok = comm_ok
        attachments = []

        for i in self._attachments:
            attachment = self.client.fn.AttachFile(
                FileContents=i['file'],
                FileName=i['name'],
                PageID=self.client.communications_page_id,
                RecordID=comm_record.id,
                FileDescription=i['description'],
                IsImage=i['image']
            )
            attachments.append(attachment)

        return ok, attachments

    def _get_recipient_to(self, contact):
        return '"%s %s" <%s>' % (
            contact.get('Display_Name', contact.get('First_Name')),
            contact.get('Last_Name'),
            contact.get('Email_Address')
        )

    def _create_message_records(self, comm_record, comm_ok):
        ok = comm_ok
        messages = []

        for recipient in self._recipients:
            message = self.client.table.dp_Communication_Messages(
                Communication_ID=comm_record.id,
                Action_Status_ID=self.MESSAGE_READY_TO_SEND_ID,
                Action_Status_Time=datetime.now(),
                Contact_ID=recipient.id,
                From='"%s" <%s>' % (self.from_name, self.from_email),
                To=self._get_recipient_to(recipient),
                Reply_To='"%s" <%s>' % (
                    self.reply_to_name, self.reply_to_email),
                Subject=self.subject,
                Body=self.body,
                Deleted=0
            )
            messages.append(message)

            try:
                message.save()
            except AddRecordError:
                ok = False

        return ok, messages


class EmailResponse(object):
    def __init__(
            self, comm_record, messages, attachments, comm_ok, messages_ok,
            attachments_ok):
        self._comm_record = comm_record
        self._messages = messages
        self._attachments = attachments
        self._comm_ok = comm_ok
        self._messages_ok = messages_ok
        self._attachments_ok = attachments_ok

    @property
    def ok(self):
        return all((self._comm_ok, self._messages_ok, self._attachments_ok))
