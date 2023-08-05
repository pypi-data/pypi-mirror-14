#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import QuerySet, Q
from django.utils import timezone


class PermissionableQuerySet(QuerySet):
    use_for_related_fields = True

    def with_perms(self, user):
            return self.filter(
                Q(users_granted=user) |
                Q(groups_granted__user=user)
            )


class PrivatableQuerySet(QuerySet):
    use_for_related_fields = True

    def public(self):
        return self.filter(is_public=True)

    def private(self):
        return self.filter(is_public=False)


class PermissionPrivatableQuerySet(PermissionableQuerySet, PrivatableQuerySet):
    use_for_related_fields = True

    def can_access(self, user):
            return self.filter(
                Q(users_granted=user) |
                Q(groups_granted__user=user) |
                Q(is_public=True)
            )


class PublishableQuerySet(QuerySet):
    use_for_related_fields = True

    def published(self):
        return self.filter(~Q(publish_date=None)).filter(publish_date__lte=timezone.now())


class AuthorableQuerySet(QuerySet):
    use_for_related_fields = True

    def authored_by(self, author):
        return self.filter(author__username=author)


class DeactivableQuerySet(QuerySet):
    use_for_related_fields = True

    def active(self):
        return self.filter(Q(_deactivation_date=None) | Q(_deactivation_date__gt=timezone.now()))

    def inactive(self):
        return self.filter(_deactivation_date__lte=timezone.now())


class ModeratableQuerySet(QuerySet):
    use_for_related_fields = True

    def approved(self):
        return self.filter(is_approved=True)

    def rejected(self):
        return self.filter(is_approved=False)
