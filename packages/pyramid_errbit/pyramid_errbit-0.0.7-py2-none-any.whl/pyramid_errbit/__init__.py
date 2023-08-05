# auto-generated version file from releasing
try:
    from ._version import __major__, __minor__, __revision__, __hash__
except ImportError:
    __major__ = 0
    __minor__ = 0
    __revision__ = 0
    __hash__ = ''

__version_info__ = (__major__, __minor__, __revision__)
__version__ = '{0}.{1}.{2}'.format(*__version_info__)

# define global reporting information
import errbit_reporter as errbit
import socket
from pyramid import events

errbit_config = None
errbit_client = None
IGNORE_400_ERRORS = True
IGNORE_ERRORS = set()

def get_request_info(request):
    """
    Extracts information about the request to notify errbit about.

    :param request: <pyramid.request.Request>

    :return: {
        'request_url': <str> || None,
        'component': <str> || None,
        'action': <str> || None,
        'params': <dict> || None,
        'session': <dict> || None,
        'cgi_data': <dict> || None,
        'timeout': <int> || None
    }
    """
    if not request:
        return {}

    try:
        params = dict(request.json_body)
    except StandardError:
        params = dict(request.params)

    try:
        session = dict(request.session)
    except StandardError:
        session = {}

    return {
        'exc_info': request.exc_info,
        'request_url': request.path_url,
        'component': request.matched_route.name if request.matched_route else '',
        'action': request.method,
        'params': params,
        'cgi_data': dict(request.environ),
        'session': session
    }

def is_error_ignored(exc_type):
    """
    Filters errors to determine whether or not to notify about them.  By
    default, 400 level errors are

    :param exc_type: subclass of <Exception>

    :return: <bool>
    """
    if IGNORE_400_ERRORS and (getattr(exc_type, 'code', 500) / 100) == 4:
        return True
    elif exc_type in IGNORE_ERRORS:
        return True
    else:
        return False

def check_for_errors(request, response):
    """
    Notifies errbit when any system exception occurs.

    :param request: <pyramid.request.Request>

    :return: <errbit_reporter.NoticeMetadata>
    """
    exc = request.exception

    if not (exc is None or is_error_ignored(exc)):
        # extract request information to notify about
        info = get_request_info(request)

        # generate the notice information
        return errbit_client.notify(**info)

def setup_error_check(event):
    event.request.add_response_callback(check_for_errors)

def includeme(config):
    global errbit_client, errbit_config, IGNORE_400_ERRORS

    settings = config.registry.settings

    # create the new errbit reporter
    errbit_config = errbit.Configuration(
        api_key=settings.get('errbit.api_key'),
        errbit_url=settings.get('errbit.url'),
        project_root=settings.get('errbit.project_root'),
        environment_name=settings.get('errbit.environment_name', 'production'),
        server_name=settings.get('errbit.server_name', socket.gethostname())
    )

    IGNORE_400_ERRORS = settings.get('errbit.ignore_400_errors') != 'False'

    # generate the errbit client
    errbit_client = errbit.Client(errbit_config)

    # register the new request callback
    config.add_subscriber(setup_error_check, events.NewRequest)