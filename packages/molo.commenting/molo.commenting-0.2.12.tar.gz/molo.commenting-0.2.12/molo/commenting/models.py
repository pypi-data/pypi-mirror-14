from django_comments.models import Comment
from django_comments.models import CommentFlag
from django.dispatch import receiver
from django_comments.signals import comment_was_flagged
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey


class MoloComment(MPTTModel, Comment):
    """
    Threaded comments - Add support for the parent comment store
    and MPTT traversal
    """

    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')

    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by = ['submit_date']

    class Meta:
        app_label = 'commenting'
        ordering = ['-submit_date', 'tree_id', 'lft']

    def flag_count(self, flag):
        return self.flags.filter(flag=flag).count()


@receiver(comment_was_flagged, sender=MoloComment)
def remove_comment_if_flag_limit(sender, comment, flag, created, **kwargs):
    # Auto removal is off by default
    try:
        threshold_count = settings.COMMENTS_FLAG_THRESHHOLD
    except AttributeError:
        return

    if flag.flag != CommentFlag.SUGGEST_REMOVAL:
        return
    # Don't remove comments that have been approved by a moderator
    if (comment.flag_count(CommentFlag.MODERATOR_APPROVAL) > 0):
        return

    if (comment.flag_count(CommentFlag.SUGGEST_REMOVAL) >= threshold_count):
        comment.is_removed = True
        comment.save()
