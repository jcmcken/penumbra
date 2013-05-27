import os
import logging
_basedir = os.path.abspath(os.path.dirname(__file__))
_rootdir = os.path.join(_basedir, '..')

# General options
ENV = os.environ.get('FLASKENV')
LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"

if ENV == 'production':
    DEBUG = False
    LOG_LEVEL = logging.INFO
    LOG_DIR = os.path.join('/var/log')
    SQLALCHEMY_DATABASE_URI = "mysql://penumbra:penumbra@localhost:3306/penumbra"
else:
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    LOG_DIR = os.path.join(_rootdir, 'tmp')
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/tmp/db.sqlite" % _rootdir
    SQLALCHEMY_ECHO = True
    ADMINISTRATIVE_GROUPS = ['administrators']
    ADMINISTRATIVE_USERS = ['admin']
    
LOG_FILE = os.path.join(LOG_DIR, 'penumbra.log')

# Security
SECRET_KEY = 'FWOhM6A5GYlGmV5khDV7TRDQ1XEso5pOMJBxptbgjtLzFQbal5SNHLOf2tXB7bkCwmHvEKWgnzDw/CvRPO8kVxJUfDhv+CGkbKkytocBi3kPR/GqVylFvYjEuGuhym/D3wTJm+T30EWB/C369lQWnoPcricZA4fi8bdFFMR+QOQO5x2BL6qZbmdANP5HzKVWn1Om95DeV/fA9izocwyKK15Cx49Lf03h/zOrKyV1yAh5vIZXz4Y9F6739yvFUBDO949YzRERR9TY/bF2kDYS8lujVaZ2Kpu3x9JxgWSSCGdO+SmTWEsg0w5H9lFepQAGRiwJaKnAKXUYHg=='
CSRF_ENABLED = True
CSRF_SESSION_KEY = 'FAX18ySe9SA2lv9IZN4dVl54d2fbK+wEjTCT0aSW8IGGQNbD7e7wSUAnGjvaRnmbj4PplqUKVDZKUaJwDBz49s+hNFQsMZDxJb2y9lRvRmN3GWs8yK7yKs/mj5A82o6ujv+hpyNNDM1YF2S2f4znhf5jg4pMwb1wP9xEqHGLguyJyva+3f6eFcg67SBpv8obBbv6cQa3irW8FR1GyooKU6PzNKzILReOVvtmXM655YNIxZTvjwm51Bx7L8Z/kdEpB5ejxBV/O5UCXrirn+G8rslUsE9uSo8ppzgtP8OIs1+Dh/T3Ow9DLfEOL/DooPUP/SJkQMlhf692GA=='

