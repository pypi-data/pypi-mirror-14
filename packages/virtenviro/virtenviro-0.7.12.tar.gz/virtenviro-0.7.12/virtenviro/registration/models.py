#~*~ coding: utf-8 ~*~
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from virtenviro.utils import id_generator


class UserProfile(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=10, choices=settings.LANGUAGES, default='ru')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    activation_code = models.CharField(max_length=255, verbose_name=_('Activation code'), null=True, blank=True)

    def clean(self):
        if not self.activation_code:
            self.activation_code = id_generator(size=20)

    def generate_activation_code(self):
        self.activation_code = id_generator(size=20)
        self.save()

    def repair_password(self):
        self.generate_activation_code()
        self.send_mail(
            template='repair',
            subject=u'Восстановление доступа к сайту {}'.format(Site.objects.get_current()))

    def send_activation_code(self):
        self.send_mail(
            template='registration',
            subject=u'Активация доступа к сайту {}'.format(Site.objects.get_current()))

    def send_mail(self, template, subject):
        from_email = getattr(settings, 'FROM_EMAIL', None)
        if from_email is None:
            return False

        context = {'profile': self, 'site': Site.objects.get_current()}
        text_content = render_to_string('accounts/email/{}.txt'.format(template), context)
        html_content = render_to_string('accounts/email/{}.html'.format(template), context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [self.user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True

    def __unicode__(self):
        return self.user.username


#def user_post_save(sender, instance, **kwargs):
#    (profile, new) = UserProfile.objects.get_or_create(user=instance)

#models.signals.post_save.connect(user_post_save, sender=User)
