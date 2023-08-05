# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.base import ContentFile
from django.core.mail.backends.base import BaseEmailBackend

from .models import Email, EmailAlternative, EmailAttachment

class DBEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for msg in email_messages:
            try:
                email = Email.objects.create(
                    subject=msg.subject,
                    body=msg.body,
                    content_subtype=msg.content_subtype,
                    from_email=msg.from_email,
                    to='; '.join(msg.to),
                    cc='; '.join(msg.cc),
                    bcc='; '.join(msg.bcc),
                    headers='\n'.join('{}: {}'.format(k, v)
                                      for k, v in msg.extra_headers),
                )
                alternatives = getattr(msg, 'alternatives', [])
                for content, mimetype in alternatives:
                    EmailAlternative.objects.create(
                        email=email,
                        content=content,
                        mimetype=mimetype or '',
                    )

                for filename, content, mimetype in msg.attachments:
                    attachment = EmailAttachment.objects.create(
                        email=email,
                        filename=filename,
                        mimetype=mimetype or '',
                    )
                    attachment.file.save(filename, ContentFile(content))
            except:
                if not self.fail_silently:
                    raise

        return len(email_messages)
