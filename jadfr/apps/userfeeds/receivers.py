__author__ = 'j_schn14'

from django.db.models.signals import pre_save
from .models import UserFeedEntry


def update_rank(sender, *args, **kwargs):
    isinstance = kwargs['instance']
    isinstance.update_rank()


pre_save.connect(update_rank, UserFeedEntry)