from datetime import datetime
import falcon
import falcon.errors
import json
import sqlalchemy.exc
import sqlalchemy.orm.exc
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.inspection import inspect
import sqlalchemy.sql.sqltypes
import logging
import sys

try:
    import geoalchemy2.shape
    from geoalchemy2.elements import WKBElement
    from geoalchemy2.types import Geometry
    from shapely.geometry import Point
    support_geo = True
except ImportError:
    support_geo = False


class CollectionResource(object):
    """
    Provides CRUD facilities for a resource collection.
    """
    def __init__(self, db_session, logger=None):
        self.db_session = db_session
        if logger is None:
            logger = logging.getLogger('autocrud')
        self.logger = logger

    def deserialize(self, path_data, body_data):
        mapper      = inspect(self.model)
        attributes  = {}

        for key, value in path_data.items():
            key = getattr(self, 'attr_map', {}).get(key, key)
            if getattr(self.model, key, None) is None or not isinstance(inspect(self.model).attrs[key], ColumnProperty):
                self.logger.error("Programming error: {0}.attr_map['{1}'] does not exist or is not a column".format(self.model, key))
                raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')
            attributes[key] = value

        for key, value in body_data.items():
            column = mapper.columns[key]
            if isinstance(column.type, sqlalchemy.sql.sqltypes.DateTime):
                attributes[key] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            elif support_geo and isinstance(column.type, Geometry) and column.type.geometry_type == 'POINT':
                point           = Point(value['x'], value['y'])
                # geoalchemy2.shape.from_shape uses buffer() which causes INSERT to fail
                attributes[key] = WKBElement(point.wkb, srid=4326)
            else:
                attributes[key] = value
        return attributes

    def serialize(self, resource):
        def _serialize_value(value):
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%dT%H:%M:%SZ')
            elif support_geo and isinstance(value, WKBElement):
                value = geoalchemy2.shape.to_shape(value)
                return {'x': value.x, 'y': value.y}
            else:
                return value
        attrs = inspect(self.model).attrs
        return {
            attr: _serialize_value(getattr(resource, attr)) for attr in attrs.keys() if isinstance(attrs[attr], ColumnProperty)
        }

    def on_get(self, req, resp, *args, **kwargs):
        """
        Return a collection of items.
        """
        resources = self.db_session.query(self.model)
        for key, value in kwargs.items():
            key = getattr(self, 'attr_map', {}).get(key, key)
            attr = getattr(self.model, key, None)
            if attr is None or not isinstance(inspect(self.model).attrs[key], ColumnProperty):
                self.logger.error("Programming error: {0}.attr_map['{1}'] does not exist or is not a column".format(self.model, key))
                raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')
            resources = resources.filter(attr == value)
        for filter_key, value in req.params.items():
            filter_parts = filter_key.split('__')
            key = filter_parts[0]
            if len(filter_parts) == 1:
                comparison = '='
            elif len(filter_parts) == 2:
                comparison = filter_parts[1]
            else:
                raise falcon.errors.HTTPBadRequest('Invalid attribute', 'An attribute provided for filtering is invalid')

            attr = getattr(self.model, key, None)
            if attr is None or not isinstance(inspect(self.model).attrs[key], ColumnProperty):
                self.logger.warn('An attribute ({0}) provided for filtering is invalid'.format(key))
                raise falcon.errors.HTTPBadRequest('Invalid attribute', 'An attribute provided for filtering is invalid')
            if comparison == '=':
                resources = resources.filter(attr == value)
            elif comparison == 'null':
                if value != '0':
                    resources = resources.filter(attr.is_(None))
                else:
                    resources = resources.filter(attr.isnot(None))
            elif comparison == 'startswith':
                resources = resources.filter(attr.like('{0}%'.format(value)))
            elif comparison == 'contains':
                resources = resources.filter(attr.like('%{0}%'.format(value)))
            elif comparison == 'lt':
                resources = resources.filter(attr < value)
            elif comparison == 'lte':
                resources = resources.filter(attr <= value)
            elif comparison == 'gt':
                resources = resources.filter(attr > value)
            elif comparison == 'gte':
                resources = resources.filter(attr >= value)
            else:
                raise falcon.errors.HTTPBadRequest('Invalid attribute', 'An attribute provided for filtering is invalid')

        resp.status = falcon.HTTP_OK
        req.context['result'] = {
            'data': [
                self.serialize(resource) for resource in resources
            ],
        }

    def on_post(self, req, resp, *args, **kwargs):
        """
        Add an item to the collection.
        """
        attributes = self.deserialize(kwargs, req.context['doc'] if 'doc' in req.context else None)
        resource = self.model(**attributes)

        self.db_session.add(resource)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as err:
            # Cases such as unallowed NULL value should have been checked
            # before we got here (e.g. validate against schema
            # using falconjsonio) - therefore assume this is a UNIQUE
            # constraint violation
            self.db_session.rollback()
            raise falcon.errors.HTTPConflict('Conflict', 'Unique constraint violated')
        except sqlalchemy.exc.ProgrammingError as err:
            self.db_session.rollback()
            if err.orig.args[1] == '23505':
                raise falcon.errors.HTTPConflict('Conflict', 'Unique constraint violated')
            else:
                raise
        except:
            self.db_session.rollback()
            raise

        resp.status = falcon.HTTP_CREATED
        req.context['result'] = {
            'data': self.serialize(resource),
        }

    def on_patch(self, req, resp, *args, **kwargs):
        """
        Update a collection.

        For now, it only supports adding entities to the collection, like this:

        {
            'patches': [
                {'op': 'add', 'path': '/', 'value': {'name': 'Jim', 'age', 25}},
                {'op': 'add', 'path': '/', 'value': {'name': 'Bob', 'age', 28}}
            ]
        }

        """
        mapper  = inspect(self.model)
        patches = req.context['doc']['patches']

        for index, patch in enumerate(patches):
            # Only support adding entities in a collection patch, for now
            if 'op' not in patch or patch['op'] not in ['add']:
                raise falcon.errors.HTTPBadRequest('Invalid patch', 'Patch {0} is not valid'.format(index))
            if patch['op'] == 'add':
                if 'path' not in patch or patch['path'] != '/':
                    raise falcon.errors.HTTPBadRequest('Invalid patch', 'Patch {0} is not valid for op {1}'.format(index, patch['op']))
                try:
                    patch_value = patch['value']
                except KeyError:
                    raise falcon.errors.HTTPBadRequest('Invalid patch', 'Patch {0} is not valid for op {1}'.format(index, patch['op']))
                args = {}
                for key, value in kwargs.items():
                    key = getattr(self, 'attr_map', {}).get(key, key)
                    if getattr(self.model, key, None) is None or not isinstance(inspect(self.model).attrs[key], ColumnProperty):
                        self.logger.error("Programming error: {0}.attr_map['{1}'] does not exist or is not a column".format(self.model, key))
                        raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')
                    args[key] = value
                for key, value in patch_value.items():
                    if isinstance(mapper.columns[key].type, sqlalchemy.sql.sqltypes.DateTime):
                        args[key] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                    else:
                        args[key] = value
                resource = self.model(**args)
                self.db_session.add(resource)

        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as err:
            # Cases such as unallowed NULL value should have been checked
            # before we got here (e.g. validate against schema
            # using falconjsonio) - therefore assume this is a UNIQUE
            # constraint violation
            self.db_session.rollback()
            raise falcon.errors.HTTPConflict('Conflict', 'Unique constraint violated')
        except sqlalchemy.exc.ProgrammingError as err:
            self.db_session.rollback()
            if err.orig.args[1] == '23505':
                raise falcon.errors.HTTPConflict('Conflict', 'Unique constraint violated')
            else:
                raise
        except:
            self.db_session.rollback()
            raise

        resp.status = falcon.HTTP_OK
        req.context['result'] = {}

class SingleResource(object):
    """
    Provides CRUD facilities for a single resource.
    """
    def __init__(self, db_session, logger=None):
        self.db_session = db_session
        if logger is None:
            logger = logging.getLogger('autocrud')
        self.logger = logger

    def deserialize(self, data):
        mapper      = inspect(self.model)
        attributes  = {}

        for key, value in data.items():
            column = mapper.columns[key]
            if isinstance(column.type, sqlalchemy.sql.sqltypes.DateTime):
                attributes[key] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            elif support_geo and isinstance(column.type, Geometry) and column.type.geometry_type == 'POINT':
                point           = Point(value['x'], value['y'])
                # geoalchemy2.shape.from_shape uses buffer() which causes INSERT to fail
                attributes[key] = WKBElement(point.wkb, srid=4326)
            else:
                attributes[key] = value

        return attributes

    def serialize(self, resource):
        def _serialize_value(value):
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%dT%H:%M:%SZ')
            elif support_geo and isinstance(value, WKBElement):
                value = geoalchemy2.shape.to_shape(value)
                return {'x': value.x, 'y': value.y}
            else:
                return value
        attrs = inspect(self.model).attrs
        return {
            attr: _serialize_value(getattr(resource, attr)) for attr in attrs.keys() if isinstance(attrs[attr], ColumnProperty)
        }

    def on_get(self, req, resp, *args, **kwargs):
        """
        Return a single item.
        """
        resources = self.db_session.query(self.model)
        for key, value in kwargs.items():
            key = getattr(self, 'attr_map', {}).get(key, key)
            attr = getattr(self.model, key, None)
            if attr is None or not isinstance(inspect(self.model).attrs[key], ColumnProperty):
                self.logger.error("Programming error: {0}.attr_map['{1}'] does not exist or is not a column".format(self.model, key))
                raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')
            resources = resources.filter(attr == value)

        try:
            resource = resources.one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise falcon.errors.HTTPNotFound()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            self.logger.error('Programming error: multiple results found for get of model {0}'.format(self.model))
            raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')

        resp.status = falcon.HTTP_OK
        req.context['result'] = {
            'data': self.serialize(resource),
        }

    def on_delete(self, req, resp, *args, **kwargs):
        """
        Delete a single item.
        """
        resources = self.db_session.query(self.model)
        for key, value in kwargs.items():
            key = getattr(self, 'attr_map', {}).get(key, key)
            attr = getattr(self.model, key, None)
            if attr is None or not isinstance(inspect(self.model).attrs[key], ColumnProperty):
                self.logger.error("Programming error: {0}.attr_map['{1}'] does not exist or is not a column".format(self.model, key))
                raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')
            resources = resources.filter(attr == value)

        try:
            deleted = resources.delete()
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as err:
            # As far we I know, this should only be caused by foreign key constraint being violated
            self.db_session.rollback()
            raise falcon.errors.HTTPConflict('Conflict', 'Other content links to this')
        except sqlalchemy.exc.ProgrammingError as err:
            self.db_session.rollback()
            if err.orig.args[1] == '23503':
                raise falcon.errors.HTTPConflict('Conflict', 'Other content links to this')
            else:
                raise

        if deleted == 0:
            raise falcon.errors.HTTPNotFound()
        elif deleted > 1:
            self.db_session.rollback()
            self.logger.error('Programming error: multiple results found for delete of model {0}'.format(self.model))
            raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')

        resp.status = falcon.HTTP_OK
        req.context['result'] = {}

    def on_put(self, req, resp, *args, **kwargs):
        """
        Update an item in the collection.
        """
        resources = self.db_session.query(self.model)
        for key, value in kwargs.items():
            key = getattr(self, 'attr_map', {}).get(key, key)
            attr = getattr(self.model, key, None)
            if attr is None or not isinstance(inspect(self.model).attrs[key], ColumnProperty):
                self.logger.error("Programming error: {0}.attr_map['{1}'] does not exist or is not a column".format(self.model, key))
                raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')
            resources = resources.filter(attr == value)

        try:
            resource = resources.one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise falcon.errors.HTTPNotFound()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            self.logger.error('Programming error: multiple results found for put of model {0}'.format(self.model))
            raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')

        attributes = self.deserialize(req.context['doc'])
        for key, value in attributes.items():
            setattr(resource, key, value)

        self.db_session.add(resource)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as err:
            # Cases such as unallowed NULL value should have been checked
            # before we got here (e.g. validate against schema
            # using falconjsonio) - therefore assume this is a UNIQUE
            # constraint violation
            self.db_session.rollback()
            raise falcon.errors.HTTPConflict('Conflict', 'Unique constraint violated')
        except sqlalchemy.exc.ProgrammingError as err:
            self.db_session.rollback()
            if err.orig.args[1] == '23505':
                raise falcon.errors.HTTPConflict('Conflict', 'Unique constraint violated')
            else:
                raise
        except:
            self.db_session.rollback()
            raise

        resp.status = falcon.HTTP_OK
        req.context['result'] = {
            'data': self.serialize(resource),
        }

    def on_patch(self, req, resp, *args, **kwargs):
        """
        Update part of an item in the collection.
        """
        resources = self.db_session.query(self.model)
        for key, value in kwargs.items():
            key = getattr(self, 'attr_map', {}).get(key, key)
            attr = getattr(self.model, key, None)
            if attr is None or not isinstance(inspect(self.model).attrs[key], ColumnProperty):
                self.logger.error("Programming error: {0}.attr_map['{1}'] does not exist or is not a column".format(self.model, key))
                raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')
            resources = resources.filter(attr == value)

        try:
            resource = resources.one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise falcon.errors.HTTPNotFound()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            self.logger.error('Programming error: multiple results found for patch of model {0}'.format(self.model))
            raise falcon.errors.HTTPInternalServerError('Internal Server Error', 'An internal server error occurred')

        attributes = self.deserialize(req.context['doc'])
        for key, value in attributes.items():
            setattr(resource, key, value)

        self.db_session.add(resource)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as err:
            # Cases such as unallowed NULL value should have been checked
            # before we got here (e.g. validate against schema
            # using falconjsonio) - therefore assume this is a UNIQUE
            # constraint violation
            self.db_session.rollback()
            raise falcon.errors.HTTPConflict('Conflict', 'Unique constraint violated')
        except sqlalchemy.exc.ProgrammingError as err:
            self.db_session.rollback()
            if err.orig.args[1] == '23505':
                raise falcon.errors.HTTPConflict('Conflict', 'Unique constraint violated')
            else:
                raise
        except:
            self.db_session.rollback()
            raise

        resp.status = falcon.HTTP_OK
        req.context['result'] = {
            'data': self.serialize(resource),
        }
