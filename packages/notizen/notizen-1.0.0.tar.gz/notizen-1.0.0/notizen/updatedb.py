#!/usr/bin/env python
# coding: utf-8

"""
FIXME
"""

import re
import os
import logging
from os import path
from notizen import indices


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# tags: and keywords: are the same.
RE_TAG = re.compile(r'^\s*tags:(.*)$', re.IGNORECASE)
RE_KEYWORDS = re.compile(r'^\s*keywords:(.*)$', re.IGNORECASE)

RE_TITLE = re.compile(r'^\s*title:(.*)$', re.IGNORECASE)
RE_SUMMARY = re.compile(r'^\s*summary:(.*)$', re.IGNORECASE)

# FIXME also *.rst
RE_FILE = re.compile(r'^.*\.md$', re.IGNORECASE)


def get_info_from_file(filepath: str) -> dict:
    '''Provides a dictionary with the info extracted from a file.
    Currently only the tags and the path to the file.'''
    # NOTE: if wrong parameters are found (e.g. several titles
    # for the same file), it won't complain, as it is useless.

    with open(filepath, 'r') as f:
        ten_first_lines = f.readlines()[:10]
    info = {'filepath': filepath}
    for line in ten_first_lines:
        # FIXME i repeat myself here:
        result = RE_TAG.match(line)
        if not result:
            result = RE_KEYWORDS.match(line)
        if result:
            tags_str = result.groups()[0]
            tags_l = tags_str.split(',')
            tags_l = [t.strip() for t in tags_l]
            tags_l += info.get('tags', [])
            # Collect all tags
            info.update({'tags': tags_l})
            continue
        result = RE_TITLE.match(line)
        if result:
            title_str = result.groups()[0]
            title_str = title_str.strip()
            # Take the last title found
            info.update({'title': title_str})
        result = RE_SUMMARY.match(line)
        if result:
            summary_str = result.groups()[0]
            summary_str = summary_str.strip()
            # Take the last summary found
            info.update({'summary': summary_str})
    return info


def update_tags_index(tags_index: dict, notes_path: str) -> None:
    '''Walks all the directory path, extracts info for each
    Markdown file and updates the Tags Index provided.'''
    # FIXME if notes_path does not exist, no error is raised.

    for (root, dirs, files) in os.walk(notes_path):
        # FIXME skip .git .ipynb_checkpoints dirs.
        for filepath in files:
            filepath = path.join(root, filepath)
            if not RE_FILE.match(filepath):
                continue
            # FIXME what if no tags?
            fileinfo = get_info_from_file(filepath)
            indices.add_file_to_tag_index(tags_index, fileinfo)
