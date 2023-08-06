import logging
import six

if six.PY2:
    from urllib import quote
else:
    from urllib.parse import quote

from contextio.lib.v2_0 import helpers
from contextio.lib.v2_0.errors import MissingResourceId

no_resource_id_required = ["BaseResource", "Discovery"]

class BaseResource(object):
    """Base class for resource objects."""
    keys = []

    def __init__(self, parent, base_uri, definition):
        class_name = self.__class__.__name__
        if class_name not in no_resource_id_required and self.resource_id not in definition:
            raise MissingResourceId(
                "Resource {0} requires attribute '{1}' for initialization".format(
                    self.__class__.__name__, self.resource_id))

        if definition == "":
            logging.error('Empty response received for ' + base_uri + "")
            return

        try:
            definition = helpers.uncamelize(definition)
        except:
            logging.error('Invalid response received for ' + base_uri + "")
            return

        for k in self.__class__.keys:
            if k in definition:
                setattr(self, k, definition[k])
            else:
                setattr(self, k, None)

        self.parent = parent
        unidict = {six.text_type(k): six.text_type(v) for k, v in definition.items()}
        self.base_uri = quote(base_uri.format(**unidict))

    def _uri_for(self, *elems):
        """Joins API endpoint elements and returns a string."""
        return '/'.join([self.base_uri] + list(elems))

    def _request_uri(self, uri_endpoint="", method="GET", params={}, headers={}, body=''):
        """Gathers up request elements and helps form the request object.

        Required Arguments:
            uri_endpoint: string - the endpoint.

        Optional Arguments:
            method: string - the method of the request. Possible values are
                'GET', 'POST', 'DELETE', 'PUT'
            params: dict - parameters to pass along
            headers: dict - any specific http headers
            body: string - request body, only used on a few PUT statements
        """
        uri = self._uri_for(uri_endpoint)
        return self.parent._request_uri(
            uri, method=method, params=params, headers=headers, body=body)

    def get(self, uri="", return_bool=True, params={}, all_args=[], required_args=[]):
        response = self._request_uri(uri, params=helpers.sanitize_params(params, all_args, required_args))
        self.__init__(self.parent, response)

        if return_bool:
            return True

        return response

    def delete(self, uri=""):
        response = self._request_uri(uri, method='DELETE')
        return bool(response['success'])

    def post(self, uri="", return_bool=True, params={}, headers={}, all_args=[], required_args=[]):
        params = helpers.sanitize_params(params, all_args, required_args)
        response = self._request_uri(uri, method="POST", params=params, headers=headers)

        if return_bool:
            return bool(response['success'])

        return response

    def put(self):
        logging.info("This method is not implemented")
