from django.core.exceptions import ObjectDoesNotExist
from elfinder.models import FileCollection, Directory, File
import logging
import traceback
import sys


""" Connector class for Django/elFinder integration.

    TODO

    Permissions checks when viewing/modifying objects - users can currently
    create files in other people's file collections, or delete files they
    do not own. This needs to be implemented in an extendable way, rather
    than being tied to one method of permissions checking.
"""


logger = logging.getLogger(__name__)


class ElFinderConnector():
    _version = '2.0'

    def __init__(self, volumes={}):
        self.httpResponse = {}
        self.httpStatusCode = 200
        self.httpHeader = {'Content-type': 'application/json'}
        self.data = {}
        self.response = {}
        self.return_view = None

        # Populate the volumes dict, using volume_id as the key
        self.volumes = {}
        for volume in volumes:
            self.volumes[volume.get_volume_id()] = volume

    def get_commands(self):
        """ Returns a dict which maps command names to functions.

            The dict key is the command name. The value is a tuple containing
            the name of a function on this class, and a dict specifying which
            GET variables must be set/unset. This lets us do validation of the
            given arguments, so the command functions can assume the correct
            values are set. Used by check_command_functions.
        """
        return {'open': ('__open', {'target': True}),
                'tree': ('__tree', {'target': True}),
                'file': ('__file', {'target': True}),
                'parents': ('__parents', {'target': True}),
                'mkdir': ('__mkdir', {'target': True, 'name': True}),
                'mkfile': ('__mkfile', {'target': True, 'name': True}),
                'rename': ('__rename', {'target': True, 'name': True}),
                'ls': ('__list', {'target': True}),
                'paste': ('__paste', {'targets[]': True, 'src': True,
                                      'dst': True, 'cut': True}),
                'rename': ('__rename', {'target': True, 'name': True}),
                'rm': ('__remove', {'targets[]': True}),
                'upload': ('__upload', {'target': True}),
               }

    def get_init_params(self):
        """ Returns a dict which is used in response to a client init request.

            The returned dict will be merged with response during the __open
            command.
        """
        return {'api': '2.0',
                'uplMaxSize': '128M',
                'options': {'separator': '/',
                            'disabled': [],
                            'archivers': {'create': [],
                                          'extract': []},
                            'copyOverwrite': 1}
               }

    def get_allowed_http_params(self):
        """ Returns a list of parameters allowed during GET/POST requests.
        """
        return ['cmd', 'target', 'targets[]', 'current', 'tree',
                'name', 'content', 'src', 'dst', 'cut', 'init',
                'type', 'width', 'height', 'upload[]']

    def get_volume(self, hash):
        """ Returns the volume which contains the file/dir represented by the
            hash.
        """
        try:
            volume_id, target = hash.split('_')
        except ValueError:
            raise Exception('Invalid target hash: %s' % hash)

        return self.volumes[volume_id]

    def check_command_variables(self, command_variables):
        """ Checks the GET variables to ensure they are valid for this command.
            _commands controls which commands must or must not be set.

            This means command functions do not need to check for the presence
            of GET vars manually - they can assume that required items exist.
        """
        for field in command_variables:
            if command_variables[field] == True and field not in self.data:
                return False
            elif command_variables[field] == False and field in self.data:
                return False
        return True

    def run_command(self, func_name, command_variables):
        """ Attempts to run the given command.

            If the command does not execute, or there are any problems
            validating the given GET vars, an error message is set.

            func: the name of the function to run (e.g. __open)
            command_variables: a list of 'name':True/False tuples specifying
            which GET variables must be present or empty for this command.
        """
        if not self.check_command_variables(command_variables):
            self.response['error'] = 'Invalid arguments'
            return

        func = getattr(self, '_' + self.__class__.__name__ + func_name, None)
        if not callable(func):
            self.response['error'] = 'Command failed'
            return

        try:
            func()
        except Exception, e:
            self.response['error'] = '%s' % e
            logger.exception(e)

    def run(self, request):
        """ Main entry point for running commands. Attemps to run a command
            function based on info in request.GET.

            The command function will complete in one of two ways. It can
            set response, which will be turned in to an HttpResponse and
            returned to the client.

            Or it can set return_view, a Django View function which will
            be rendered and returned to the client.
        """

        self.request = request

        # Is this a POST or a GET?
        if request.method == 'POST':
            data_source = request.POST
        elif request.method == 'GET':
            data_source = request.GET

        # Copy allowed parameters from the given request's GET to self.data
        for field in self.get_allowed_http_params():
            if field in data_source:
                if field == "targets[]":
                    self.data[field] = data_source.getlist(field)
                else:
                    self.data[field] = data_source[field]

        # If a valid command has been specified, try and run it. Otherwise set
        # the relevant error message.
        commands = self.get_commands()
        if 'cmd' in self.data:
            if self.data['cmd'] in commands:
                cmd = commands[self.data['cmd']]
                self.run_command(cmd[0], cmd[1])
            else:
                self.response['error'] = 'Unknown command'
        else:
            self.response['error'] = 'No command specified'

        self.httpResponse = self.response
        return self.httpStatusCode, self.httpHeader, self.httpResponse

    def __parents(self):
        """ Handles the parent command.

            Sets response['tree'], which contains a list of dicts representing
            the ancestors/siblings of the target object.

            The tree is not a tree in the traditional hierarchial sense, but
            rather a flat list of dicts which have hash and parent_hash (phash)
            values so the client can draw the tree.
        """
        target = self.data['target']
        volume = self.get_volume(target)
        self.response['tree'] = volume.get_tree(target,
                                                ancestors=True,
                                                siblings=True)

    def __tree(self):
        """ Handles the 'tree' command.

            Sets response['tree'] - a list of children of the specified
            target Directory.
        """
        target = self.data['target']
        volume = self.get_volume(target)
        self.response['tree'] = volume.get_tree(target)

    def __file(self):
        """ Handles the 'file' command.

            Sets return_view, which will cause read_file_view to be rendered
            as the response. A custom read_file_view can be given when
            initialising the connector.
        """
        target = self.data['target']
        volume = self.get_volume(target)

        # A file was requested, so set return_view to the read_file view.
        #self.return_view = self.read_file_view(self.request, volume, target)
        self.return_view = volume.read_file_view(self.request, target)

    def __open(self):
        """ Handles the 'open' command.

            Sets response['files'] and response['cwd'].

            If 'tree' is requested, 'files' contains information about all
            ancestors, siblings and children of the target. Otherwise, 'files'
            only contains info about the target's immediate children.

            'cwd' contains info about the currently selected directory.

            If 'target' is blank, information about the root dirs of all
            currently-opened volumes is returned. The root of the first
            volume is considered to be the current directory.
        """
        if 'tree' in self.data and self.data['tree'] == '1':
            inc_ancestors = True
            inc_siblings = True
        else:
            inc_ancestors = False
            inc_siblings = False

        target = self.data['target']
        if target == '':
            # No target was specified, which means the client is being opened
            # for the first time and requires information about all currently
            # opened volumes.

            # Assume the first volume's root is the currently open directory.
            volume = self.volumes.itervalues().next()
            self.response['cwd'] = volume.get_info('')

            # Add relevant tree information for each volume
            for volume_id in self.volumes:
                volume = self.volumes[volume_id]
                self.response['files'] = volume.get_tree('',
                                                         inc_ancestors,
                                                         inc_siblings)
        else:
            # A target was specified, so we only need to return info about
            # that directory.
            volume = self.get_volume(target)
            self.response['cwd'] = volume.get_info(target)
            self.response['files'] = volume.get_tree(target,
                                                     inc_ancestors,
                                                     inc_siblings)

        # If the request includes 'init', add some client initialisation
        # data to the response.
        if 'init' in self.data:
            self.response.update(self.get_init_params())

    def __mkdir(self):
        target = self.data['target']
        volume = self.get_volume(target)
        self.response['added'] = [volume.mkdir(self.data['name'], target)]

    def __mkfile(self):
        target = self.data['target']
        volume = self.get_volume(target)
        self.response['added'] = [volume.mkfile(self.data['name'], target)]

    def __rename(self):
        target = self.data['target']
        volume = self.get_volume(target)
        self.response.update(volume.rename(self.data['name'], target))

    def __list(self):
        target = self.data['target']
        volume = self.get_volume(target)
        self.response['list'] = volume.list(target)

    def __paste(self):
        targets = self.data['targets[]']
        source = self.data['src']
        dest = self.data['dst']
        cut = (self.data['cut'] == '1')
        source_volume = self.get_volume(source)
        dest_volume = self.get_volume(dest)
        if source_volume != dest_volume:
            raise Exception('Moving between volumes is not supported.')
        self.response.update(dest_volume.paste(targets, source, dest, cut))

    def __remove(self):
        targets = self.data['targets[]']
        self.response['removed'] = []
        # Because the targets might not all belong to the same volume, we need
        # to lookup the volume and call the remove() function for every target.
        for target in targets:
            volume = self.get_volume(target)
            self.response['removed'].append(volume.remove(target))

    def __upload(self):
        parent = self.data['target']
        volume = self.get_volume(parent)
        self.response.update(volume.upload(self.request.FILES, parent))
