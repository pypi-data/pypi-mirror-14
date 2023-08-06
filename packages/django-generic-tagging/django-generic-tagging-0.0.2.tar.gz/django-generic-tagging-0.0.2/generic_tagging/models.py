from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import ugettext_lazy as _

from .exceptions import CannotReorderException, CannotDeleteLockedTagException

from .compatibility import GenericForeignKey


class TagManager(models.Manager):
    def get_for_object(self, object):
        '''Get tags which are belonged to the specific object
        :param obj: Object
        :return: tags
        '''
        ct = ContentType.objects.get_for_model(object)
        return self.filter(items__content_type=ct, items__object_id=object.pk).distinct()


class TaggedItemManager(models.Manager):
    def get_for_object(self, object):
        '''Get tagged items which are belongs to the specific object
        :param obj: Object
        :return: tagged items
        '''
        ct = ContentType.objects.get_for_model(object)
        return self.filter(content_type=ct, object_id=object.pk).distinct()

    def add(self, label, object, author):
        '''Add the tag to the specific object.
        If the tag named as 'label' is not exist, it will be created.
        :param label: Tag name
        :param object: Object
        :param author: Author
        :return: created tagged item
        '''
        if not author.has_perm('generic_tagging.add_tagged_item', obj=object):
            raise PermissionDenied('The user could not add the label to the object')
        ct = ContentType.objects.get_for_model(object)
        tag = Tag.objects.get_or_create(label=label)[0]
        tagged_item = self.create(tag=tag,
                                  content_type=ct,
                                  object_id=object.pk,
                                  author=author)
        return tagged_item

    def remove(self, label, object):
        '''Remove the tag from the specific object
        :param label: Tag name
        :param object: Object
        '''
        ct = ContentType.objects.get_for_model(object)
        self.filter(tag__label=label, content_type=ct, object_id=object.pk).delete()

    def clear(self, object):
        '''Clear all tagged item from the object
        :param object: Object
        '''
        ct = ContentType.objects.get_for_model(object)
        self.filter(content_type=ct, object_id=object.pk).delete()

    def get_tag_count(self, object):
        '''Get number of tags which are belonged to the specific object
        :param object:
        :return: number of tags
        '''
        ct = ContentType.objects.get_for_model(object)
        return self.filter(content_type=ct, object_id=object.pk).count()

    @staticmethod
    def swap_order(tagged_item, other_tagged_item):
        '''Swap the orders between two tagged items which are belonged to a same object
        If two tagged items owners are not same, then it will raise `ValidationError`.
        :param tagged_item: Tagged item
        :param other_tagged_item: Another tagged item
        '''
        if not (tagged_item.content_type.pk == other_tagged_item.content_type.pk and
                        tagged_item.object_id == other_tagged_item.object_id):
            raise CannotReorderException('These tags are not belonged to same object')
        temp = tagged_item.order
        tagged_item.order = other_tagged_item.order
        other_tagged_item.order = temp
        tagged_item.save()
        other_tagged_item.save()


class Tag(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)

    objects = TagManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.label

    @models.permalink
    def get_absolute_url(self):
        return ('generic_tagging_tag_detail', (), {'slug': self.label})


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_('Tag'), related_name='items')
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content type'))
    object_id = models.PositiveIntegerField(_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    locked = models.BooleanField(_('Locked'), default=False)
    order = models.IntegerField(_('Order'), default=0, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), related_name='items', null=True, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    objects = TaggedItemManager()

    class Meta:
        ordering = ('order', 'created_at')
        unique_together = ('tag', 'content_type', 'object_id')
        verbose_name = _('Tagged item')
        verbose_name_plural = _('Tagged items')
        permissions = (
            ('lock_tagged_item', 'Can lock tagged item'),
            ('unlock_tagged_item', 'Can unlock tagged item'),
        )

    def __str__(self):
        return '{} {}'.format(str(self.tag), str(self.content_object))

    def delete(self, *args, **kwargs):
        if self.locked:
            raise CannotDeleteLockedTagException('Can not delete locked tag')
        return super().delete(*args, **kwargs)

    def lock(self):
        '''Lock this tag
        :param by_user: User who attempt to lock
        '''
        if self.locked:
            raise ValidationError('''The tagged item is already locked''')
        self.locked = True
        self.save()

    def unlock(self):
        '''Unlock this tag
        :param by_user:
        '''
        if not self.locked:
            raise ValidationError('''The tagged item is already unlocked''')
        self.locked = False
        self.save()
