# coding: utf-8


import os
import re
import logging
from os import path
from notizen import file_processing


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# FIXME also *.rst
RE_FILE = re.compile(r'^.*\.md$', re.IGNORECASE)


def show_matching_files(matching_files: list, tag: str) -> None:
    '''Print the list of matching files. Or a notification if there were no results.'''
    if matching_files is None:
        msg = 'No matching files with "{}" tag.\n\nMisspelled? or inexistent?'
        msg = msg.format(tag)
        print(msg)
        return  # FIXME return error to shell
        # obj.exit(1)?
    msg = '{} matching files under tag "{}":'
    print(msg.format(len(matching_files), tag))
    for f in matching_files:
        print('\t{}'.format(f))


def walk_and_index(notes_path: str, index_fn: "function") -> None:
    '''Walks all the directory path, extracts info for each
    Markdown file and triggers the .index() of the engine.'''
    # FIXME if notes_path does not exist, no error is raised.

    for (root, dirs, files) in os.walk(notes_path):
        for filepath in files:
            filepath = path.join(root, filepath)
            # FIXME skip .git .ipynb_checkpoints dirs.
            if not RE_FILE.match(filepath):
                continue
            # FIXME what if no tags?
            fileinfo = file_processing.get_info_from_file(filepath)
            index_fn(fileinfo)
            