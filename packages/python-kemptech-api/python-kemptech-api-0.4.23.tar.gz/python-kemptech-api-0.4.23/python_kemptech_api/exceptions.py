from .api_xml import get_error_msg

# 400+ shouldn't be handled here, but cover it anyway.
# This is just optional fallback for
# laziness when no message is given.
STATUS_CODES = {
    400: 'Mandatory parameter missing from request',
    401: 'Client Error: Authorization required',
    403: 'Incorrect permissions',
    404: 'Not found. Ensure the API is enabled on the LoadMaster',
    405: 'Unknown command',
    422: 'Invalid operation'
}


def get_api_exception_message(msg, code, is_xml_msg):
    if msg is not None:
        # 400 Errors should be handled here. This will pass the error
        # message given by the LoadMaster API and show it as the exception
        # message in the traceback.
        message = get_error_msg(msg) if is_xml_msg else msg
    else:
        try:
            message = '{} {}.'.format(code, STATUS_CODES[code])
        except KeyError:
            message = "An unknown error has occurred ({}).".format(code)

    return message


class KempTechApiException(Exception):
    """Raised if HTTP request has failed."""

    def __init__(self, msg=None, code=None, is_xml_msg=True):
        message = get_api_exception_message(msg, code, is_xml_msg)
        super(KempTechApiException, self).__init__(message)


class KempConnectionError(KempTechApiException):
    def __init__(self, endpoint):
        msg = "A connection error occurred to {endpoint}."\
            .format(endpoint=endpoint)
        super(KempConnectionError, self).__init__(msg)


class UrlRequiredError(KempTechApiException):
    def __init__(self, cmd_url):
        msg = "{} is an invalid URL".format(cmd_url)
        super(UrlRequiredError, self).__init__(msg)


class TooManyRedirectsException(KempTechApiException):
    def __init__(self, cmd_url):
        msg = "Too many redirects with request to {}.".format(cmd_url)
        super(TooManyRedirectsException, self).__init__(msg)


class TimeoutException(KempTechApiException):
    def __init__(self, endpoint):
        msg = "A connection {} has timed out.".format(endpoint)
        super(TimeoutException, self).__init__(msg)


class HTTPError(KempTechApiException):
    def __init__(self, cmd_url):
        msg = "A HTTP error occurred with request to {}.".format(cmd_url)
        super(HTTPError, self).__init__(msg)


class ApiNotEnabledError(KempTechApiException):
    def __init__(self):
        msg = "Ensure the API is enabled on the LoadMaster."
        super(ApiNotEnabledError, self).__init__(msg)


class CommandNotAvailableException(KempTechApiException):
    def __init__(self, lm, cmd_name):
        msg = "Command '{}' is not available on LoadMaster {}.".format(
            cmd_name, lm)
        super(CommandNotAvailableException, self).__init__(msg,
                                                           is_xml_msg=False)


class ConnectionTimeoutException(KempTechApiException):
    def __init__(self, lm):
        msg = "Connection timed out to '{}'.".format(lm)
        super(ConnectionTimeoutException, self).__init__(
            msg, is_xml_msg=False)


def get_parameter_message(obj, parameters):
    try:
        param = parameters['param']
        value = parameters['value']
        msg = '{} failed to set {}: {}'.format(obj, param, value)
    except (KeyError, TypeError) as e:
        msg = '{} failed to set {} ({})'.format(
            obj, parameters, str(e))

    return msg


class ValidationError(Exception):
    pass


class LoadMasterParameterError(Exception):
    def __init__(self, lm, parameters):
        msg = get_parameter_message(lm, parameters)
        super(LoadMasterParameterError, self).__init__(msg)


class VirtualServiceParameterError(Exception):
    def __init__(self, vs, parameters):
        msg = get_parameter_message(vs, parameters)
        super(VirtualServiceParameterError, self).__init__(msg)


class RealServerParameterError(Exception):
    def __init__(self, rs, parameters):
        msg = get_parameter_message(rs, parameters)
        super(RealServerParameterError, self).__init__(msg)


class MissingInfo(Exception):
    service = 'My service'
    param_name = 'parameter_name'

    def __init__(self, param):
        msg = ("{} is missing the {} parameter "
               "'{}'").format(self.service, self.param_name, param)
        super(MissingInfo, self).__init__(msg)


class VirtualServiceMissingLoadmasterInfo(MissingInfo):
    service = 'Virtual service'
    param_name = 'LoadMaster'


class RealServerMissingLoadmasterInfo(MissingInfo):
    service = 'Real server'
    param_name = 'LoadMaster'


class RealServerMissingVirtualServiceInfo(MissingInfo):
    service = 'Real server'
    param_name = 'Virtual service'
