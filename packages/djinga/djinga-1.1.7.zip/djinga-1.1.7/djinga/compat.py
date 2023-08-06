try:
    from django.template.base import TemplateDoesNotExist, TemplateSyntaxError
except ImportError:
    # Django >= 1.9
    from django.template.exceptions import TemplateDoesNotExist, \
        TemplateSyntaxError
