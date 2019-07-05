from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.template import RequestContext
from elfinder.connector import ElFinderConnector
from elfinder.models import FileCollection
from elfinder.volume_drivers.model_driver import ModelVolumeDriver


def index(request, coll_id):
    """ Displays the elFinder file browser template for the specified
        FileCollection.
    """
    collection = FileCollection.objects.get(pk=coll_id)
    return render_to_response("elfinder.html",
                              {'coll_id': collection.id},
                              RequestContext(request))


def connector_view(request, coll_id):
    """ Handles requests for the elFinder connector.
    """

    model_volume = ModelVolumeDriver(coll_id)

    finder = ElFinderConnector([model_volume])
    finder.run(request)

    # Some commands (e.g. read file) will return a Django View - if it
    # is set, return it directly instead of building a response
    if finder.return_view:
        return finder.return_view

    response = HttpResponse(mimetype=finder.httpHeader['Content-type'])
    response.status_code = finder.httpStatusCode
    if finder.httpHeader['Content-type'] == 'application/json':
        response.content = json.dumps(finder.httpResponse)
    else:
        response.content = finder.httpResponse

    return response


def read_file(request, volume, file_hash, template="read_file.html"):
    """ Default view for responding to "open file" requests.

        coll: FileCollection this File belongs to
        file: The requested File object
    """
    return render_to_response(template,
                              {'file': file_hash},
                              RequestContext(request))
