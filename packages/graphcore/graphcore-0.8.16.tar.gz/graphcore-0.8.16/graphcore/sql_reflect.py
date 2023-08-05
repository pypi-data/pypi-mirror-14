from sqlalchemy.engine import reflection

import inflect

from .sql_query import SQLQuery

_pluralizer = inflect.engine()


def _column_to_property(column):
    """ assumes the column name has _id postfix """
    return column[:-3]


class SQLReflector(object):

    def __init__(self, graphcore, engine, sql_query_class=SQLQuery,
                 param_style='%s', exclude_tables=None):
        """ add rules to graphcore instance based on schema found in SQL db.

        graphcore: Graphcore instance
        engine: sqlalchemy.engine instance

        assumes all tables have a primary key id
        """
        self.graphcore = graphcore
        self.sql_query_class = sql_query_class
        self.param_style = param_style

        if exclude_tables is None:
            exclude_tables = []

        self.insp = reflection.Inspector.from_engine(engine)

        for table in self.insp.get_table_names():
            if table in exclude_tables:
                continue

            self._sql_reflect_table(table)

        for view in self.insp.get_view_names():
            self._sql_reflect_table(view)

    def _type_name_from_table(self, table):
        type_name = _pluralizer.singular_noun(table)

        if type_name is False:
            # unable to singularize {table}, going to assume it is
            # alredy singular
            type_name = table

        return type_name

    def _relationship(self, table, column_name):
        type_name = self._type_name_from_table(table)
        property_name = _column_to_property(column_name)

        self.graphcore.property_type(
            type_name, property_name, property_name
        )

        self.graphcore.register_rule(
            ['{}.id'.format(type_name)],
            '{}.{}.id'.format(type_name, property_name),
            function=self._sql_query_property(table, column_name),
        )

        # backref
        self.graphcore.property_type(
            property_name, _pluralizer.plural(type_name), type_name
        )
        self.graphcore.register_rule(
            ['{}.id'.format(property_name)],
            '{}.{}.id'.format(property_name, _pluralizer.plural(type_name)),
            function=self._sql_query_backref(table, column_name),
            cardinality='many'
        )

    def _property(self, table, column_name):
        type_name = self._type_name_from_table(table)

        return self.graphcore.register_rule(
            ['{}.id'.format(type_name)],
            '{}.{}'.format(type_name, column_name),
            function=self._sql_query_property(table, column_name),
        )

    def _unground_property(self, table, column_name):
        type_name = self._type_name_from_table(table)

        return self.graphcore.register_rule(
            [], '{}.{}'.format(type_name, column_name),
            function=self._sql_query_unground_property(table, column_name),
            cardinality='many'
        )

    def _sql_query_backref(self, table, column):
        return self.sql_query_class(
            [table], '{}.id'.format(table), {},
            input_mapping={
                'id': '{}.{}'.format(table, column),
            }, one_column=True, param_style=self.param_style
        )

    def _sql_query_property(self, table, column):
        return self.sql_query_class(
            [table], '{}.{}'.format(table, column), {},
            input_mapping={
                'id': '{}.id'.format(table),
            }, one_column=True, first=True, param_style=self.param_style
        )

    def _sql_query_unground_property(self, table, column):
        return self.sql_query_class(
            [table], '{}.{}'.format(table, column), {},
            one_column=True, param_style=self.param_style
        )

    def sql_reflect_column(self, table, column_name):
        if column_name[-3:] == '_id':
            self._relationship(table, column_name)
        else:
            self._property(table, column_name)

    def _sql_reflect_table(self, table_name):
        columns = self.insp.get_columns(table_name)

        for column in columns:
            if column['name'] == 'id':
                self._unground_property(table_name, column['name'])
            else:
                self.sql_reflect_column(table_name, column['name'])
