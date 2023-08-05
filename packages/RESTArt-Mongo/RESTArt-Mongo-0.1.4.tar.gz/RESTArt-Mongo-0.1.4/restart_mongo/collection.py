from __future__ import absolute_import

import copy

import bson
from jsonpatch import JsonPatch
from restart import status
from restart.resource import Resource
from restart.exceptions import NotFound
from restart.utils import make_location_header

from .form import Form
from .filter import Filter
from .paginator import Paginator
from .sorter import Sorter
from .selector import Selector
from .middlewares import SerializerMiddleware
from .utils import get_exception_detail


class Collection(Resource):
    """The resource class that represents a MongoDB collection.

    Note:
       You must subclass this class, and specify the
       class-level attributes `database` and `collection_name`.
    """

    #: The database instance
    database = None

    #: The collection name
    collection_name = None

    #: The validation form class
    form_class = Form

    #: The filter class
    filter_class = Filter

    #: The paginator object
    paginator = Paginator()

    #: The sorter object
    sorter = Sorter()

    #: The selector object
    selector = Selector()

    middleware_classes = (SerializerMiddleware,)

    def __init__(self, *args, **kwargs):
        if self.database is None:
            raise AttributeError('The class-level attribute `database` '
                                 'must be specified.')
        if self.collection_name is None:
            raise AttributeError('The class-level attribute `collection_name` '
                                 'must be specified.')

        self.engine = self.database[self.collection_name]
        self.filter = self.filter_class(self.database, self.collection_name)

        super(Collection, self).__init__(*args, **kwargs)

    def get_pk(self, pk):
        try:
            return bson.ObjectId(pk)
        except bson.errors.InvalidId:
            raise NotFound()

    def get_doc(self, pk, fields=None):
        doc = self.engine.find_one(
            {'_id': self.get_pk(pk)},
            fields=fields
        )
        if doc:
            return doc
        else:
            raise NotFound()

    def get_params(self, request):
        query_params = copy.deepcopy(request.args)
        page, per_page = self.paginator.get_args(query_params)
        sort = self.sorter.get_args(query_params)
        fields = self.selector.get_fields(query_params)
        lookup = self.filter.query(query_params)
        return page, per_page, sort, fields, lookup

    def index(self, request):
        page, per_page, sort, fields, lookup = self.get_params(request)

        skip, limit = (page - 1) * per_page, per_page
        docs = self.engine.find(
            spec=lookup, skip=skip, limit=limit,
            sort=sort, fields=fields
        )
        count = self.engine.find(spec=lookup).count()
        headers = self.paginator.make_headers(
            request.uri.split('?', 1)[0],
            page, per_page, count
        )
        return list(docs), status.HTTP_200_OK, headers

    def create(self, request):
        form = self.form_class(request.data)
        if form.is_valid():
            _id = self.engine.insert(form.document)
            headers = {'Location': make_location_header(request, _id)}
            return {'_id': _id}, status.HTTP_201_CREATED, headers
        return form.errors, status.HTTP_400_BAD_REQUEST

    def read(self, request, pk):
        _, _, _, fields, _ = self.get_params(request)
        return self.get_doc(pk, fields)

    def replace(self, request, pk):
        form = self.form_class(request.data)
        if form.is_valid():
            doc = form.document
            doc.update({'_id': self.get_pk(pk)})
            self.engine.remove({'_id': doc['_id']})
            self.engine.insert(doc)
            return '', status.HTTP_204_NO_CONTENT
        return form.errors, status.HTTP_400_BAD_REQUEST

    def update(self, request, pk):
        doc = self.get_doc(pk)

        # Do JSON-Patch
        patch_data = JsonPatch(request.data)
        try:
            patch_data.apply(doc, in_place=True)
        except Exception as e:
            return ({'jsonpatch_error': get_exception_detail(e)},
                    status.HTTP_400_BAD_REQUEST)

        # Validate data after JSON-Patch
        form = self.form_class(doc)
        if form.is_valid():
            self.engine.save(form.document)
            return '', status.HTTP_204_NO_CONTENT
        return form.errors, status.HTTP_400_BAD_REQUEST

    def delete(self, request, pk):
        doc = self.get_doc(pk)
        self.engine.remove({'_id': doc['_id']})
        return '', status.HTTP_204_NO_CONTENT
