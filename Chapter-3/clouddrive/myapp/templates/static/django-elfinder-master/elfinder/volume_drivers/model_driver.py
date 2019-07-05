from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render_to_response
from django.template import RequestContext
from elfinder.volume_drivers.base import BaseVolumeDriver
from elfinder import models
import logging


logger = logging.getLogger(__name__)


class ModelVolumeDriver(BaseVolumeDriver):
    def __init__(self, collection_id,
                 collection_model=models.FileCollection,
                 directory_model=models.Directory,
                 file_model=models.File,
                 *args, **kwargs):

        super(ModelVolumeDriver, self).__init__(*args, **kwargs)
        self.collection_model = collection_model
        self.directory_model = directory_model
        self.file_model = file_model

        self.collection = self.collection_model.objects.get(pk=collection_id)

    def get_volume_id(self):
        return 'fc%s' % self.collection.id

    def get_info(self, hash):
        return self.get_object(hash).get_info()

    def get_tree(self, target, ancestors=False, siblings=False):
        """ Returns a list of dicts describing children/ancestors/siblings of
            the target directory.

            Siblings of the root node are always excluded, as they refer to
            root directories of other file collections.
        """
        dir = self.get_object(target)
        tree = []

        # Add children to the tree first
        for item in dir.get_children():
            tree.append(item.get_info())
        for item in dir.files.all():
            tree.append(item.get_info())

        # Add ancestors next, if required
        if ancestors:
            for item in dir.get_ancestors(include_self=True):
                tree.append(item.get_info())
                for ancestor_sibling in item.get_siblings():
                    if ancestor_sibling.parent:
                        tree.append(ancestor_sibling.get_info())

        # Finally add siblings, if required
        if siblings:
            for item in dir.get_siblings():
                if item.parent:
                    tree.append(item.get_info())

        return tree

    def get_object(self, hash):
        """ Returns the object specified by the given hash.

            The hash is in the format "y_xn", where y is the volume_id,
            x is a letter identifying the type of object being requested and
            n is that object's id.

            d:  Directory
            f:  File

            The tree_id of the root node of the currently open FileCollection
            is checked to ensure the target belongs to that tree.
            The client requests the last-remembered dir on init, which breaks
            things if they are now looking at a different FileCollection.

            If the target does not belong to the current tree, return the root
            of the current tree instead.
        """
        if hash == '':
            # No target has been specified so return the root directory.
            return self.directory_model.objects.get(parent=None,
                                                    collection=self.collection)

        try:
            volume_id, object_hash = hash.split('_')
        except ValueError:
            raise Exception('Invalid target hash: %s' % hash)

        try:
            object_id = int(object_hash[1:])
        except ValueError:
            raise Exception('Invalid target hash: %s' % object_hash)

        # Figure which type of object is being requested
        if object_hash[0] == 'f':
            model = self.file_model
        elif object_hash[0] == 'd':
            model = self.directory_model
        else:
            raise Exception('Invalid target hash: %s' % object_hash)

        try:
            object = model.objects.get(pk=object_id,
                                       collection=self.collection.id)
        except ObjectDoesNotExist:
            raise Exception('Could not open target')

        return object

    def _create_object(self, name, parent_hash, model):
        """ Helper function to create objects (files/directories).
        """

        parent = self.get_object(parent_hash)

        new_obj = model(name=name,
                        parent=parent,
                        collection=self.collection)
        try:
            new_obj.validate_unique()
        except ValidationError, e:
            logger.exception(e)
            raise Exception("\n".join(e.messages))

        new_obj.save()
        return new_obj.get_info()

    def read_file_view(self, request, hash):
        file = self.get_object(hash)
        return render_to_response('read_file.html',
                                  {'file': file},
                                  RequestContext(request))

    def mkdir(self, name, parent):
        """ Creates a new directory. """
        return self._create_object(name, parent, self.directory_model)

    def mkfile(self, name, parent):
        """ Creates a new file. """
        return self._create_object(name, parent, self.file_model)

    def rename(self, name, target):
        """ Renames a file or directory. """
        object = self.get_object(target)
        object.name = name
        object.save()
        return {'added': [object.get_info()],
                'removed': [target]}

    def list(self, target):
        """ Returns a list of files/directories in the target directory. """
        list = []
        for object in self.get_tree(target):
            list.append(object['name'])
        return list

    def paste(self, targets, source, dest, cut):
        """ Moves/copies target files/directories from source to dest. """
        source_dir = self.get_object(source)
        dest_dir = self.get_object(dest)
        added = []
        removed = []
        for target in targets:
            object = self.get_object(target)
            object.parent = dest_dir
            if not cut:
                # This is a copy so the original object should not be changed.
                # Setting the id to None causes Django to insert a new model
                # instead of updating the existing one.
                object.id = None

            # If an object with the same name already exists in the target
            # directory, it should be deleted. This needs to be done for
            # both Files and Directories. Using filter() and iterating
            # over the results is a bit cleaner than using get() and checking
            # if an object was returned, even though most of the time both
            # querysets will be empty.
            dirs = self.directory_model.objects.filter(name=object.name,
                                                   parent=object.parent)
            files = self.file_model.objects.filter(name=object.name,
                                                  parent=object.parent)
            for dir in dirs:
                removed.append(dir.get_hash())
                dir.delete()
            for file in files:
                removed.append(file.get_hash())
                file.delete()

            object.save()
            added.append(object.get_info())
            if cut:
                removed.append(object.get_info()['hash'])

        return {'added': added,
                'removed': removed}

    def remove(self, target):
        """ Delete a File or Directory object. """
        object = self.get_object(target)
        object.delete()
        return target

    def upload(self, files, parent):
        """ For now, this uses a very naive way of storing files - the entire
            file is read in to the File model's content field in one go.

            This should be updated to use read_chunks to add the file one 
            chunk at a time.
        """
        added = []
        parent = self.get_object(parent)
        for upload in files.getlist('upload[]'):
            new_file = self.file_model(name=upload.name,
                                       parent=parent,
                                       collection=self.collection,
                                       content=upload.read())
            try:
                new_file.validate_unique()
            except ValidationError, e:
                logger.exception(e)
                raise Exception("\n".join(e.messages))

            new_file.save()
            added.append(new_file.get_info())
        return {'added': added}
