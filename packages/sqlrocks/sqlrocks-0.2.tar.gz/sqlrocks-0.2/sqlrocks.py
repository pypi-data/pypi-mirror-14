# -*- coding: utf-8 -*-

from collections import Iterable


class Sql:
    def __init__(self, sql='', args=None, db=None):
        """
        Init Sql instance

        :param str sql: sql string
        :param list args: sql arguments
        :param Db db: Db instance
        :return: Sql instance
        """
        self.sql = sql
        self.args = args if args else []
        self.db = db

    def rocks(self):
        """
        MAYDAY ROCKS \m/
        """
        self.db.rocks(self.sql, self.args)
        return self.db.cur

    def select(self, expr='*'):
        """
        Select clause

        :param Sql|str|Iterable expr: expression
        :return: Sql instance
        """
        expr, args = Sql.parse_expr(expr)

        self.sql += 'SELECT ' + expr
        self.args.extend(args)

        return self

    def delete(self, expr=None):
        """
        Delete clause

        :param Sql|str|Iterable expr: expression
        :return: Sql instance
        """
        self.sql += 'DELETE'

        if expr:
            expr, args = Sql.parse_expr(expr)
            self.sql += ' ' + expr
            self.args.extend(args)

        return self

    def fr(self, expr):
        """
        From clause

        :param Sql|str|Iterable expr: expression
        :return: Sql instance
        """
        expr, args = Sql.parse_expr(expr)

        self.sql += ' FROM ' + expr
        self.args.extend(args)

        return self

    def use_index(self, expr):
        """
        Use index clause

        :param str|Iterable expr: expression
        :return: Sql instance
        """
        self.sql += ' USE INDEX(' + self.add_quote(expr) + ')'
        return self

    def ignore_index(self, expr):
        """
        Ignore index clause

        :param str|Iterable expr: expression
        :return: Sql instance
        """
        self.sql += ' IGNORE INDEX(' + self.add_quote(expr) + ')'
        return self

    def join(self, expr):
        """
        From clause

        :param str expr: expression
        :return: Sql instance
        """
        self.sql += ' ' + expr
        return self

    def where(self, *args, **kwargs):
        """
        Where clause

        :param dict|list|tuple|str args: where conditions
        :return: Sql instance
        """
        cond = args[0] if args else kwargs.items()

        cond_str, cond_args = Sql.parse_where_cond(cond)

        if cond_str:
            self.sql += ' WHERE ' + cond_str
        if cond_args:
            self.args.extend(cond_args)

        return self

    def group_by(self, expr):
        """
        Group by clause

        :param Sql|str|Iterable expr: expression
        :return: Sql instance
        """
        expr, args = Sql.parse_expr(expr)

        self.sql += ' GROUP BY ' + expr
        self.args.extend(args)

        return self

    def having(self, *args, **kwargs):
        """
        Having clause

        :param dict|list|tuple|str cond: where conditions
        :return: Sql instance
        """
        cond = args[0] if args else kwargs.items()

        cond_str, cond_args = Sql.parse_where_cond(cond)

        if cond_str:
            self.sql += ' HAVING ' + cond_str
        if cond_args:
            self.args.extend(cond_args)

        return self

    def order_by(self, expr):
        """
        Order by clause

        :param Sql|str|Iterable expr: expression
        :return: Sql instance
        """
        expr, args = Sql.parse_expr(expr)

        self.sql += ' ORDER BY ' + expr if expr else ''
        self.args.extend(args)

        return self

    def limit(self, a, b=None):
        """
        Limit clause

        :param list|tuple|int|str a: a
        :param int|str b: b
        :return: Sql instance
        """
        if isinstance(a, (list, tuple)):
            self.sql += ' LIMIT %s, %s' % (a[0], a[1])
        else:
            if a is None:
                pass
            elif b is None:
                self.sql += ' LIMIT %s' % a
            else:
                self.sql += ' LIMIT %s, %s' % (a, b)

        return self

    def insert(self, table):
        """
        Insert clause

        :param str table: table name
        :return: Sql instance
        """
        self.sql += 'INSERT INTO `%s`' % table
        return self

    def cols(self, cols):
        """
        Insert columns

        :param str|Iterable cols: expression
        :return: Sql instance
        """
        self.sql += '(%s)' % Sql.add_quote(cols)
        return self

    def vals(self, *args):
        """
        Insert values

        :param args: insert values
        :return: Sql instance
        """
        self.sql += ' VALUES'

        values = args if len(args) > 1 else args[0]

        if isinstance(values[0], (list, tuple)):
            for vals in values:
                self.sql += '(' + ('%s,' * len(vals))[:-1] + '),'
                self.args.extend(vals)
            self.sql = self.sql[0:-1]
        else:
            self.sql += '(' + ('%s,' * len(values))[:-1] + ')'
            self.args.extend(values)

        return self

    def update(self, table):
        """
        Update clause

        :param str table: table name
        :return: Sql instance
        """
        self.sql += 'UPDATE `%s`' % table
        return self

    def set(self, expr):
        self.sql += ' SET '

        if isinstance(expr, dict):
            for k in expr:
                self.sql += '`' + k + '`=%s, '
                self.args.append(expr[k])
            self.sql = self.sql[0:-2]
        else:
            expr, args = Sql.parse_expr(expr)
            self.sql += expr
            self.args.extend(args)

        return self

    def alias(self, name):
        """
        Add alias

        :param str name: name
        :return: Sql Instance
        """
        self.sql += ' AS `%s`' % name
        return self

    def as_subquery(self, alias=None):
        """
        Set subquery

        :param str alias: subquery alias
        :return: Sql instance
        """
        if alias is None:
            self.sql = '(%s)' % self.sql
        else:
            self.sql = '(%s) AS `%s`' % (self.sql, alias)
        return self

    @staticmethod
    def add_quote(expr):
        """
        Add quote

        :param str|Iterable expr: expression
        :return: string
        """
        if isinstance(expr, str):
            return '`' + expr + '`'
        return '`' + '`, `'.join(expr) + '`'

    @staticmethod
    def parse_expr(expr):
        """
        parse expression

        :param Sql|str|Iterable expr: expression
        :return: expression string
        """
        if isinstance(expr, Sql):
            return expr.sql, expr.args
        elif isinstance(expr, str) or expr is None:
            return expr, []
        else:
            str_list = []
            arg_list = []

            for i in expr:
                if isinstance(i, Sql):
                    arg_list.extend(i.args)
                    str_list.append(i.sql)
                else:
                    str_list.append(i)

            return ', '.join(str_list), arg_list

    @staticmethod
    def parse_cond(v):
        """
        parse condition

        :param list|tuple v: condition details
        :return: condition string and argument
        """
        cond_len = len(v)

        if cond_len == 1:
            return v[0], None
        elif cond_len == 2:
            if isinstance(v[1], Sql):
                return '%s = %s' % (v[0], v[1].sql), v[1].args
            else:
                return '%s = %s' % (v[0], '%s'), v[1]
        elif cond_len == 3:
            key = v[1].upper()

            if key == 'BETWEEN':
                return '%s %s %s' % (v[0], v[1], '%s AND %s'), v[2]
            elif key in {'IN', 'NOT IN'}:
                if isinstance(v[2], Sql):
                    return '%s %s %s' % (v[0], v[1], v[2].sql), v[2].args
                else:
                    placeholder = ('%s,' * len(v[2]))[:-1]
                    return '%s %s (%s)' % (v[0], v[1], placeholder), v[2]
            else:
                if isinstance(v[2], Sql):
                    return '%s %s %s' % (v[0], v[1], v[2].sql), v[2].args
                else:
                    return '%s %s %s' % (v[0], v[1], '%s'), v[2]

    @staticmethod
    def flatten_where_cond(where_cond, cond_arg_list):
        """
        flatten where conditions

        :param dict where_cond: where conditions
        :param list cond_arg_list: condition argument list
        :return: condition string
        """
        # get conjunction
        conj = list(where_cond.keys())[0]
        cond_str_list = []

        for val in where_cond[conj]:
            if isinstance(val, dict):
                cond_str_list.append(Sql.flatten_where_cond(val, cond_arg_list))
            elif isinstance(val, str):
                cond_str_list.append(val)
            else:
                # list or tuple
                cond_str, cond_arg = Sql.parse_cond(val)
                cond_str_list.append(cond_str)

                if cond_arg is not None:
                    if isinstance(cond_arg, str):
                        cond_arg_list.append(cond_arg)
                    elif isinstance(cond_arg, Iterable):
                        cond_arg_list.extend(cond_arg)
                    else:
                        cond_arg_list.append(cond_arg)

        conj = ' %s ' % conj

        return '(%s)' % conj.join(cond_str_list)

    @staticmethod
    def parse_where_cond(where_cond):
        """
        parse where conditions

        :param dict|list|tuple|str where_cond: where conditions
        :return: condition string
        """
        if where_cond is None:
            return '', None
        elif isinstance(where_cond, str):
            return where_cond, None
        else:
            # set default conjunction
            if not isinstance(where_cond, dict):
                if isinstance(where_cond, tuple):
                    where_cond = [where_cond]
                where_cond = {'AND': where_cond}

            cond_arg_list = []
            cond_str = Sql.flatten_where_cond(where_cond, cond_arg_list)

            return cond_str, cond_arg_list

    @property
    def val(self):
        return self.sql

    def __repr__(self):
        return self.sql


class Db:
    def __init__(self, conn, cur, debug=False):
        """
        Init Db instance

        :param conn: MySQLdb conn
        :param cur: MySQLdb cursor
        :param bool debug: default False
        :return: Db instance
        """
        self.conn = conn
        self.cur = cur
        self.debug = debug

    def sql(self):
        """
        Create a Sql instance

        :return: Sql instance
        """
        return Sql(db=self)

    def select(self, expr='*'):
        """
        Create a Sql instance

        :param Sql|str|Iterable expr: expression
        :return: Sql instance
        """
        return self.sql().select(expr)

    def count(self, table, where=None):
        """
        Count table

        :param str table: table name
        :param dict|list|tuple|str where: where conditions
        :return: int
        """
        sql = self.select('COUNT(*)').fr('`%s`' % table)
        result = sql.where(where).rocks().fetchone()
        return result['COUNT(*)'] if isinstance(result, dict) else result[0]

    def insert(self, table, data):
        """
        Insert clause

        :param str table: table name
        :param dict data: data
        :return: last row id
        """
        return self.sql().insert(table).set(data).rocks().lastrowid

    def update(self, table, data, where=None, order_by=None, limit=None):
        """
        Update clause

        :param str table: table name
        :param dict data: data
        :param dict|list|tuple|str where: where conditions
        :param str|Iterable order_by: order_by
        :param list|tuple|int|str limit: limit
        :return: affected rows
        """
        sql = self.sql().update(table).set(data).where(where)
        return sql.order_by(order_by).limit(limit).rocks().rowcount

    def save(self, table, data, pk, insert=None):
        """
        Save data

        :param str table: table name
        :param dict data: data
        :param str pk: primary key
        :param bool insert: insert
        :return: last row id or affected rows
        """
        if insert or pk not in data:
            return self.insert(table, data)
        else:
            sub_data = {k: data[k] for k in data if k != pk}
            return self.update(table, sub_data, (pk, data[pk]))

    def delete(self, table, where=None, order_by=None, limit=None):
        """
        Delete clause

        :param str table: table name
        :param dict|list|tuple|str where: where conditions
        :param str|Iterable order_by: order_by
        :param list|tuple|int|str limit: limit
        :return: affected rows
        """
        sql = self.sql().delete().fr('`%s`' % table).where(where)
        return sql.order_by(order_by).limit(limit).rocks().rowcount

    def rocks(self, sql, args=None):
        """
        Execute sql

        :param str sql: sql
        :param Iterable args: args
        :return:
        """
        if self.debug:
            print('%s\n%s' % (sql, args))
        return self.cur.execute(sql, args)

    def commit(self, *args, **kwargs):
        """
        Commit

        :param args:
        :param kwargs:
        """
        self.conn.commit(*args, **kwargs)

    def rollback(self, *args, **kwargs):
        """
        Rollback

        :param args:
        :param kwargs:
        """
        self.conn.rollback(*args, **kwargs)

    def close(self, *args, **kwargs):
        """
        Close connection

        :param args:
        :param kwargs:
        """
        self.conn.close(*args, **kwargs)


class Model:
    """:type db: Db"""
    db = None

    # table name
    table = ''

    # primary key
    pk = 'id'

    def __init__(self, *args, **kwargs):
        """
        Init Model instance

        :return: Model instance
        """
        self._row = args[0] if args else kwargs

    def __getattr__(self, item):
        """
        Get field from attr

        :param str item: item
        :return:
        """
        if item in self._row:
            return self._row[item]
        else:
            raise AttributeError

    def __getitem__(self, item):
        """
        Get field from item

        :param str item: item
        :return:
        """
        if item in self._row:
            return self._row[item]
        else:
            raise AttributeError

    @classmethod
    def to_obj(cls, data):
        """
        Mapping table row(s) to class object(s)

        :param list|tuple|dict data: table rows
        :return: class objects
        """
        if data is None:
            return None
        elif isinstance(data, dict):
            return cls(data)
        else:
            return [cls(i) for i in data]

    @classmethod
    def select(cls, expr='*'):
        """
        Select clause

        :param Sql|str|Iterable expr: expression
        :return: Sql instance
        """
        return cls.db.select(expr).fr(cls.table)

    @classmethod
    def get(cls, pk, expr='*', fetch_obj=True):
        """
        Get row(s) by pk(s)

        :param int|str|Iterable pk: primary key(s)
        :param Sql|str|Iterable expr: expression
        :param fetch_obj: default True
        :return row(s)
        """
        if isinstance(pk, Iterable) and not isinstance(pk, str):
            data = cls.select(expr).where((cls.pk, 'IN', pk)).rocks().fetchall()
        else:
            data = cls.select(expr).where((cls.pk, pk)).rocks().fetchone()

        return cls.to_obj(data) if fetch_obj else data

    @classmethod
    def one(cls, expr='*', where=None, order_by=None, fetch_obj=True):
        """
        Get one row

        :param Sql|str|Iterable expr: expression
        :param dict|list|tuple|str where: where conditions
        :param str|Iterable order_by: order_by
        :param fetch_obj: default True
        :return row
        """
        sql = cls.select(expr).where(where).order_by(order_by).limit(1)
        row = sql.rocks().fetchone()
        return cls.to_obj(row) if fetch_obj else row

    @classmethod
    def first(cls, expr='*', fetch_obj=True):
        """
        Get first row

        :param Sql|str|Iterable expr: expression
        :param fetch_obj: default True
        :return row
        """
        return cls.one(expr=expr, order_by=cls.pk, fetch_obj=fetch_obj)

    @classmethod
    def last(cls, expr='*', fetch_obj=True):
        """
        Get last row

        :param Sql|str|Iterable expr: expression
        :param fetch_obj: default True
        :return row
        """
        return cls.one(expr=expr, order_by='-' + cls.pk, fetch_obj=fetch_obj)

    @classmethod
    def exists(cls, where):
        """
        Exists

        :param dict|list|tuple|str where: where conditions
        :return: bool
        """
        return True if cls.one('*', where, fetch_obj=False) else False

    @classmethod
    def all(cls, expr='*', where=None, order_by=None, limit=None,
            fetch_obj=True):
        """
        Get rows

        :param Sql|str|Iterable expr: expression
        :param dict|list|tuple|str where: where conditions
        :param str|Iterable order_by: order_by
        :param list|tuple|int|str limit: limit
        :param fetch_obj: default True
        :return: rows
        """
        sql = cls.select(expr).where(where).order_by(order_by).limit(limit)
        rows = sql.rocks().fetchall()
        return cls.to_obj(rows) if fetch_obj else rows

    @classmethod
    def count(cls, where=None):
        """
        Count table

        :param dict|list|tuple|str where: where conditions
        :return: int
        """
        return cls.db.count(cls.table, where)

    @classmethod
    def add(cls, *args, **kwargs):
        """
        Insert clause

        :return: last row id
        """
        return cls.db.insert(cls.table, args[0] if args else kwargs)

    @classmethod
    def saved(cls, data, insert=None):
        """
        Save raw data

        :param dict data: data
        :param bool insert: default None
        :return: last row id or affected rows
        """
        return cls.db.save(cls.table, data, cls.pk, insert)

    def save(self, insert=None):
        """
        Save object

        :param bool insert: default None
        :return: last row id or affected rows
        """
        data = self.fields_filter(self.__dict__)

        if self.pk in self._row and not insert:
            # update
            where = (self.pk, self._row[self.pk])
            return self.db.update(self.table, data, where)
        else:
            # insert or update
            data.update({k: self._row[k] for k in self._row if k not in data})
            return self.db.save(self.table, data, self.pk, insert)

    @classmethod
    def update(cls, data, where=None, order_by=None, limit=None):
        """
        Update clause

        :param dict data: data
        :param dict|list|tuple|str where: where conditions
        :param str|Iterable order_by: order_by
        :param list|tuple|int|str limit: limit
        :return: affected rows
        """
        return cls.db.update(cls.table, data, where, order_by, limit)

    @classmethod
    def delete(cls, where=None, order_by=None, limit=None):
        """
        Delete clause

        :param dict|list|tuple|str where: where conditions
        :param str|Iterable order_by: order_by
        :param list|tuple|int|str limit: limit
        :return: affected rows
        """
        return cls.db.delete(cls.table, where, order_by, limit)

    def remove(self):
        """
        Delete object

        :return: affected rows
        """
        return self.db.delete(self.table, (self.pk, getattr(self, self.pk)))

    @classmethod
    def get_fields(cls):
        """
        Get table fields

        :return: fields
        :rtype list|tuple|set
        """
        return {}

    @classmethod
    def fields_filter(cls, data):
        """
        Remove irrelevant fields

        :param dict data: data
        :return: clean data
        """
        fields = cls.get_fields()
        return {k: data[k] for k in data if k in fields}

    @classmethod
    def rocks(cls, sql, args=None):
        """
        Execute sql

        :param str sql: sql
        :param Iterable args: args
        :return:
        """
        return cls.db.rocks(sql, args)
