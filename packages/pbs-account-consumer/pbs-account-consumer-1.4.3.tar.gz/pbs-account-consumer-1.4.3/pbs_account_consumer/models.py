# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Nonce(models.Model):
    server_url = models.CharField(max_length=2047)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    def __unicode__(self):
        return "Nonce: %s, %s" % (self.server_url, self.salt)


class Association(models.Model):
    server_url = models.TextField(max_length=2047)
    handle = models.CharField(max_length=255)
    secret = models.TextField(max_length=255)  # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField(max_length=64)

    def __unicode__(self):
        return "Association: %s, %s" % (self.server_url, self.handle)


def delete_openid_user(sender, instance=None, **kwargs):
    """ Cleanup method for user removal.
    Makes sure that related table info is removed as well.
    """
    if instance:
        try:
            openid_user = UserOpenID.objects.get(user=instance)
            openid_user.delete()
        except UserOpenID.DoesNotExist:
            pass

pre_delete.connect(delete_openid_user, sender=USER_MODEL)


class UserOpenID(models.Model):
    user = models.ForeignKey(USER_MODEL)
    claimed_id = models.CharField(max_length=255, unique=True)
    display_id = models.TextField(max_length=2047)

    def update_openid_identifiers(self, claimed_id, display_id):
        self.claimed_id = claimed_id
        self.display_id = display_id
        self.save()

    @classmethod
    def by_identity_url(cls, identity_url, default=None):
        try:
            return cls.objects.get(claimed_id__exact=identity_url)
        except cls.DoesNotExist:
            return default

    @classmethod
    def by_user_email(cls, email, default=None):
        try:
            return cls.objects.get(user__email=email)
        except cls.DoesNotExist:
            return default
