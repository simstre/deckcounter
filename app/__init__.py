from flask import Flask
import redis

app = Flask('app')
app.config.from_object('base_config')
redis = redis.StrictRedis(
	host=app.config['REDIS_HOST'], 
	port=app.config['REDIS_PORT'], 
	db=app.config['REDIS_DB'],
	password=app.config['REDIS_PASSWORD'])
from app import views
