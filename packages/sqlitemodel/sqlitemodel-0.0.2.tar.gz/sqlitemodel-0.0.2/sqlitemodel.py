# -*- coding: utf-8 -*-

"""
Copyright (c) 2016, René Tanczos <gravmatt@gmail.com> (Twitter @gravmatt)
The MIT License (MIT)

sqlitemodel is a wrapper for the sqlite3 database that enables you to
create models you can easily query, save and update.

Project on github https://github.com/gravmatt/sqlitemodel
"""

__author__ = 'Rene Tanczos'
__version__ = '0.0.2'
__license__ = 'MIT'

import sqlite3, copy


class SQL:
    '''SQL builder to generate SQL statements'''

    def __init__(self):
        self.__command = None
        self.__select = ''
        self.__update = ''
        self.__delete = ''
        self.__insert = ''
        self.__create = ''
        self.__columns = []
        self.__values = []
        self.values = []
        self.__from = ''
        self.__where = []
        self.__orderBy = ''
        self.__limit = ''


    def CREATE(self, table):
        self.__command = 'create'
        self.__create = 'CREATE TABLE IF NOT EXISTS %s ' % table
        self.__create += '(%s);'
        return self


    def COLUMN(self, name, type):
        self.__columns.append('%s %s' % (name, type))
        return self


    def SELECT(self, *fields):
        self.__command = 'select'
        self.__select = 'SELECT '
        if(fields):
            self.__select += ', '.join(fields)
        else:
            self.__select += 'rowid, *'
        return self


    def UPDATE(self, table):
        self.__command = 'update'
        self.__update = 'UPDATE %s SET ' % table
        return self


    def SET(self, field, value):
        self.__values.append((field, value))
        return self


    def DELETE(self, table):
        self.__command = 'delete'
        self.__delete = 'DELETE FROM %s' % table
        return self


    def INSERT(self, table):
        self.__command = 'insert'
        self.__insert = 'INSERT INTO %s ' % table
        return self


    def VALUES(self, **values):
        self.__values = list({(k, values[k]) for k in values})
        return self


    def FROM(self, table):
        self.__from = ' FROM %s' % table
        return self


    def WHERE(self, field, operator, value):
        self.__where.append((field, operator, value))
        return self


    def AND(self):
        self.__where.append((None, 'AND', None))
        return self


    def OR(self):
        self.__where.append((None, 'OR', None))
        return self


    def LIMIT(self, offset, max):
        self.__limit = ' LIMIT %s,%s' % (offset, max)
        return self


    def ORDER_BY(self, field, direction):
        self.__orderBy = ' ORDER BY %s %s' % (field, direction)
        return self


    def getValues(self):
        return tuple(self.values) if self.values else ();


    def toStr(self):
        sql = None
        where = ''
        if(self.__where):
            where = ' WHERE '
            wherebuild = []
            for t in self.__where:
                if(not t[0] and not t[2]):
                    wherebuild.append(t[1])
                else:
                    wherebuild.append('%s%s?' % (t[0], t[1]))
            where += ' '.join(wherebuild)

        if(self.__command == 'select'):
            sql = self.__select + self.__from + where + self.__orderBy + self.__limit + ';'
        elif (self.__command == 'insert'):
            sql = self.__insert + '(' + ','.join(['%s' % t[0] for t in self.__values]) + ') VALUES (' + ('?,'*len(self.__values))[:-1] + ');'
            self.values = [t[1] for t in self.__values]
        elif (self.__command == 'update'):
            sql = self.__update + ', '.join(['%s=%s' % (t[0], '?') for t in self.__values]) + where + ';'
            self.values = [t[1] for t in self.__values]
        elif (self.__command == 'delete'):
            sql = self.__delete + where + ';'
            self.values = [t[1] for t in self.__values]
        elif(self.__command == 'create'):
            sql = self.__create % ', '.join(self.__columns)

        if(self.__where):
            self.values = [t[2] for t in self.__where if t[0] or t[2]]

        return sql


class Model:
    '''Abstracts the communication with the database and makes it easy to store objects'''

    def __init__(self, id=None, dbfile=None):
        self.id = id
        self._dbfile = dbfile


    def columns(self):
        pass


    def tablename(self):
        pass


    def createTable(self):
        with Database(self._dbfile) as db:
            db.createTable(self)


    def save(self):
        with Database(self._dbfile) as db:
            db.save(self)


    def delete(self):
        with Database(self._dbfile) as db:
            return db.delete(self)


    def getModel(self):
        if(self.id):
            with Database(self._dbfile) as m:
                try:
                    m.getById(self, self.id)
                except:
                    self.id = None


    def select(self, sql):
        with Database(self._dbfile) as m:
            return m.select(self, sql)


    def selectOne(self, sql):
        users = self.select(sql)
        return users[0] if users else None


class Database:
    '''Represents an easy to use interface to the database'''

    DB_FILE = None


    def __init__(self, dbfile=None, foreign_keys=False):
        self.dbfile = dbfile if dbfile else Database.DB_FILE
        self.conn = sqlite3.connect(self.dbfile)
        self.db = self.conn.cursor()
        if(foreign_keys):
            self.db.execute('PRAGMA foreign_keys = ON;')


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


    def close(self):
        if(self.conn):
            self.conn.close();


    def _get_model_column_names(self, model):
        return [n['name'] for n in model.columns()]


    def createTable(self, model):
        sql = SQL().CREATE(model.tablename())
        for column in model.columns():
            sql.COLUMN(column['name'], column['type'])
        with Database() as db:
            db.db.execute(sql.toStr())
            db.conn.commit()


    def save(self, model):
        values = [model.__dict__[i] for i in self._get_model_column_names(model)]
        if(model.id):
            v = ','.join(['%s=?' % i for i in self._get_model_column_names(model)])
            sql = 'UPDATE %s SET %s WHERE rowid=?' % (model.tablename(), v)
            values += [model.id]
        else:
            f = ','.join(self._get_model_column_names(model))
            v = ('?,'*len(self._get_model_column_names(model)))[:-1]
            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (model.tablename(), f, v)
        self.db.execute(sql, values)
        self.conn.commit()
        if(self.db.lastrowid):
            model.id = self.db.lastrowid
        return model.id


    def delete(self, model):
        if(model.id):
            sql = 'DELETE FROM %s WHERE rowid=?;' % model.tablename()
            self.db.execute(sql, (model.id,))
            self.conn.commit()
            return True
        else:
            return False


    def select(self, model, sql, values=()):
        if(sql.__class__ == SQL):
            sql.SELECT().FROM(model.tablename())
            self.db.execute(sql.toStr(), sql.getValues())
        else:
            self.db.execute(sql, values)
        columns = [t[0] for t in self.db.description]
        objects = []
        row = self.db.fetchone()
        mrange = None
        try:
            mrange = xrange
        except:
            mrange = range
        while(row):
            o = copy.deepcopy(model)
            for i in mrange(len(columns)):
                k = 'id' if columns[i] == 'rowid' else columns[i]
                o.__dict__[k]=row[i]
            row = self.db.fetchone()
            objects.append(o)
        return objects


    def selectOne(self, model, sql, values=()):
        res = self.select(model, sql, values)
        return res[0] if len(res) > 0 else None


    def selectById(self, model, id):
        return self.selectOne(model, SQL().WHERE('rowid', '=', id))


    def getRaw(self, sql, values=(), max=-1):
        query = sql.toStr() if sql.__class__ == SQL else sql
        self.db.execute(query, sql.values if sql.__class__ == SQL else values)
        keys = [t[0] for t in self.db.description]
        return (keys, self.db.fetchmany(max))


    def getDict(self, sql, values=(), max=-1):
        header, raw = self.getRaw(sql, values, max)
        table = []
        for row in raw:
            obj = {}
            headIdx = 0
            for name in header:
                obj[name] = row[headIdx]
                headIdx += 1
            table.append(obj)
        return table
