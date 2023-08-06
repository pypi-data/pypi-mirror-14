__author__ = 'Brennon Bortz'
__version__ = '0.2.3'

# import pymongo
import mongoengine


import eim.documents
import eim.tools

# import eim.tools.database

# def connect(username, password):
#     """
#     Connects to the Emotion in Motion database and authenticates against the ``eim`` collection with the provided
#     username and password.
#
#     Parameters
#     ----------
#     username : str
#         The username to use for authentication
#     password : str
#         The password to use for authentication
#
#     Returns
#     -------
#     out : :py:class:`pymongo.Database`
#         A handle for the Emotion in Motion database
#
#     Examples
#     --------
#     >>> db = connect('eim', 'eim')
#     >>> db.last_status()['ok']
#     1.0
#     """
#
#     # Create client, connect to database, and authenticate
#     client = pymongo.MongoClient('db0.musicsensorsemotion.com')
#     db = client.eim
#     db.authenticate(username, password)
#
#     return db

def connect(username, password):
    """
    Connect to the Emotion in Motion database and authenticate against the ``eim`` collection with the provided
    username and password.

    You *must* connect to the database before performing database operations.

    Parameters
    ----------
    username : str
        The username to use for authentication
    password : str
        The password to use for authentication
    """
    mongoengine.connect(
        host='mongodb://%s:%s@db0.musicsensorsemotion.com,db1.musicsensorsemotion.com,db2.musicsensorsemotion.com,db3.musicsensorsemotion.com/eim' % (username, password),
        replicaSet='rs-eim'
    )

