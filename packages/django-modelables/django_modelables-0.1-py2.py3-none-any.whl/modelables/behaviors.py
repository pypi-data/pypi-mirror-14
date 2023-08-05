#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .querysets import PublishableQuerySet, AuthorableQuerySet, DeactivableQuerySet, PrivatableQuerySet, \
    ModeratableQuerySet, PermissionableQuerySet, PermissionPrivatableQuerySet


class Permissionable(models.Model):
    users_granted = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(u"users with access"), blank=True, related_name='%(app_label)s_%(class)s')
    groups_granted = models.ManyToManyField(Group, verbose_name=_(u"groups with access"), blank=True, related_name='%(app_label)s_%(class)s')

    objects = PermissionableQuerySet.as_manager()

    class Meta:
        abstract = True
        app_label = _(u"modelables")

    def grant_access(self, user=None, group=None):
        if user:
            if user not in self.users_granted:
                self.users_granted.all().add(user)
        if group:
            if group not in self.groups_granted:
                self.groups_granted.all().add(user)

    def revoke_access(self, user=None, group=None):
        if user:
            if user in self.users_granted:
                self.users_granted.all().remove(user)
        if group:
            if group in self.groups_granted:
                self.groups_granted.all().remove(user)


class Privatable(models.Model):
    is_public = models.BooleanField(_(u"public?"), default=False)

    objects = PrivatableQuerySet.as_manager()

    class Meta:
        abstract = True
        app_label = 'modelables'

    def make_public(self):
        if not self.is_public:
            self.is_public = True
            self.save()

    def make_private(self):
        if self.is_public:
            self.is_public = False
            self.save()


class PermissionPrivatable(Permissionable, Privatable):
    objects = PermissionPrivatableQuerySet.as_manager()

    class Meta:
        abstract = True
        app_label = 'modelables'


class Authorable(models.Model):
    """
    Provides authoring feature. ''author'' field is a user, and is optional.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='%(app_label)s_%(class)s_authors')

    objects = AuthorableQuerySet.as_manager()

    class Meta:
        abstract = True
        app_label = _(u"modelables")


class Permalinkable(models.Model):
    """
    Provides a ''slug'' field with permalink features.
    """
    slug = models.SlugField(blank=True)

    class Meta:
        abstract = True
        app_label = _(u"modelables")

    def get_url_kwargs(self, **kwargs):
        kwargs.update(getattr(self, 'url_kwargs', {}))
        return kwargs

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.slug_source)
        super(Permalinkable, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        url_kwargs = self.get_url_kwargs(slug=self.slug)
        return self.url_name, (), url_kwargs


class UUIDPKable(models.Model):
    """
    Replace model AutoField 'id' with an UUID field
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
        app_label = _(u"modelables")


class UUIDable(models.Model):
    """
    Adds an UUID field
    """
    uuid = models.UUIDField(_(u"UUID"), default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
        app_label = _(u"modelables")


class Publishable(models.Model):
    """
    Provides publishing feature.
    """
    _publish_date = models.DateTimeField(null=True)
    _publisher = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='%(app_label)s_%(class)s_publishers')

    class Meta:
        abstract = True
        app_label = 'modelables'

    objects = PublishableQuerySet.as_manager()

    def publish(self, date=None, publisher=None):
        if not publisher:
            return False
        if not date:
            date = timezone.now()
        self._publish_date = date
        self.save()
        return True

    def unpublish(self):
        self._publish_date = None
        self._publisher = None
        self.save()

    @property
    def publish_date(self):
        return self._publish_date

    @property
    def publisher(self):
        return self._publisher

    @property
    def is_published(self):
        return self._publish_date < timezone.now()


class Timestampable(models.Model):
    """
    Provides self-updating ''creation_date'' and ''modified_date'' date fields.
    """
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        app_label = _(u"modelables")
        get_latest_by = "modified_date"
        ordering = ('-modified_date', '-created_date',)


class Deactivable(models.Model):
    """
    Provides object deactivation feature. Deactivation may be sometime in future.
    """
    _deactivation_date = models.DateTimeField(blank=True, null=True, db_index=True, editable=False)

    class Meta:
        abstract = True
        app_label = 'modelables'

    objects = DeactivableQuerySet.as_manager()

    def deactivate(self, deactivation_date=None):
        """
        :param deactivation_date:If not provided, ''deactivation_date'' = timezone.now()
        :return:None
        """
        self.deactivation_date = timezone.now() if deactivation_date is None else deactivation_date
        return self.save()

    def activate(self):
        self.deactivation_date = None
        return self.save()

    @property
    def is_active(self):
        if self._deactivation_date is None:
            return True
        else:
            return self._deactivation_date > timezone.now()


class Moderatable(models.Model):
    is_approved = models.BooleanField(_(u"approved?"), default=False)

    class Meta:
        abstract = True
        app_label = 'modelables'

    objects = ModeratableQuerySet.as_manager()

#
# class Scheduleable(models.Model):
#     # start_date = models.DateTimeField
#     # end_date = models.DateTimeField
#
#     class Meta:
#         app_label = 'modelables'


class Orderable(models.Model):
    position = models.PositiveIntegerField(_(u"position"), default=0)

    class Meta:
        abstract = True
        app_label = 'modelables'
        get_latest_by = 'position'
        ordering = ('position',)


    # next_element = models.OneToOneField('self', verbose_name=_(u"next"), editable=False, null=True, blank=True,
    #                                     related_name='previous')
    # is_first = models.BooleanField(_(u"first element?"), editable=False, default=False)
    #
    # class Meta:
    #     abstract = True
    #
    # def put_before(self, element):
    #     self.next_element = element.next_element
    #     element.next_element = self
    #     element.save()
    #     self.save()
    #     return True
    #
    # def put_after(self, element):
    #     previous_element = element.previous
    #     if previous_element:
    #         self.next_element = previous_element.next_element
    #         previous_element.next_element = self
    #     previous_element.save()
    #     self.save()
    #     return True
    #
    # def put_first(self):
    #     # TODO: Improve this!
    #     first = self.get_first()
    #     first.is_first = False
    #     self.next_element = first
    #     self.is_first = True
    #     self.save()
    #
    # def put_last(self):
    #     try:
    #         last = Orderable.objects.get(next_element=None)
    #     except MultipleObjectsReturned:
    #         return False
    #     last.next_element = self
    #     self.next_element = None
    #     last.save()
    #     self.save()
    #
    # def get_first(self):
    #     pass
