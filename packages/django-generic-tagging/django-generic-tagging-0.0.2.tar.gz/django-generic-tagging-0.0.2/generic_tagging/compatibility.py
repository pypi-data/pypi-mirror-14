try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    # for Django<=1.6
    from django.contrib.contenttypes.generic import GenericForeignKey
