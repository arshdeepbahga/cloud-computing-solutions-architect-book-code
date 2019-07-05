

class BaseVolumeDriver(object):
    def __init__(self, *args, **kwargs):
        pass

    def get_volume_id(self):
        """ Returns the volume ID for the volume, which is used as a prefix
            for client hashes.
        """
        raise NotImplementedError

    def get_info(self, target):
        """ Returns a dict containing information about the target directory
            or file. This data is used in response to 'open' commands to
            populates the 'cwd' response var.

            :param target: The hash of the directory for which we want info.
            If this is '', return information about the root directory.
            :returns: dict -- A dict describing the directory.
        """
        raise NotImplementedError

    def get_tree(self, target, ancestors=False, siblings=False):
        """ Gets a list of dicts describing children/ancestors/siblings of the
            target.

            :param target: The hash of the directory the tree starts from.
            :param ancestors: Include ancestors of the target.
            :param siblings: Include siblings of the target.
            :param children: Include children of the target.
            :returns: list -- a list of dicts describing directories.
        """
        raise NotImplementedError

    def read_file_view(self, request, hash):
        """ Django view function, used to display files in response to the
            'file' command.

            :param request: The original HTTP request.
            :param hash: The hash of the target file.
            :returns: dict -- a dict describing the new directory.
        """
        raise NotImplementedError

    def mkdir(self, name, parent):
        """ Creates a directory.

            :param name: The name of the new directory.
            :param parent: The hash of the parent directory.
            :returns: dict -- a dict describing the new directory.
        """
        raise NotImplementedError

    def mkfile(self, name, parent):
        """ Creates a directory.

            :param name: The name of the new file.
            :param parent: The hash of the parent directory.
            :returns: dict -- a dict describing the new file.
        """
        raise NotImplementedError

    def rename(self, name, target):
        """ Renames a file or directory.

            :param name: The new name of the file/directory.
            :param target: The hash of the target file/directory.
            :returns: dict -- a dict describing which objects were added and
            removed.
        """
        raise NotImplementedError

    def list(self, target):
        """ Lists the contents of a directory.

            :param target: The hash of the target directory.
            :returns: list -- a list containing the names of files/directories
            in this directory.
        """
        raise NotImplementedError

    def paste(self, targets, source, dest, cut):
        """ Moves/copies target files/directories from source to dest.

            If a file with the same name already exists in the dest directory
            it should be overwritten (the client asks the user to confirm this
            before sending the request).

            :param targets: A list of hashes of files/dirs to move/copy.
            :param source: The current parent of the targets.
            :param dest: The new parent of the targets.
            :param cut: Boolean. If true, move the targets. If false, copy the
            targets.
            :returns: dict -- a dict describing which targets were moved/copied.
        """
        raise NotImplementedError

    def remove(self, target):
        """ Deletes the target files/directories.

            The 'rm' command takes a list of targets - this function is called
            for each target, so should only delete one file/directory.

            :param targets: A list of hashes of files/dirs to delete.
            :returns: string -- the hash of the file/dir that was deleted.
        """
        raise NotImplementedError

    def upload(self, files, parent):
        """ Uploads one or more files in to the parent directory.

            :param files: A list of uploaded file objects, as described here:
            https://docs.djangoproject.com/en/dev/topics/http/file-uploads/
            :param parent: The hash of the directory in which to create the
            new files.
            :returns: TODO
        """
