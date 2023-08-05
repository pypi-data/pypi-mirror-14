#!/usr/bin/env python
# coding: utf-8

"""
FIXME
"""

import pickle
import logging


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def add_file_to_tag_index(tags_index: dict, fileinfo: dict) -> None:
    '''Adds entries into the Tags Index'''
    tags_l = fileinfo.get('tags', None)
    if not tags_l:  # File has no tags
        return
    filepath = fileinfo['filepath']
    for tag in tags_l:
        file_l = tags_index.get(tag, [])
        file_l = list(set(file_l + [filepath, ]))
        tags_index[tag] = file_l


def load_indices(where_from: str) -> tuple:
    '''Loads the indices from the file refered by :where_from
    and returns a tuple: (tags_index, ).
    Should not find the file, it will return empty indices.'''

    try:
        with open(where_from, 'br') as f:
            idx = pickle.load(file=f)
        tags_index = idx['tags_index']
    except FileNotFoundError:
        tags_index = {}
        LOGGER.info('File "{}" was not found.'.format(where_from))
    return (tags_index, )


def save_indices(tags_index: dict, where: str) -> None:
    '''Save the indices into the file refered by :where.'''

    idx = {
        'tags_index': tags_index,
    }
    with open(where, 'bw') as f:
        pickle.dump(obj=idx, file=f, protocol=-1)
