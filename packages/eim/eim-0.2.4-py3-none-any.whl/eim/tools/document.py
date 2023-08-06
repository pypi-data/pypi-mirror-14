# __author__ = 'Brennon Bortz'
#
# import pickle
# import os
# import uuid
# import pandas
#
# # FIXME: Check for any exceptions that might be thrown and document them
#
# def as_pandas_df(documents, sep='.'):
#     """
#     Convert a list of documents to a :py:class:`pandas.DataFrame`. This method flattens any and all nested keys in
#     the document.
#
#     Parameters
#     ----------
#     documents : dict or list of dict
#         The document or list of documents to be converted
#     sep : str, optional
#         The separator to use when joining nested keys into a flattened key
#
#     Returns
#     -------
#     out : :py:class:`pandas.DataFrame`
#         A DataFrame containing the documents
#
#     Examples
#     --------
#     >>> nested_doc = {'foo': 'bar', 'baz': {'bam': [10,11,12]}}
#     >>> df = as_pandas_df(nested_doc)
#     >>> df.columns
#     Index(['baz.bam.0', 'baz.bam.1', 'baz.bam.2', 'foo'], dtype='object')
#
#     >>> df = as_pandas_df(nested_doc, sep='_')
#     >>> df.columns
#     Index(['baz_bam_0', 'baz_bam_1', 'baz_bam_2', 'foo'], dtype='object')
#
#     >>> second_doc = {'foo': 'pop', 'baz': {'bam': [20,21,22]}}
#     >>> df = as_pandas_df([nested_doc, second_doc])
#     >>> df.loc[0,'baz.bam.0']
#     10
#     >>> df.loc[1,'baz.bam.1']
#     21
#     """
#
#     if type(documents) != list:
#         documents = [documents]
#     flattened = flatten_documents(documents, sep)
#     df = pandas.DataFrame(flattened)
#     return df


def flatten_documents(documents, sep='.'):
    """
    'Flatten' a list of documents so that there are no nested keys.

    Nested keys become concatenated with their parent(s) using ``sep``. For instance, the dictionary
    ``{'foo': [{'bar':1},2,3]}`` is flattened to a dictionary with the keys ``foo.0.bar``, ``foo.1``, and ``foo.2``.
    This method works only for dictionaries that would qualify as JSON. In other words, only those dictionaries that
    contain atomic types, lists, and other dictionaries will work with this method.

    Parameters
    ----------
    documents : list of dict
        The document to be flattened
    sep : str, optional
        The string to use when joining nested keys into a flattened key (the default is `'.'`)

    Returns
    -------
    out : list of dict
        A list of flattened documents

    Examples
    --------
    >>> a_dict = {'foo': [{'bar':1},2,3]}
    >>> b_dict = {'bam': [{'baz':4}]}
    >>> flat_dicts = flatten_documents([a_dict, b_dict])
    >>> flat_dicts[0]['foo.0.bar']
    1
    >>> flat_dicts[0]['foo.1']
    2
    >>> flat_dicts[0]['foo.2']
    3
    >>> flat_dicts[1]['bam.0.baz']
    4
    """
    return [flatten_document(doc, sep=sep) for doc in documents]


def flatten_document(document, sep='.'):
    """
    'Flatten' a document so that there are no nested keys.

    Nested keys become concatenated with their parent(s) using ``sep``. For instance, the dictionary
    ``{'foo': [{'bar':1},2,3]}`` is flattened to a dictionary with the keys ``foo.0.bar``, ``foo.1``, and ``foo.2``.
    This method works only for dictionaries that would qualify as JSON. In other words, only those dictionaries that
    contain atomic types, lists, and other dictionaries will work with this method.

    Parameters
    ----------
    document : dict
        The document to be flattened
    sep : str, optional
        The string to use when joining nested keys into a flattened key (the default is `'.'`)

    Returns
    -------
    out : dict
        The flattened document

    Examples
    --------
    >>> a_dict = {'foo': [{'bar':1},2,3]}
    >>> flat_dict = flatten_document(a_dict)
    >>> flat_dict['foo.0.bar']
    1
    >>> flat_dict['foo.1']
    2
    >>> flat_dict['foo.2']
    3
    """
    doc_keys = sorted(all_keys(document, sep=sep))
    flattened = {}
    for key in doc_keys:
        flattened[key] = dict_value_for_keypath(document, key, sep=sep)
    return flattened


def all_keys(dictionary, sep='.', parent_key='', only_leaves=True):
    """
    Extract all keys of a dictionary and place them in a list.

    This method works only for dictionaries that would qualify as JSON. In other words, only those dictionaries that
    contain atomic types, lists, and other dictionaries will work with this method. Keys are joined together using the
    string specified in ``sep``. Only 'leaf' keys will be extracted when ``only_leaves`` is ``True`` (default). The
    entries of lists will be represented as single numbers in the 'keypath'. For instance, in ``{'foo': [1,2,3]}``, the
    extracted keys would be ``foo.0``, ``foo.1``, and ``foo.2``.

    Parameters
    ----------
    dictionary : dict
        The dictionary from which to extract keys
    sep : str, optional
        The string to use when joining nested keys into a flattened key (the default is `'.'`)
    parent_key : str, optional
        The prefix keypath (used in recursive calls; the default is `''`
    only_leaves : bool
        If `True`, only 'leaf' keys will be extracted.

    Returns
    -------
    out : list of str
        The list of extracted keys

    Examples
    --------
    >>> a_dict = {'foo': 'bar'}
    >>> dict_keys = all_keys(a_dict)
    >>> set(dict_keys) == set(['foo'])
    True

    >>> a_dict = {'foo': [1,2,3]}
    >>> dict_keys = all_keys(a_dict)
    >>> set(dict_keys) == set(['foo.0', 'foo.1', 'foo.2'])
    True

    >>> a_dict = {'foo': [{'bar':1},2,3]}
    >>> dict_keys = all_keys(a_dict)
    >>> set(dict_keys) == set(['foo.0.bar', 'foo.1', 'foo.2'])
    True

    >>> a_dict = {'foo': [{'bar':1},2,3]}
    >>> dict_keys = all_keys(a_dict, sep='_')
    >>> set(dict_keys) == set(['foo_0_bar', 'foo_1', 'foo_2'])
    True

    >>> a_dict = {'foo': [{'bar':1},2,3]}
    >>> dict_keys = all_keys(a_dict, only_leaves=False)
    >>> set(dict_keys) == set(['foo', 'foo.0', 'foo.1', 'foo.2', 'foo.0.bar'])
    True
    """

    import collections

    key_set = set()

    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key

        if isinstance(value, collections.MutableMapping):
            if not only_leaves:
                key_set.add(new_key)

            children = all_keys(value, sep=sep, parent_key=new_key, only_leaves=only_leaves)
            key_set = key_set.union(children)
        elif isinstance(value, list):
            if not only_leaves:
                key_set.add(new_key)

            for i in range(len(value)):
                list_index_key = new_key + sep + str(i)
                if not only_leaves:
                    key_set.add(list_index_key)

                # Recurse if the list entry is a dict
                if isinstance(value[i], dict):
                    children = all_keys(value[i], sep=sep, parent_key=list_index_key, only_leaves=only_leaves)
                    key_set = key_set.union(children)

                # Otherwise, just add a key with the index in dot notation
                else:
                    key_set.add(new_key + sep + str(i))
        else:
            key_set.add(new_key)

    return list(key_set)


def dict_value_for_keypath(dictionary, keypath, sep='.'):
    """
    Traverse the ``sep``-delimited 'keypath' in `dictionary` and return its value.

    This method works only for dictionaries that would qualify as JSON. In other words, only those dictionaries that
    contain atomic types, lists, and other dictionaries will work with this method. Keypaths are split by `sep`, and
    these individual keys are used to traverse the dictionary.

    Parameters
    ----------
    dictionary : dict
        The dictionary to traverse
    keypath : str
        The ``sep``-delimited compound keypath
    sep : str, optional
        The delimiter used in building the keypath (the default is `'.'`)

    Returns
    -------
    out : any
        The value for the keypath. This may be a ``dict`` or ``list`` of values.

    Examples
    --------
    >>> a_dict = {'foo': 'bar'}
    >>> val = dict_value_for_keypath(a_dict, 'foo')
    >>> val == 'bar'
    True

    >>> a_dict = {'foo': [1,2,3]}
    >>> val = dict_value_for_keypath(a_dict, 'foo.1')
    >>> val == 2
    True

    >>> a_dict = {'foo': [{'bar':1},2,3]}
    >>> val = dict_value_for_keypath(a_dict, 'foo.0.bar')
    >>> val == 1
    True
    >>> val = dict_value_for_keypath(a_dict, 'foo.1')
    >>> val == 2
    True
    >>> val = dict_value_for_keypath(a_dict, 'foo.0')
    >>> val == {'bar': 1}
    True
    >>> val = dict_value_for_keypath(a_dict, 'foo.3')
    Traceback (most recent call last):
        ...
    IndexError: list index out of range

    >>> a_dict = {'foo': [{'bar':[{'baz': 'cheese'}]}]}
    >>> val = dict_value_for_keypath(a_dict, 'foo.0.bar.0.baz')
    >>> val == 'cheese'
    True

    >>> a_dict = {'foo': [{'bar':[{'baz': 'cheese'}]}]}
    >>> val = dict_value_for_keypath(a_dict, 'foo_0_bar_0_baz', sep='_')
    >>> val == 'cheese'
    True
    """

    import collections

    if keypath == '':
        return dictionary

    key_list = keypath.split(sep=sep)

    value_for_key = None

    remaining_keypath = sep.join(key_list[1:])

    # pprint(dictionary)

    if isinstance(dictionary, collections.MutableMapping):
        value_for_key = dict_value_for_keypath(dictionary[key_list[0]], remaining_keypath, sep)
    elif isinstance(dictionary, list):
        value_for_key = dict_value_for_keypath(dictionary[int(key_list[0])], remaining_keypath, sep)

    return value_for_key


# def save_document_to_file(document, filepath, filename=''):
#     """
#     Serialize the document in ``document`` and save it to ``filepath``.
#
#     If ``filepath`` is not specified, a random filename is generated and the document is saved to this file in a *tmp*
#     subdirectory of the current working directory. The ``document`` must be serializable by Python's ``pickle`` module.
#     All documents retrieved from the Emotion in Motion database meet this requirement.
#
#     Parameters
#     ----------
#     document : dict
#         The document to be saved to a file
#     filepath : str
#         The path to the folder in which the file should be saved
#     filename : str
#         The name to give the file
#
#     Returns
#     -------
#     out : str
#         The absolute path of the saved file
#
#     Examples
#     --------
#     >>> simple_list = [1,2,3]
#     >>> save_document_to_file(simple_list, './tmp', filename='./test.pickle') # doctest: +ELLIPSIS
#     '...'
#     >>> read_simple_list = read_document_from_file('./tmp/test.pickle')
#     >>> os.unlink('./tmp/test.pickle')
#     >>> set(simple_list) == set(read_simple_list)
#     True
#     """
#
#     actual_filename = filename
#
#     # If no filepath was provided, use a random filename in tmp subdirectory of the current working directory
#     if actual_filename == '':
#
#         # Generate random filename
#         actual_filename = str(uuid.uuid4()) + '.pickle'
#
#     # Create filepath
#     actual_filepath = os.path.join(os.path.abspath(filepath), actual_filename)
#
#     # Create the directory part of the filepath if it does not yet exist
#     actual_filepath_prefix = os.path.dirname(actual_filepath)
#     if not os.path.exists(actual_filepath_prefix):
#         os.makedirs(actual_filepath_prefix)
#
#     # Open the output file
#     outfile = open(actual_filepath, 'wb')
#
#     # Pickle the document
#     pickle.dump(document, outfile, pickle.HIGHEST_PROTOCOL)
#
#     # Close the output file
#     outfile.close()
#
#     return actual_filepath


# def read_document_from_file(filepath):
#     """
#     Read a document that has been serialized to a file with :py:meth:`eim.tools.document.save_document_to_file`.
#
#     Parameters
#     ----------
#     filepath : str
#         The path to the serialized document file
#
#     Returns
#     -------
#     out : dict
#         The deserialized document
#
#     Examples
#     --------
#     >>> simple_list = [1,2,3]
#     >>> save_document_to_file(simple_list, './tmp', filename='./test.pickle') # doctest: +ELLIPSIS
#     '...'
#     >>> read_simple_list = read_document_from_file('./tmp/test.pickle')
#     >>> os.unlink('./tmp/test.pickle')
#     >>> set(simple_list) == set(read_simple_list)
#     True
#     """
#
#     # Read in the serialized file and deserialize it.
#     infile = open(filepath, mode='rb')
#     document = pickle.load(infile)
#
#     # Close the file and return the deserialized document.
#     infile.close()
#     return document
