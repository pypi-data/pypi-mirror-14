import orb

from orb import Query as Q
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden
from pyramid_orb.utils import get_context
from .orbservice import OrbService


class ModelService(OrbService):
    """ Represents an individual database record """
    def __init__(self, request, model, parent=None, record_id=None, from_collection=None, record=None, name=None):
        name = name or str(id)
        super(ModelService, self).__init__(request, parent, name=name)

        # define custom properties
        self.model = model
        self.record_id = record_id
        self.__record = record
        self.from_collection = from_collection

    def __getitem__(self, key):
        schema = self.model.schema()

        # lookup the articles information
        col = schema.column(key, raise_=False)
        if col:
            # return a reference for the collection
            if isinstance(col, orb.ReferenceColumn):
                record_id = self.model.select(where=Q(self.model) == self.record_id, limit=1).values(col.name())[0]
                return ModelService(self.request, col.referenceModel(), record_id=record_id)

            # columns are not directly accessible
            else:
                raise KeyError(key)

        # generate collector services
        lookup = schema.collector(key)
        if lookup:
            name = lookup.name()
            record = self.model(self.record_id, context=orb.Context(columns=['id']))
            method = getattr(record, name, None)
            if not method:
                raise KeyError(key)
            else:
                from .collection import CollectionService
                values, context = get_context(self.request, model=self.model)
                if values:
                    where = orb.Query.build(values)
                    context.where = where & context.where

                records = method(context=context)
                return CollectionService(self.request, records, parent=self)

        # lookup regular method
        method = getattr(self.model, key, None)
        if method and self.request.method == 'GET':
            record = self.__record or self.model(self.record_id)
            return_value = method(record)
            if isinstance(return_value, orb.Collection):
                from .collection import CollectionService
                return CollectionService(self.request, return_value, parent=self, name=key)
            elif isinstance(return_value, orb.Model):
                return ModelService(self.request, parent=self, record=return_value)
            else:
                from .builtins import PyObjectService
                return PyObjectService(self.request, return_value, parent=self)
        else:
            return ModelService(self.request, self.model, parent=self, record_id=key)

    def _update(self):
        values, context = get_context(self.request, model=self.model)
        record = self.model(self.record_id, context=context)
        record.update(values)
        record.save()
        return record.__json__()

    def get(self):
        values, context = get_context(self.request, model=self.model)
        if context.returning == 'schema':
            return self.model.schema()
        elif self.record_id:
            return self.model(self.record_id, context=context)
        else:
            if values:
                where = orb.Query.build(values)
                context.where = where & context.where
            return self.model.select(context=context)

    def patch(self):
        if self.record_id:
            return self._update()
        else:
            raise HTTPBadRequest()

    def post(self):
        if self.record_id:
            raise HTTPBadRequest()
        else:
            values, context = get_context(self.request, model=self.model)
            record = self.model.create(values, context=context)
            return record.__json__()

    def put(self):
        if self.record_id:
            return self._update()
        else:
            raise HTTPBadRequest()

    def delete(self):
        if self.record_id:
            values, context = get_context(self.request, model=self.model)
            if self.from_collection:
                return self.from_collection.remove(self.record_id, context=context)
            else:
                return self.record.delete(context=context)
        else:
            raise HTTPBadRequest()

    def permission(self):
        method = self.request.method.lower()
        auth = getattr(self.model, '__auth__')
        if callable(auth):
            return auth(self.request)
        elif isinstance(auth, dict):
            try:
                method_auth = auth[method]
            except KeyError:
                raise HTTPForbidden()
            else:
                if callable(method_auth):
                    return method_auth(self.request)
                else:
                    return method_auth
        elif isinstance(auth, (list, tuple, set)):
            return method in auth
        else:
            return auth
