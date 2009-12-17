# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.cache import cache

BLOCKED_IPS_LIST = 'external-link:blocked-ips'

class LinkClick(models.Model):
    """
        Represents a click on an external link.
        Usage:
            clicked_link = LinkClick(link_url)
            clicked_link.store(request)
    """
    user = models.ForeignKey(User, null=True)
    site = models.ForeignKey(Site)
    link = models.CharField(max_length=512)
    referer = models.CharField(max_length=512)
    ip_addr = models.IPAddressField()
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def store(self, request):
        """
        Update params based on Request object
        """
        ip_addr = request.META['REMOTE_ADDR']

        if ip_addr in BlockedIp.objects.get_ips():
            # If it's a blocked IP, dont do anything 
            return None

        user = None
        if request.user.is_authenticated():
            user = request.user

        self.user = user
        self.site = Site.objects.get_current()
        self.referer = request.META.get('HTTP_REFERER','')
        self.ip_addr = ip_addr
        self.save()

class BlockedManager(models.Manager):
    
    def get_ips(self):
        """
        Returns a cached list of ip addresses
        """
        result = cache.get(BLOCKED_IPS_LIST, None)

        if not result:
            result = self.values_list('ip_addr', flat=True)
            cache.set(BLOCKED_IPS_LIST, result, 60*60*24) # 1 day?

        return result

class BlockedIp(models.Model):
    """
    Contains a list of IPs that shouldn't be tracked, such as search engines
    crawlers, etc.
    """
    ip_addr = models.IPAddressField()
    name = models.CharField(max_length=128, blank=True)

    objects = BlockedManager()

    def __unicode__(self):
        return self.ip_addr

    def save(self, *args, **kwargs):
        """
        Clear the cached list of blocked IPs
        """
        cache.delete(BLOCKED_IPS_LIST)
        super(BlockedIp, self).save(*args, **kwargs)
