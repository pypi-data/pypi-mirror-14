import copy
import datetime
import math
from collections import Counter

import pymongo
from tornado import gen

from tornado_async_odm import *
from tornado_async_odm import dbclient
from tornado_async_odm.errors import BadFormatError


class DBDocument(dict):
    """ Represents MongoDB database collection (table-equivalent of SQL)
    """

    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):

        if not hasattr(self, 'db_name'):
            # raise key error if does not exist
            self.db_name = kwargs.pop('db_name')

        # Check for db and collection name attributes
        if not hasattr(self, 'collection_name'):
            # raise key error if does not exist
            self.collection_name = kwargs.pop('collection_name')

        # Check for db and collection names
        if not self.db_name or not self.collection_name:
            raise ValueError('db_name and collection_name must not be None')

        # Check if fields is defined
        if not hasattr(self, 'fields'):
            raise AttributeError('fields must be defined for DBDocument class')

        if hasattr(self, 'csv_fields'):

            temp_csv_fields = copy.copy(self.csv_fields)

            if 'action' not in temp_csv_fields:
                raise ValueError('csv_fields must contain action field')

            temp_csv_fields.remove('action')

            if not set(temp_csv_fields) < set(self.fields.keys()):
                raise AttributeError('csv_fields must be subset of fields with exception of action field')

        if hasattr(self, 'index_fields'):
            if not set(self.index_fields) <= set(self.fields.keys()):
                raise AttributeError('index_fields must be subset of fields. index_fields: ' + str(self.index_fields) + ', fields: ' + str(self.fields.keys()))

        # Check if database connection has been established
        if not dbclient.db_connection:
            raise RuntimeError('database connection not initialized')

        # Get database
        self._database = dbclient.db_connection[self.db_name]

        # x509 authentication
        if dbclient.ssl and not self._database.authenticate(dbclient.x509_username, mechanism='MONGODB-X509'):
            raise ConnectionError('error authenticating ' + dbclient.x509_username + ' on ' + self.db_name)

        # Get collection
        self._collection = self._database[self.collection_name]

        # initialize items
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def __setitem__(self, key, value):
        """ Set dictionary item
        Override __setitem__method to update dict key-value pair
        Ensure field is valid        self.csv_file = csv_file
        """

        # exclude auto-generated object id, '_id'
        if key not in self.fields.keys() and key != '_id':
                raise LookupError('Key ' + key + ' is not valid for ' + self.__class__.__name__)

        if value is None:
            raise ValueError('Key ' + key + ' has None value')

        value = self.validate_field(key, value)

        dict.__setitem__(self, key, value)

    def __eq__(self, other):
        """ Override comparison method
        """

        if not isinstance(other, DBDocument):
            raise NotImplementedError

        for k, v in other.items():
            if k not in self.keys() or self[k] != other[k]:
                return False
        return True

    def validate_field(self, key, value):
        """ Validate field key-value pair
        """

        # if _id is not in field, ignore
        if key == '_id' and key not in self.fields:
            return value

        for data_type in self.fields[key]:
            if data_type == TYPE_NONE:
                pass
            elif data_type == TYPE_INT:
                pass
            elif data_type == TYPE_BOOL:
                if not isinstance(value, bool):
                    raise ValueError(key + ' must be boolean. Found: ' + value)
            elif data_type == TYPE_DATE:
                pass
            elif data_type == TYPE_STR:
                value = value.strip()
            elif data_type == TYPE_LOWER:
                value = value.strip().lower()
            elif data_type == TYPE_STR_A0:
                value = value.strip()
                if not regex_a0.match(value):
                    raise ValueError(key + ' must only consists of letters/numbers. Found: ' + value)
            elif data_type == TYPE_STR_LETTERS:
                value = value.strip()
                if not regex_letters.match(value):
                    raise ValueError(key + ' must only consists of letters. Found: ' + value)
            elif data_type == TYPE_STR_ASPACE:
                value = value.strip()
                if not regex_aspace.match(value):
                    raise ValueError(key + ' must only consists of letters/spaces. Found: ' + value)
            elif data_type == TYPE_EMAIL:
                value = value.strip()
                if not regex_email.match(value):
                    raise ValueError(key + ' must be valid email. Found: ' + value)
            elif data_type == TYPE_PHONE:
                value = value.strip()
                if not regex_phone.match(value):
                    raise ValueError(key + ' must be valid phone number. Found: ' + value)
            else:
                raise ValueError(data_type + ' for ' + key + ' is not a valid data type')

        return value

    def validate(self):
        """ Validate dictionary data
        Check if all required fields exist
        Ignore _id as its special case
        """
        if not Counter(self.keys()-['_id']) == Counter(self.fields.keys()-['_id']):
            raise BadFormatError('incomplete object data - requires: ' + str(self.fields.keys()) + ' but has ' + str(self.keys()))

    def get_timestamp(self):
        now = datetime.datetime.utcnow()
        now = now.replace(microsecond = int(math.ceil(now.microsecond / 1000.0)) * 1000)
        return now

    def modify_timestamp(self, timestamp):
        timestamp = timestamp.replace(microsecond = int(math.ceil(timestamp.microsecond / 1000.0)) * 1000)
        return timestamp

    def update_timestamp(self, field='timestamp'):
        """ Update timestamp field
         MongoDB only supports datetime (converted to bson) with resolution up to 1000 microseconds
         This method rounds-down current time to 1000 microseconds resolution.
        """
        self[field] = self.get_timestamp()

    def keep_only_index_fields(self):
        """ Keep only index fields
        Useful when want to keep only a few fields for query
        """
        if not hasattr(self, 'index_fields'):
            raise AttributeError('index_fields must be defined in order to call keep_only_index_fields method')
        cached_keys = []
        for key in self.keys():
            if key not in self.index_fields:
                cached_keys.append(key)
        for target_key in cached_keys:
            del self[target_key]
        return True

    @gen.coroutine
    def create_index(self):
        if hasattr(self, 'index_fields'):
            index_sets = []
            for field in self.index_fields:
                index_sets.append((field, pymongo.ASCENDING))
            yield self._collection.create_index(index_sets, unique=True)

    @gen.coroutine
    def exists(self):
        res = yield self._collection.find(self).limit(1).count()
        return (res != 0)

    @gen.coroutine
    def find_one(self, sort_key=None, sort_order=None):
        """

        """
        if sort_key and sort_order:
            cursor = self._collection.find(self).sort(sort_key, sort_order).limit(1)
            yield cursor.fetch_next
            res = cursor.next_object()
        else:
            res = yield self._collection.find_one(self)
        if not res:
            return None
        self.reload(res)
        self.validate()
        return self

    @gen.coroutine
    def find(self, distinct=None):
        res = []
        if distinct:
            cursor = yield self._collection.find(self).distinct(distinct)
            res = cursor
        else:
            cursor = self._collection.find(self)
            while (yield cursor.fetch_next):
                item = self.__class__(cursor.next_object())
                item.validate()
                res.append(item)
            if len(res) == 0:
                return None
        return res

    def reload(self, res):
        for k, v in res.items():
            self[k] = v

    @gen.coroutine
    def save(self, generate_timestamp=True):
        if generate_timestamp:
            self.update_timestamp()
        else:
            if 'timestamp' in self:
                self['timestamp'] = self.modify_timestamp(self['timestamp'])
        self.validate()
        yield self.create_index()
        res = yield self._collection.insert(self)
        return res

    @gen.coroutine
    def update(self, updated_values=None):
        if updated_values:
            self.updated_values = updated_values
        if not self.updated_values:
            raise ValueError('updated_values must be defined before calling update()')
        # ensure updated_values have valid fields
        if not set(self.updated_values.keys()) < set(self.fields.keys()):
            raise ValueError('updated_values must be subset of fields')
        # verify updated_values
        for field in self.updated_values:
            self.validate_field(field, self.updated_values[field])
        self.updated_values['timestamp'] = self.get_timestamp()
        yield self.create_index()
        res = yield self._collection.update(self, {'$set':self.updated_values})
        # TODO: even if there's an issue, it might return ok=1
        return res['ok'] == 1

    @gen.coroutine
    def remove(self):
        yield self.create_index()
        res = yield self._collection.remove(self)
        # TODO: even if there's an issue, it might return ok=1
        return res['ok'] == 1

    @gen.coroutine
    def drop_database(self):
        yield dbclient.db_connection.drop_database(self.db_name)

class DBDocumentList(list):
    """ DBDocument List for bulk operation

    op_not_allowed: operations not allowed
    """

    logger = logging.getLogger(__name__)

    def __init__(self, db_name, collection_name, op_not_allowed=[], *args):
        list.__init__(self, *args)

        self.db_name = db_name
        self.collection_name = collection_name
        self.op_not_allowed = op_not_allowed
        self._database = dbclient.db_connection[self.db_name]
        self._collection = self._database[self.collection_name]
        self._bulk = self._collection.initialize_unordered_bulk_op()

    def append(self, item):
        if not isinstance(item, DBDocument):
            raise TypeError('only objects with type ' + DBDocument + ' are allowed')
        if item.db_name != self.db_name and item.collection_name != self.collection_name:
            raise TypeError('only objects with db: ' + self.db_name + ' , and collection: ' + self.collection_name + ' are allowed')
        super(DBDocumentList, self).append(item)

    @gen.coroutine
    def commit(self):
        for item in self:
            if not item.db_operation:
                raise ValueError('db_operation must be defined for bulk operation. Not defined for ' + str(item))
            if item.db_operation in self.op_not_allowed:
                raise ValueError('db_operation ' + item.db_operation + ' is not allowed for this type ' + str(item.__class__))
            if item.db_operation == DB_INSERT:
                item.update_timestamp()
                item.validate()
                self._bulk.insert(item)
            elif item.db_operation == DB_UPDATE:
                if not item.updated_values:
                    raise ValueError('updated_values must be defined for bulk update operation')
                self._bulk.find(item).update({'$set':item.updated_values})
            elif item.db_operation == DB_REMOVE:
                self._bulk.find(item).remove()
            else:
                raise ValueError('db_operation ' + item.db_operation + ' is invalid')
            yield item.create_index()
        if self:    
            res = yield self._bulk.execute()
            logger.info('bulk operation result: ' + str(res))
        else:
            logger.info('bulk operation not executed - list is empty!')
        # reinitialize bulk
        self._bulk = self._collection.initialize_unordered_bulk_op()

    @gen.coroutine
    def save_all(self):
        for item in self:
            item.update_timestamp()
            item.validate()
            self._bulk.insert(item)
        yield self._bulk.execute()

    @gen.coroutine
    def update_all(self):
        for item in self:
            if not item.updated_values:
                raise ValueError('updated_values must be defined before calling update()')
            self._bulk.find(item).update({'$set':item.updated_values})
        yield self._bulk.execute()

    @gen.coroutine
    def remove_all(self):
        for item in self:
            self._bulk.find(item).remove()
        yield self._bulk.execute()

