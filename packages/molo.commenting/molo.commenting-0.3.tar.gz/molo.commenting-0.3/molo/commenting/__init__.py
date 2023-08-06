from molo.commenting.models import MoloComment
from molo.commenting.forms import MoloCommentForm


def get_model():
    return MoloComment


def get_form():
    return MoloCommentForm
