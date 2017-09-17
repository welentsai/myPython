# -*- coding: utf-8 -*-

import hashlib
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

# 通常一個應用程式也只會用到一個 declarative_base() 類別
Base = declarative_base()

# __repr__ should return a printable representation of the object
# __repr__ is more for developers 
# __str__ is for end users

# Python類別 User 對應 DB中的 users 表格
# User Class 可稱為 Mapped class
class User(Base):
    __tablename__ = 'users' # 映對到資料庫中的 users 資料表

    id = Column(Integer, primary_key=True) # SQLite has an implicit “auto increment” feature
    name = Column(String)
    username = Column(String)
    password = Column(String)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = hashlib.sha1(password).hexdigest()

    def __repr__(self):
        return "User('{}','{}', '{}')".format(
            self.name,
            self.username,
            self.password
        )



# Before Python interpreter executing the code, it will define a few special variables.
# if the python interpreter is running that module (the source file) as the main program, 
# it sets the special __name__ variable to have a value "__main__"

'''
One of the reasons for doing this is that sometimes you write a module (a .py file) where it can be executed directly. 
Alternatively, it can also be imported and used in another module. 
By doing the main check, you can have that code only execute when you want to run the module as a program 
and not have it execute when someone just wants to import your module and call your functions themselves.
'''

if __name__ == '__main__':  # 當此檔案被Python interpreter直接執行時, 以下code才會被run
    ''' 此時只有建立 SQLAlchemy Engine 實例，還沒在記憶體內建立資料，
        只有第一個 SQL 指令被下達時，才會真正連接到資料庫內執行 '''
    engine = create_engine('sqlite:///:memory:')  # echo=True, show logging

    # engine = create_engine('sqlite:///example.txt', echo=True)  # echo=True, show logging

    pgEngine = create_engine(
        "postgresql+pg8000://welen:867080@localhost:5566/test",
        client_encoding='utf8'
    )


    #Base.metadata.drop_all(engine)   # all tables are deleted
    ''' 真正建立表格是使用 Base.metadata.create_all(engine) '''
    Base.metadata.create_all(pgEngine)

    # User.__table__.drop(engine) # delete User Tabl

    Session = sessionmaker(bind=pgEngine) # 將engine綁定(bind)到 Session 類別, 以開始進行與資料庫的互動
    session = Session() # create a Session

    user_1 = User('user1', 'username1', 'password_1'.encode('utf-8'))
    session.add(user_1) # pending status 

    print('Mapper:', user_1.__mapper__) # <Python 類別> 與 <映對的資料表名稱> 

    # 什麼時候資料才會被新增到資料庫內呢？
    # 只有進行 QUERY, COMMIT, FLUSH 時才會被寫入資料庫內
    # 查詢的基本使用法為 session.query(Mapped Class)
    # 所以query()時, SQLAlchemy 會先將 user_1 的資料寫入資料庫中
    # 若無資料回傳 None
    # first() 則是回傳查詢結果的第1筆
    row = session.query(User).filter_by(name='user1').first() # 注意, 是User 類別, 不是instances
    if row:
    	print('Found user1')
    	print(row)
    else:
    	print('Can not find user1')

    '''
    session.rollback() # 資料庫回到新增 user1 之前的狀態

    row = session.query(User).filter_by(name='user1').first()

    if row:
        print('Found user1 after rollback')
        print(row)
    else:
        print('Can not find user1 after rollback')
    '''

    user_2 = User('user2', 'username2', 'password_2'.encode('utf-8'))
    session.add(user_2)
    session.commit() # 寫入資料庫

    # query() 可以使用 from_statement() 方法, 以完整的 SQL 指令進行查詢
    # 搭配 params() 將變數代入 SQL 指令中
    # :name 代表會有一個參數名 name
    rows = session.query(User).from_statement('SELECT * FROM users WHERE name=:name').params(name='user1')

    for r in rows:
    	print(r.id, end=", ")
    	print(r.name)

    # SELECT users.name FROM users
    for r in session.query(User):
        print(r.id, end=', ')
        print(r.username)

    print()
    # SELECT users.id, users.username FROM users
    print('SELECT users.username FROM users')
    for r in session.query(User.id, User.username):
        print(r.id, end=', ')
        print(r.username)

    print()
    # SELECT * FROM users where id = 1
    for r in session.query(User).filter_by(id=1):
    	print(r.id)
    	print(r.name)


    # print(auser) # auser.__repr__ ()  is called 
    print('Mapper:', user_1.__mapper__)