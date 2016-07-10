from peewee import *

database = MySQLDatabase('csdn', **{'host': 'localhost', 'password': 'txwyy123', 'port': 3306, 'user': 'root'})

class BaseModel(Model):
    class Meta:
        database = database

class Article(BaseModel):

    id = IntegerField(primary_key=True, unique=True)
    title = CharField()
    url = CharField()
    read_count = IntegerField()
    comment_count = IntegerField()
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        db_table = 't_article'