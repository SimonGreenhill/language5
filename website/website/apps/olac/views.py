#http://www.openarchives.org/OAI/openarchivesprotocol.html
import time
from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.timezone import utc
from django.conf import settings

from reversion.models import Revision

from website.apps.core.models import Language as Model

KNOWN_METADATA_PREFIXES = ('olac', 'oai_dc')

ERRORS = {
    'badArgument': 'The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.',
    'badResumptionToken': 'The value of the resumptionToken argument is invalid or expired.',
    'badVerb': 'Value of the verb argument is not a legal OAI-PMH verb, the verb argument is missing, or the verb argument is repeated.',
    'cannotDisseminateFormat': 'The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository.',
    'idDoesNotExist': 'The value of the identifier argument is unknown or illegal in this repository.',
    'noRecordsMatch': 'The combination of the values of the from, until, set and metadataPrefix arguments results in an empty list.',
    'noMetadataFormats': 'There are no metadata formats available for the specified item.',
    'noSetHierarchy': 'The repository does not support sets.'
}

def check_ident(ident):
    return settings.OLAC_SETTINGS['_identifier'].match(ident)

def parse_time(timestamp):
    if hasattr(datetime, "strptime"):
        d = datetime.strptime('%s UTC' % timestamp, "%Y-%m-%d %Z")
    else:
        # damn you python 2.4 on Centos!
        d = datetime.fromtimestamp(time.mktime(time.strptime(timestamp, "%Y-%m-%d")))
    d = d.replace(tzinfo=utc)
    return d


def get_last_update():
    try:
        return Revision.objects.order_by('-id').only('date_created')[0].date_created
    except IndexError: # no Revision's (i.e. when running tests), return current time
        return datetime.utcnow().replace(tzinfo=utc)


def oai(request):
    try:
        verb = request.REQUEST['verb']
    except (KeyError, IndexError):
        return Identify(request) # No verb given!

    if verb == 'Identify':
        return Identify(request)
    elif verb == 'ListIdentifiers':
        return ListIdentifiers(request)
    elif verb == 'ListMetadataFormats':
        return ListMetadataFormats(request)
    elif verb == 'ListSets':
        return ListSets(request)
    elif verb == 'ListRecords':
        return ListRecords(request)
    elif verb == 'GetRecord':
        return GetRecord(request)
    else:
        return Error(request, ['badVerb'])

def Error(request, error_list, extra_kwargs={}):
    "ERROR handler"
    out = {
        'errors': [(e, ERRORS[e]) for e in error_list],
        'url': request.build_absolute_uri()
    }
    out.update(extra_kwargs)
    return render_to_response('olac/Error.xml', out,
        context_instance=RequestContext(request),
        mimetype="application/xhtml+xml")


def Identify(request):
    """
    This verb takes no arguments and returns information about a repository

    The response must include one instance of the following elements:

    Arguments::
    `repositoryName`:   a human readable name for the repository;
    `baseURL`:          the base URL of the repository;
    `protocolVersion`:  the version of the OAI-PMH supported by the repository;
    `earliestDatestamp`: a UTCdatetime that is the guaranteed lower limit
        of all datestamps recording changes, modifications, or deletions in the
        repository. A repository must not use datestamps lower than the one
        specified by the content of the earliestDatestamp element.
        earliestDatestamp must be expressed at the finest granularity
        supported by the repository.
    `deletedRecord`:    the manner in which the repository supports the notion
        of deleted records. Legitimate values are no ; transient ;
        persistent with meanings defined in the section on deletion.
    `granularity`:      the finest harvesting granularity supported by the
        repository. The legitimate values are YYYY-MM-DD and
            YYYY-MM-DDThh:mm:ssZ with meanings as defined in ISO8601.

    The response must include one or more instances of the following element:

    `adminEmail` : the e-mail address of an administrator of the repository.

    The response may include multiple instances of the following optional elements:

    `compression` :     a compression encoding supported by the repository.
        The recommended values are those defined for the Content-Encoding header
        in Section 14.11 of RFC 2616 describing HTTP 1.1. A compression element
        should not be included for the identity encoding, which is implied.
    `description` : an extensible mechanism for communities to describe their
        repositories. For example, the description container could be used to
        include collection-level metadata in the response to the Identify request.
        Implementation Guidelines are available to give directions with this respect.
        Each description container must be accompanied by the URL of an XML schema
        describing the structure of the description container.
    """
    out = {'url': request.build_absolute_uri()}

    if len(request.REQUEST.keys()) > 1: # should take NO other arguments.
        return Error(request, ['badArgument'], out)

    return render_to_response('olac/Identify.xml', out,
        context_instance=RequestContext(request),
            mimetype="application/xhtml+xml")


def ListIdentifiers(request):
    """
    This verb is an abbreviated form of ListRecords, retrieving only headers
    rather than records. Optional arguments permit selective harvesting of
    headers based on set membership and/or datestamp. Depending on the
    repository's support for deletions, a returned header may have a status
    attribute of "deleted" if a record matching the arguments specified in
    the request has been deleted.

    Arguments::
        `from`:      an optional argument with a UTCdatetime value, which specifies
                        a lower bound for datestamp-based selective harvesting.
        `until`:     an optional argument with a UTCdatetime value, which specifies
                        a upper bound for datestamp-based selective harvesting.
        `metadataPrefix`:   a required argument, which specifies that headers should
                        be returned only if the metadata format matching the supplied
                        metadataPrefix is available or, depending on the repository's
                        support for deletions, has been deleted. The metadata formats
                        supported by a repository and for a particular item can be
                        retrieved using the ListMetadataFormats request.
        `set`:      an optional argument with a setSpec value, which specifies set
                        criteria for selective harvesting.
        `resumptionToken`:   an exclusive argument with a value that is the flow
                    control token returned by a previous ListIdentifiers request
                    that issued an incomplete list.

    Error and Exception Conditions::
        `badArgument` - The request includes illegal arguments or is missing required
            arguments.
        `badResumptionToken` - The value of the resumptionToken argument is invalid or
            expired.
        `cannotDisseminateFormat` - The value of the metadataPrefix argument is not
            supported by the repository.
        `noRecordsMatch` - The combination of the values of the from, until, and set
            arguments results in an empty list.
        `noSetHierarchy` - The repository does not support sets.
    """
    out = {'url': request.build_absolute_uri(), 'last_update': get_last_update()}
    error_list = []

    # metadataPrefix is REQUIRED
    if 'metadataPrefix' not in request.REQUEST:
        error_list.append('badArgument')
    elif request.REQUEST['metadataPrefix'] not in KNOWN_METADATA_PREFIXES:
        out['metadataPrefix'] = request.REQUEST['metadataPrefix']
        error_list.append('cannotDisseminateFormat')
    elif len(request.GET.getlist('metadataPrefix')) > 1:
        # should NOT handle cases when there are two or more metadataPrefix's
        error_list.append('badArgument')
    else:
        out['metadataPrefix'] = request.REQUEST['metadataPrefix']

    if 'set' in request.REQUEST:
        error_list.append('noSetHierarchy')
    if 'resumptionToken' in request.REQUEST:
        error_list.append('badResumptionToken')

    if len(error_list) > 0:
        return Error(request, error_list, out)


    objects = Model.objects.all().exclude(isocode__exact="")

    if 'from' in request.REQUEST:
        out['from'] = request.REQUEST['from']
        try:
            frm = parse_time(request.REQUEST['from'])
        except (TypeError, ValueError):
            return Error(request, ['badArgument'], out)
        objects = objects.filter(added__gte=frm)
            #
            #
            # datetime_published__year=
            # datetime_published__year='2008',
            #                          datetime_published__month='03',
            #                          datetime_published__day='27')

    if 'until' in request.REQUEST:
        out['until'] = request.REQUEST['until']
        try:
            until = parse_time(request.REQUEST['until'])
        except (TypeError, ValueError):
            return Error(request, ['badArgument'], out)

        objects = objects.filter(added__lte=until)

    if len(objects) == 0:
        return Error(request, ['noRecordsMatch'], out)

    out['object_list'] = objects
    return render_to_response('olac/ListIdentifiers.xml', out,
        context_instance=RequestContext(request),
                            mimetype="application/xhtml+xml")


def ListSets(request):
    """
    This verb is used to retrieve the set structure of a repository, useful for
    selective harvesting.

    Arguments::

    `resumptionToken`   - an exclusive argument with a value that is the flow
        control token returned by a previous ListSets request that issued an
        incomplete list.

    Error and Exception Conditions::

    `badArgument`   - The request includes illegal arguments or is missing
        required arguments.
    `badResumptionToken` - The value of the resumptionToken argument is
        invalid or expired.
    `noSetHierarchy` - The repository does not support sets.
    """
    return Error(request, ['noSetHierarchy'])

def ListMetadataFormats(request):
    """
    This verb is used to retrieve the metadata formats available from a repository.
    An optional argument restricts the request to the formats available for a specific item.

    Arguments::
    `identifier`:    an optional argument that specifies the unique identifier
            of the item for which available metadata formats are being requested.
            If this argument is omitted, then the response includes all metadata
            formats supported by this repository. Note that the fact that a
            metadata format is supported by a repository does not mean that it
            can be disseminated from all items in the repository.

    Error and Exception Conditions::
    `badArgument` - The request includes illegal arguments or is missing required arguments.
    `idDoesNotExist` - The value of the identifier argument is unknown or illegal in this repository.
    `noMetadataFormats` - There are no metadata formats available for the specified item.
    """
    out = {'url': request.build_absolute_uri()}
    if 'identifier' in request.REQUEST:
        # Check identifier:
        out['identifier'] = request.REQUEST['identifier']
        ident = check_ident(request.REQUEST['identifier'])
        if ident is None:
            return Error(request, ['idDoesNotExist'], out)

        isocode, language_id = ident.groups()
        try:
            Model.objects.get(pk=language_id)
        except Model.DoesNotExist:
            return Error(request, ['idDoesNotExist'], out)
        return render_to_response('olac/ListMetadataFormats.xml', out,
                    context_instance=RequestContext(request),
                                        mimetype="application/xhtml+xml")

    return render_to_response('olac/ListMetadataFormats.xml', out,
                    context_instance=RequestContext(request),
                                        mimetype="application/xhtml+xml")


def ListRecords(request):
    """
    This verb is used to harvest records from a repository.

    Optional arguments permit selective harvesting of records based on set
    membership and/or datestamp. Depending on the repository's support for
    deletions, a returned header may have a status attribute of "deleted"
    if a record matching the arguments specified in the request has been deleted.
    No metadata will be present for records with deleted status.

    Arguments::

    `from`   - an optional argument with a UTCdatetime value, which specifies a
        lower bound for datestamp-based selective harvesting.
    `until`  - an optional argument with a UTCdatetime value, which specifies a
        upper bound for datestamp-based selective harvesting.
    `set`    - an optional argument with a setSpec value , which specifies set
        criteria for selective harvesting.
    `resumptionToken`
            - an exclusive argument with a value that is the flow control token
            returned by a previous ListRecords request that issued an incomplete
            list.
    `metadataPrefix` - a required argument (unless the exclusive argument
        resumptionToken is used) that specifies the metadataPrefix of the
        format that should be included in the metadata part of the returned
        records. Records should be included only for items from which the
        metadata format matching the metadataPrefix can be disseminated.
        The metadata formats supported by a repository and for a particular
        item can be retrieved using the ListMetadataFormats request.

    Error and Exception Conditions::

    `badArgument` - The request includes illegal arguments or is missing
        required arguments.
    `badResumptionToken` - The value of the resumptionToken argument is
        invalid or expired.
    `cannotDisseminateFormat` - The value of the metadataPrefix argument
        is not supported by the repository.
    `noRecordsMatch` - The combination of the values of the from, until,
        set and metadataPrefix arguments results in an empty list.
    `noSetHierarchy` - The repository does not support sets.
    """
    out = {'url': request.build_absolute_uri(), 'last_update': get_last_update()}
    error_list = []

    # metadataPrefix is REQUIRED
    if 'metadataPrefix' not in request.REQUEST:
        error_list.append('badArgument')
    elif request.REQUEST['metadataPrefix'] not in KNOWN_METADATA_PREFIXES:
        error_list.append('cannotDisseminateFormat')
    elif len(request.GET.getlist('metadataPrefix')) > 1:
        # should NOT handle cases when there are two or more metadataPrefix's
        error_list.append('badArgument')
    else:
        metadataPrefix = request.REQUEST['metadataPrefix']
        out['metadataPrefix'] = metadataPrefix

    # neither set nor resumptionToken are implemented
    if 'set' in request.REQUEST:
        error_list.append('noSetHierarchy')
    if 'resumptionToken' in request.REQUEST:
        error_list.append('badResumptionToken')

    if len(error_list) > 0:
        return Error(request, error_list, out)

    objects = Model.objects.all().exclude(isocode__exact="")

    if 'from' in request.REQUEST:
        out['from'] = request.REQUEST['from']
        try:
            frm = parse_time(request.REQUEST['from'])
        except (TypeError, ValueError):
            return Error(request, ['badArgument'], out)
        objects = objects.filter(added__gte=frm)

    if 'until' in request.REQUEST:
        out['until'] = request.REQUEST['until']
        try:
            until = parse_time(request.REQUEST['until'])
        except (TypeError, ValueError):
            return Error(request, ['badArgument'], out)

        objects = objects.filter(added__lte=until)

    if len(objects) == 0:
        return Error(request, ['noRecordsMatch'], out)

    out['object_list'] = objects
    return render_to_response('olac/ListRecords.xml', out,
        context_instance=RequestContext(request),
                            mimetype="application/xhtml+xml")


def GetRecord(request):
    """
    This verb is used to retrieve an individual metadata record from a repository.

    Required arguments specify the identifier of the item from which the record
    is requested and the format of the metadata that should be included in the
    record. Depending on the level at which a repository tracks deletions,
    a header with a "deleted" value for the status attribute may be returned,
    in case the metadata format specified by the metadataPrefix is no longer
    available from the repository or from the specified item.

    Arguments::

    `identifier` - a required argument that specifies the unique identifier of
        the item in the repository from which the record must be disseminated.
    `metadataPrefix` - a required argument that specifies the metadataPrefix of
        the format that should be included in the metadata part of the returned
        record . A record should only be returned if the format specified by
        the metadataPrefix can be disseminated from the item identified by the
        value of the identifier argument. The metadata formats supported by a
        repository and for a particular record can be retrieved using the
        ListMetadataFormats request.

    Error and Exception Conditions::

    `badArgument` - The request includes illegal arguments or is missing required
        arguments.
    `cannotDisseminateFormat` - The value of the metadataPrefix argument is not
        supported by the item identified by the value of the identifier argument.
    `idDoesNotExist` - The value of the identifier argument is unknown or
        illegal in this repository.
    """
    out = {'url': request.build_absolute_uri(), 'last_update': get_last_update()}
    error_list = []

    # metadataPrefix is REQUIRED
    if 'metadataPrefix' not in request.REQUEST:
        error_list.append('badArgument')
    elif request.REQUEST['metadataPrefix'] not in KNOWN_METADATA_PREFIXES:
        error_list.append('cannotDisseminateFormat')
    else:
        out['metadataPrefix'] = request.REQUEST['metadataPrefix']

    # identifier is REQUIRED
    if 'identifier' not in request.REQUEST:
        error_list.append('badArgument')

    if len(error_list) > 0:
        return Error(request, error_list, out)

    out['identifier'] = request.REQUEST['identifier'],
    # Check identifier:
    ident = check_ident(request.REQUEST['identifier'])
    if ident is None:
        return Error(request, ['idDoesNotExist'], out)

    isocode, language_id = ident.groups()
    try:
        L = Model.objects.get(pk=language_id)
    except Model.DoesNotExist:
        return Error(request, ['idDoesNotExist'], out)

    out['object'] = L
    return render_to_response('olac/GetRecord.xml', out,
        context_instance=RequestContext(request),
                            mimetype="application/xhtml+xml")
