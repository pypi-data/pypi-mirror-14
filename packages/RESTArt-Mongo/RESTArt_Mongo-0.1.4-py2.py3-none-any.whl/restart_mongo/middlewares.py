from __future__ import absolute_import

from jsonsir import Serializer
from jsonsir.contrib.intencoder import IntEncoder
from jsonsir.contrib.boolencoder import BoolEncoder
from jsonsir.contrib.regexencoder import RegexEncoder
from jsonsir.contrib.objectidencoder import ObjectIdEncoder
from jsonsir.contrib.datetimeencoder import DateTimeEncoder


# Make an instance of `Serializer` (bound with specified encoders)
serializer = Serializer([
    IntEncoder(),
    BoolEncoder(),
    RegexEncoder(),
    ObjectIdEncoder(),
    # Using UTC Format, see http://www.w3.org/TR/NOTE-datetime for details
    DateTimeEncoder('%Y-%m-%dT%H:%M:%SZ'),
])


class SerializerMiddleware(object):
    """The middleware used for serializing/deserializing the
    request/response payload.
    """

    #: The serializer object
    serializer = serializer

    #: The serializing scheme
    #:     True -- serialize data and bind it with type names
    #:     False -- only serialize data
    with_type_name = False

    def process_request(self, request):
        """Deserialize the request data and query parameters.

        :param request: the request object.
        """
        request._data = self.serializer.deserialize(request.data)
        request._args = self.serializer.deserialize(request.args)

    def process_response(self, request, response):
        """Serialize the response data.

        :param request: the request object.
        :param response: the response object.
        """
        response.data = self.serializer.serialize(response.data,
                                                  self.with_type_name)
        return response
