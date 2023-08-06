__author__ = 'Brennon Bortz'

# import pymongo
#
# def get_random_document(collection, filter=None):
#     """
#     Retrieves a random document from the specified collection that matches the filter dictionary. `get_random_document`
#     requires that the documents in the target collection have a `random` field, the value of which is a floating-point
#     number in the range [0,1).
#
#     Parameters
#     ----------
#     collection : :py:class:`pymongo.Collection`
#         The collection in the database from which to retrieve a random document
#     filter : dict
#         A filter to use as the search query
#
#     Returns
#     -------
#     out : dict or None
#         The randomly selected document
#
#     Examples
#     --------
#     >>> import eim
#     >>> db = eim.connect('eim', 'eim')
#     >>> doc = get_random_document(db.trials)
#     >>> 'metadata' in doc.keys()
#     True
#
#     >>> doc = get_random_document(db.bad_collection)
#     """
#
#     # If a filter wasn't passed, give it an empty dict
#     # and a random number
#     from random import random
#     actual_filter = filter or {}
#     actual_filter['random'] = {'$lte': random()}
#
#     # Get document
#     random_document = collection.find_one(filter=actual_filter, sort=[('random', pymongo.DESCENDING)])
#
#     # Make sure we retrieved a document
#     try:
#         assert isinstance(random_document, dict), 'A MongoDB document was not returned by pymongo.collection.find_one(). There may not be a "random" field on documents in this collection.'
#         return random_document
#     except:
#         return None
#
# def get_random_documents(collection, count, filter={}):
#     """
#     Parameters
#     ----------
#     collection : :py:class:`pymongo.Collection`
#         The collection in the database from which to retrieve a random document
#     count : int
#         The number of documents to retrieve
#     filter : dict
#         A filter to use as the search query
#
#     Returns
#     -------
#     out : list of dict
#         A list of randomly selected documents
#
#     Examples
#     --------
#     >>> import eim
#     >>> db = eim.connect('eim', 'eim')
#     >>> docs = get_random_documents(db.trials, 5)
#     >>> len(docs)
#     5
#
#     >>> docs = get_random_documents(db.bad_collection, 5)
#     >>> docs
#     []
#     """
#
#     # Empty list for docs
#     docs = []
#
#     # Repeatedly call get_random_document to get docs
#
#     for i in range(count):
#         random_document = get_random_document(collection, filter=filter)
#         if random_document:
#             docs.append(random_document)
#
#     return docs
