from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from mptt.models import MPTTModel, TreeForeignKey


class FileCollectionChildMixin:
    """ Provides common methods for Files/Directories.
    """
    def get_parent_hash(self):
        """ Returns the hash of this object's parent, or '' if this is the
            root of the tree.
        """
        if self.parent:
            return self.parent.get_hash()
        else:
            return ''


class Directory(MPTTModel, FileCollectionChildMixin):
    """ A Directory in the file structure of a FileCollection. May contain
        child Directory and File objects.

        TODO prevent directories which are not auto-created root nodes from
             being saved with no parent.
    """
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='dirs')
    collection = models.ForeignKey('FileCollection')

    class Meta:
        verbose_name_plural = 'directories'
        unique_together = ('name', 'parent')

    def __unicode__(self):
        return self.name

    def get_hash(self):
        return '%s_d%s' % (self.collection.get_volume_id(), self.id)

    def get_info(self):
        """ Returns an object to represent this object in elFinder. Populates
            'cwd' in response to 'open' command.

            If the object is the root dir, 'volume_id' is included in the
            response.
        """
        obj = {'name': self.name,
               'hash': self.get_hash(),
               'phash': self.get_parent_hash(),
               'mime': 'directory',
               'read': 1,
               'write': 1,
               'size': 0,
               'dirs': 0 if (self.dirs.count() == 0) else 1
               }

        if not self.parent:
            obj['volume_id'] = self.collection.get_volume_id()
            obj['locked'] = 1
            obj['name'] = self.collection.name

        return obj


class FileCollection(models.Model):
    """ A collection of Directory and File objects.

        # TODO delete files/dirs when deleting file collection
    """
    name = models.CharField(max_length=255, unique=True)
    #tree_id = models.CharField(
    #root_node = models.OneToOneField(Directory)

    def save(self, *args, **kwargs):
        """ Creates a Directory (root node) when the FileCollection is first
            created.
        """
        created = (self.id is None)
        super(FileCollection, self).save(*args, **kwargs)
        if created:
            root_dir = Directory(name='root_node_%s' % self.id,
                                 collection=self)
            root_dir.save()

    def __unicode__(self):
        return self.name

    def get_volume_id(self):
        return 'fc%s' % self.id


class File(models.Model, FileCollectionChildMixin):
    """ A File in a FileCollection.
    """
    name = models.CharField(max_length=255)
    parent = TreeForeignKey(Directory, null=True, blank=True,
                            related_name='files')
    content = models.TextField(max_length=2048, blank=True)
    collection = models.ForeignKey('FileCollection')

    class Meta:
        unique_together = ('name', 'parent')

    def __unicode__(self):
        return self.name

    def get_hash(self):
        return '%s_f%s' % (self.collection.get_volume_id(), self.id)

    def get_info(self):
        """ Returns an object to represent this object in elFinder. Populates
            'cwd' in response to 'open' command.
        """
        return {'name': self.name,
                'hash': self.get_hash(),
                'phash': self.get_parent_hash(),
                'mime': 'text/plain',
                'size': len(self.content),
                'read': True,
                'write': True,
                'rm': True}
