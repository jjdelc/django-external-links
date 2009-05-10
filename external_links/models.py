# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User

class LinkClick(models.Model):
    """
        Represents a click on an external link.
        Usage:
            clicked_link = LinkClick(link_url)
            clicked_link.store(request)
    """
    user = models.ForeignKey(User, null=True)
    link = models.CharField(max_length=512)
    referer = models.CharField(max_length=512)
    ip_addr = models.IPAddressField()
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def store(self, request):
        """
        Update params based on Request object
        """
        user = None
        if request.user.is_authenticated():
            user = request.user

        self.user = user
        self.referer = request.META.get('HTTP_REFERER','')
        self.ip_addr = request.META['REMOTE_ADDR']
        self.save()
