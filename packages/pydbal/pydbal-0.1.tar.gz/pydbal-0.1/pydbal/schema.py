#!/usr/bin/env python
#
# Copyright (c) 2016 Alexander Lokhman <alex.lokhman@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import, division, print_function, with_statement

from abc import ABCMeta, abstractmethod
from binascii import crc32

from .statement import Statement
from .cache import cached


class BaseAsset:
    __metaclass__ = ABCMeta

    _name = None
    _namespace = None
    _quoted = False

    @abstractmethod
    def __init__(self, **params):
        pass

    def _set_name(self, name):
        if BaseAsset._is_identifier_quoted(name):
            self._quoted = True
            name = self._trim_quotes(name)
        if "." in name:
            self._namespace, name = name.split(".", 1)
        self._name = name

    def get_name(self):
        if self._namespace:
            return self._namespace + "." + self._name
        return self._name

    def get_namespace(self):
        return self._namespace

    @staticmethod
    def _is_identifier_quoted(identifier):
        return identifier[:1] in ("`", '"', "[")

    @staticmethod
    def _trim_quotes(identifier):
        return identifier.translate(None, '`"[]')

    def _get_quoted_name(self, platform):
        keywords = platform.get_keywords()

        def quote(identifier):
            if self._quoted or identifier in keywords:
                return platform.quote_single_identifier(identifier)
            return identifier
        return ".".join(map(quote, self.get_name().split(".")))

    @staticmethod
    def _generate_identifier_name(column_names, prefix="", max_size=30):
        def encode(column_name):
            return "%X" % (crc32(column_name) & 0xffffffff)
        return (prefix.upper() + "_" + "".join(map(encode, column_names)))[:max_size]


class Schema(BaseAsset):
    pass


class View(BaseAsset):
    def __init__(self, name, sql):
        self._set_name(name)
        self._sql = sql

    def get_sql(self):
        return self._sql


class Table(BaseAsset):
    pass


class Column(BaseAsset):
    _length = None
    _precision = 10
    _scale = 0
    _unsigned = False
    _fixed = False
    _notnull = True
    _default = None
    _autoincrement = False
    _platform_options = {}
    _column_definition = None
    _comment = None
    _custom_schema_options = {}

    def __init__(self, name, type_, options=None):
        self._set_name(name)
        self._type = type_
        if options is not None:
            self.set_options(options)

    def set_options(self, options):
        for option, value in options.iteritems():
            getattr(self, "set_" + option)(value)
        return self

    def set_length(self, length):
        if length is not None:
            self._length = int(length)
        else:
            self._length = None
        return self

    def get_length(self):
        return self._length

    def set_precision(self, precision):
        self._precision = int(precision)
        return self

    def get_precision(self):
        return self._precision

    def set_scale(self, scale):
        self._scale = int(scale)
        return self

    def get_scale(self):
        return self._scale

    def set_unsigned(self, unsigned):
        self._unsigned = bool(unsigned)
        return self

    def is_unsigned(self):
        return self._unsigned

    def set_fixed(self, fixed):
        self._fixed = bool(fixed)
        return self

    def is_fixed(self):
        return self._fixed

    def set_notnull(self, notnull):
        self._notnull = bool(notnull)
        return self

    def is_notnull(self):
        return self._notnull

    def set_default(self, default):
        self._default = default
        return self

    def get_default(self):
        return self._default

    def set_autoincrement(self, autoincrement):
        self._autoincrement = bool(autoincrement)
        return self

    def is_autoincrement(self):
        return self._autoincrement

    def set_platform_options(self, platform_options):
        if isinstance(platform_options, dict):
            self._platform_options = platform_options
        return self

    def set_platform_option(self, name, value):
        self._platform_options[name] = value
        return self

    def get_platform_option(self, name):
        return self._platform_options[name]

    def set_column_definition(self, value):
        self._column_definition = str(value)
        return self

    def get_column_definition(self):
        return self._column_definition

    def set_comment(self, comment):
        self._comment = str(comment)
        return self

    def get_comment(self):
        return self._comment

    def set_custom_schema_options(self, custom_schema_options):
        if isinstance(custom_schema_options, dict):
            self._custom_schema_options = custom_schema_options
        return self

    def set_custom_schema_option(self, name, value):
        self._custom_schema_options[name] = value
        return self

    def get_custom_schema_option(self, name):
        return self._custom_schema_options[name]


class SchemaManager:
    def __init__(self, connection):
        self._connection = connection
        self._platform = connection.get_platform()

    def __contains__(self, item):
        if isinstance(item, (list, tuple)):
            return all(x in self for x in item)
        try:
            name = item.get_name().lower()
        except AttributeError:
            name = item.lower()
        if isinstance(item, (Table, basestring)):
            return name in (x.lower() for x in self.get_table_names())
        elif isinstance(item, View):
            return name in (x.lower() for x in self.get_view_names())
        return False

    @cached
    def get_database_names(self):
        sql = self._platform.get_list_databases_sql()
        databases = self._connection.query(sql).fetch_all(Statement.FETCH_DEFAULT)
        return map(self._platform.get_database_definition, databases)

    @cached
    def get_namespace_names(self):
        sql = self._platform.get_list_namespaces_sql()
        namespaces = self._connection.query(sql).fetch_all(Statement.FETCH_DEFAULT)
        return map(self._platform.get_namespace_definition, namespaces)

    @cached
    def get_sequence_names(self, database=None):
        if database is None:
            database = self._connection.get_database()
        sql = self._platform.get_list_sequences_sql(database)
        sequences = self._connection.query(sql).fetch_all(Statement.FETCH_DEFAULT)
        return map(self._platform.get_sequence_definition, sequences)

    @cached
    def get_table_names(self):
        sql = self._platform.get_list_tables_sql()
        tables = self._connection.query(sql).fetch_all(Statement.FETCH_DEFAULT)
        return map(self._platform.get_table_definition, tables)

    @cached
    def get_tables(self):
        pass

    @cached
    def get_view_names(self, database=None):
        return map(View.get_name, self.get_views(database))

    @cached
    def get_views(self, database=None):
        if database is None:
            database = self._connection.get_database()
        sql = self._platform.get_list_views_sql(database)
        views = self._connection.query(sql).fetch_all(Statement.FETCH_DEFAULT)
        return map(lambda x: View(*self._platform.get_view_definition(x)), views)
