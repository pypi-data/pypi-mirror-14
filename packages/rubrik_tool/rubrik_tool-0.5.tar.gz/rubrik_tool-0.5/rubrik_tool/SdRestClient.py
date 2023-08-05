import copy
import logging
import json
import requests
import time

from requests.auth import HTTPBasicAuth

log = logging.getLogger(__name__)


class SdRestClient(object):
    __before_request = None

    __after_request = None

    MAX_REQUEST_ATTEMPTS = 4

    @classmethod
    def set_request_callbacks(cls, before_request, after_request):
        cls.__before_request = staticmethod(before_request)
        cls.__after_request = staticmethod(after_request)

    def __init__(self, base_url, authenticate=None):
        """Create a client instance for talking with the ScaleData REST API.

        The base URL should not end with a trailing '/'.
        Example: 'https://localhost:443'

        In the future this interface should include authentication
        information.
        """

        self.base_url = base_url
        self.authenticate = authenticate
        self.auth_token = None

    def get_base_url(self):
        return self.base_url

    def stream(self, relative_url):
        local_filename = "/tmp/" + relative_url.split('/')[-1]
        r = self.__request('get', relative_url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=100000):
                if chunk:
                    f.write(chunk)
        return local_filename

    def send_one_request(self, method, relative_uri, **kwargs):
        """Make a generic HTTP request and return the decoded JSON response.
           If the response is not a JSON, then the response object is returned
        The relative URI should start with a '/'.
        Example: '/vm'

        The data keyword argument, if provided, will be JSON encoded before
        sending the request.
        """
        response = self.__request(method, relative_uri, **kwargs)

        # try re-authenticating for authentication failures
        if response.status_code == 401 and self.authenticate is not None:
            log.debug('Authentication failed for: %s, trying to authenticate'
                      % repr(relative_uri))
            self.auth_token = self.authenticate()
            log.debug('Auth token is %s for base_url %s' %
                      (repr(self.auth_token), repr(self.base_url)))
            response = self.__request(method, relative_uri, **kwargs)
            if response.status_code == 200:
                log.debug("Authentication successful for %s" %
                          repr(relative_uri))

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Log the response content since it's often helpful to diagnose
            # the issue.
            log.debug(
                'HTTP error response content (%s):\n%s' %
                (repr(e.response.status_code), repr(e.response.content)))
            raise
        try:
            return response.json()
        except ValueError as e:
            return response

    # Post requests are potentially non-idempotent so we refrain from retrying
    # them unless we are certain that the previous attempt did not make it to
    # the server.  When in doubt we err on the safe side.
    def is_request_retriable(self, method, e):
        if method != 'post':
            return True
        if isinstance(e, requests.exceptions.ConnectionError) or \
           isinstance(e, requests.exceptions.TooManyRedirects):
            return True
        log.debug('Not retrying further as request may not be idempotent')
        return False

    def request(self, method, relative_uri, **kwargs):
        """Make an HTTP request with retries. Return the decoded JSON response.

        The semantics mirror those of self.send_one_request with the exception
        of performing up to self.MAX_REQUEST_ATTEMPTS request attempts until
        successful.

        Note that multiple attempts could be dangerous for non-idempotent
        requests, so we retry just in cases in which retrying is safe.
        """
        max_attempts = max(1, self.MAX_REQUEST_ATTEMPTS)
        for attempt in range(1, max_attempts + 1):
            try:
                response = self.send_one_request(method,
                                                 relative_uri,
                                                 **kwargs)
                break
            except Exception as e:
                log.debug(
                    'Request attempt %d/%d failed' % (attempt, max_attempts))
                if not self.is_request_retriable(method, e) or \
                   attempt == max_attempts:
                    raise

            time.sleep(10)

        return response

    def delete(self, relative_uri, **kwargs):
        """Make an HTTP DELETE request and return the decoded JSON response.
        """

        return self.request('delete', relative_uri, **kwargs)

    def get(self, relative_uri, **kwargs):
        """Make an HTTP GET request and return the decoded JSON response.
        """

        return self.request('get', relative_uri, **kwargs)

    def patch(self, relative_uri, **kwargs):
        """Make an HTTP PATCH request and return the decoded JSON response.
        """

        return self.request('patch', relative_uri, **kwargs)

    def post(self, relative_uri, **kwargs):
        """Make an HTTP POST request and return the decoded JSON response.
        """

        return self.request('post', relative_uri, **kwargs)

    def put(self, relative_uri, **kwargs):
        """Make an HTTP PUT request and return the decoded JSON response.
        """

        return self.request('put', relative_uri, **kwargs)

    def __request(self, method, relative_uri, **kwargs):
        full_url = self.base_url + relative_uri
        log.debug('Making a %s call to url: %s [%s]' %
                  (method, full_url, kwargs))

        new_kwargs = copy.copy(kwargs)
        new_kwargs['verify'] = False

        if ('data' in kwargs.keys()):
            data = json.dumps(kwargs['data'], indent=2, sort_keys=True)
            new_kwargs['data'] = data

        if (self.auth_token is not None) and ('auth' not in kwargs.keys()):
            new_kwargs['auth'] = HTTPBasicAuth(self.auth_token, '')

        if (SdRestClient.__before_request is not None):
            SdRestClient.__before_request(method, relative_uri)

        # Run with disabled InsecureRequestWarning coming from urllib3. We
        # knowingly disable certificate verification because our product
        # initially comes with self-signed certificates.
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            response = requests.request(method, full_url, **new_kwargs)

        if (SdRestClient.__after_request is not None):
            SdRestClient.__after_request(method, relative_uri)

        return response
