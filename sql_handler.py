import sqlite3
from random import randint

class SQLhandler:
    def __init__(self):
        self.connection = sqlite3.connect('db/Haiku.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
        create table Haiku
        (
        id integer PRIMARY KEY AUTOINCREMENT
        , title text not null
        , haiku_text text not null
        , image_path text not null unique    
        )
        ''')

    def get_haiku(self):
        self.max_id = int(self.cursor.execute('''
        select max(id) from Haiku
        ''').fetchall()[0][0])
        self.rand_id = randint(1, self.max_id)
        self.title, self.haiku_text, self.image_path = self.cursor.execute(f'''
        select title, haiku_text, image_path
        from Haiku
        where id = {self.rand_id}
        ''').fetchall()[0]
        # print('Всё хорошо get_haiku')
        self.connection.commit()
        self.connection.close()
        return self.title, self.haiku_text, self.image_path

    def dump_haiku(self, title, haiku_text, image_path):
        sql_insert = '''
            INSERT INTO Haiku (title, haiku_text, image_path)
            VALUES (?, ?, ?)
        '''
        self.cursor.execute(sql_insert, (title, haiku_text, image_path))
        # print('Всё хорошо dump_haiku')
        self.connection.commit()
        self.connection.close()

if __name__ == '__main__':
    sql = SQLhandler()
    sql.create_table()
    # sql.dump_haiku('dhsgfhsgdhf', 'hsjfhjhjjhjs', 'hkjdshfjhskdf')
    # print(sql.get_haiku())
