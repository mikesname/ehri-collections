"""Actions to take when suggestions are made."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from django.core.mail import mail_admins
from django.template.loader import get_template
from django.template import Context

from suggestions import models


@receiver(post_save, sender=models.Suggestion)
def new_suggestion_mail(sender, **kwargs):
    """Send people an email when a suggestion is made."""
    instance = kwargs.pop("instance")
    plaintext = get_template('suggestions/email.txt')
    html = get_template('suggestions/email.html')

    subject = "Suggestion from %s" % instance.name
    d = Context(dict(object=instance, subject=subject))
    text_content = plaintext.render(d)
    html_content = html.render(d)
    mail_admins("Suggestion from: %s" % instance.name, text_content,
            html_message = html_content)


