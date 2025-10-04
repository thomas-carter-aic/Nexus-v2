from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from pymongo import MongoClient

class UserRepository(ABC):
@abstractmethod
def save(self, user):
pass

@abstractmethod
def find_by_id(self, user_id):
pass

class PostgresUserRepository(UserRepository):
def init(self, connection_string):
self.engine = create_engine(connection_string)

def save(self, user):
with self.engine.connect() as conn:
conn.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user['id'], user['name']))

def find_by_id(self, user_id):
with self.engine.connect() as conn:
result = conn.execute("SELECT * FROM users WHERE id = %s", (user_id,)).fetchone()
return dict(result) if result else None

class MongoUserRepository(UserRepository):
def init(self, connection_string):
self.client = MongoClient(connection_string)
self.db = self.client['users_db']

def save(self, user):
self.db.users.insert_one(user)

def find_by_id(self, user_id):
return self.db.users.find_one({'id': user_id})
