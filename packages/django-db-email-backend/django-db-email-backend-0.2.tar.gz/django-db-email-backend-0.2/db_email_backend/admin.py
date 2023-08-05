# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Email, EmailAlternative, EmailAttachment


class EmailAlternativeInline(admin.StackedInline):
    model = EmailAlternative
    readonly_fields = ('mimetype', 'content')
    extra = 0
    max_num = 0
    can_delete = False


class EmailAttachmentInline(admin.StackedInline):
    model = EmailAttachment
    readonly_fields = ('filename', 'mimetype', 'file')
    extra = 0
    max_num = 0
    can_delete = False


class EmailAdmin(admin.ModelAdmin):
    fields = (
        ('from_email', 'create_date', 'content_subtype'),
        ('to', 'cc', 'bcc'),
        'subject', 'body', 'headers')
    readonly_fields = (
        'create_date','from_email', 'to', 'cc', 'bcc', 'subject', 'body', 'content_subtype', 'headers')
    list_display = ('subject', 'to', 'from_email', 'create_date', 'attachment_count', 'alternative_count')
    list_filter = ('content_subtype',)
    date_hierarchy = 'create_date'
    search_fields = ('to', 'from_email', 'cc', 'bcc', 'subject', 'body')
    inlines = (EmailAlternativeInline, EmailAttachmentInline)

    def attachment_count(self, instance):
        return instance.attachments.count()
    attachment_count.short_description = 'Attachments'

    def alternative_count(self, instance):
        return instance.alternatives.count()
    alternative_count.short_description = 'Alternatives'

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Email, EmailAdmin)


