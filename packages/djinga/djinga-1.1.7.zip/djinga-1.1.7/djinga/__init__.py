from .version import __version__, __version_info__
from .environment import Environment

try:
    from django.template.base import add_to_builtins
    add_to_builtins('djinga.templatetags.djinga_tags')
except ImportError:
    # Django >= 1.9 hack
    from django.template import engine
    engine.Engine.default_builtins.append('djinga.templatetags.djinga_tags')

from . import ext
