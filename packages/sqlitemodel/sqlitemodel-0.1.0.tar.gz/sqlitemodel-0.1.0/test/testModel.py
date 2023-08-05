#!/usr/bin/python -B

from sqlitemodel import Database, SQL, Model


class User(Model):
    def __init__(self, id=None):
        Model.__init__(self, id)
        self.name = ''
        self.age = 0
        self.getModel()


    def columns(self):
        return [
            {'name': 'name', 'type': 'TEXT'},
            {'name': 'age', 'type': 'INTEGER'}
        ]


    def tablename(self):
        return 'users'


    def __str__(self):
        return '%s (%s)' % (self.name, self.age)


def main():
    Database.DB_FILE = 'test.db'
    # raw_input('[ENTER] search..')
    # user = User(2)
    # if(user.id):
    #     print user.name, user.age
    # else:
    #     print 'user not found'
    #
    # raw_input('[ENTER] create table..')
    # user.createTable()
    #
    # raw_input('[ENTER] insert new user..')
    # user = User()
    # user.name = 'Rene'
    # user.age = 22
    # user.save()
    # if(user.id):
    #     print user.name, user.age
    # else:
    #     print 'user not found'
    #
    # raw_input('[ENTER] update user..')
    # user.name = 'rene'
    # user.age = 26
    # user.save()
    # if(user.id):
    #     print user.name, user.age
    # else:
    #     print 'user not found'

    # raw_input('[ENTER] delete..')
    # print 'delete..'
    # print user.delete()

    # for u in User().select():
    #     print u
    #
    user = User().selectOne(SQL().WHERE('name', '=', 'rene'))
    user.name = 'RENE'
    user.save()

    with Database() as db:
        for u in db.select(User(), SQL().WHERE('name', '=', 'RENE')):
            print(u)


if(__name__ == '__main__'):
    main()
