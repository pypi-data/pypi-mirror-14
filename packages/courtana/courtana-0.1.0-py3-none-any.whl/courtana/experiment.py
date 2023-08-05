#!/venv/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import json
import shutil
import warnings
import numpy as np
import pandas as pd

# from courtana.tracker.trackdata import TrackData

CODENAME = 'apt'  # ApterousGal4

HDFSTORE_RAW = 'raw.h5'
HDFSTORE_TRACKER = 'tracker.h5'

PATH_VIDEOS = '../videos'
PATH_TRACKER_OUTPUT = '../opencsp_output'

FILENAME_PATTERN = re.compile(
    r"^(?P<date>\d{8})"                 # date
    r"(?:_(?P<female>[a-z0-9]+[^_]))?"  # female info
    r"(?:_(?P<male>[a-z0-9]+[^_]))?"    # male info
    r"(?:_(?P<info>[a-z0-9]+[^_]))?"    # additional info
    r"(?:_(?P<id>\d+))?"                # video ID
    r"(?:_(?P<extra>[a-z0-9]+[^_]))?"   # extra info
    r"(?:\.(?P<ext>\w+))$"              # file extension
)


class Experiment(object):

    FILENAME_PATTERN = re.compile(
        r"^(?P<date>\d{8})"                 # date
        r"(?:_(?P<female>[a-z0-9]+[^_]))?"  # female info
        r"(?:_(?P<male>[a-z0-9]+[^_]))?"    # male info
        r"(?:_(?P<info>[a-z0-9]+[^_]))?"    # additional info
        r"(?:_(?P<id>\d+))?"                # video ID
        r"(?:_(?P<extra>[a-z0-9]+[^_]))?"   # extra info
        r"(?:\.(?P<ext>\w+))$"              # file extension
    )

    # PATH_VIDEOS = ''
    # PATH_TRACKDATA = ''

    def __init__(self, codename, blind=False):
        self.codename = str(codename)
        self.exp_suffix = '_blind.csv' if blind is True else '_exp.csv'
        csvfile = self.codename + self.exp_suffix
        print("Loading experiment '{}' ({})".format(self.codename, csvfile))
        try:
            csvfile = self.codename + self.exp_suffix
            self.table = pd.read_csv(csvfile, index_col=0)
        except OSError:
            warnings.warn("Could not read experiment file")
            print("Creating from scratch...")
            self.table = pd.DataFrame(columns=['path_video'])

    def save(self):
        csvfile = self.codename + self.exp_suffix
        print("Saving experiment:", csvfile)
        self.table.to_csv(csvfile)

    def add_video(self, filepath):
        """Adds a video to the experiment. Provide the file path."""
        filename = os.path.basename(filepath)
        # Is the file already in the table?
        if filepath not in self.table.path_video.values:
            # Add a new entry
            match = re.fullmatch(self.FILENAME_PATTERN, filename)
            if match:
                matches = match.groupdict()
                del matches['ext']
                self.table = self.table.append(matches, ignore_index=True)
                current_index = len(self.table)-1
                self.table.loc[current_index, 'path_video'] = filepath
            else:
                warnings.warn("Match failed!")
        else:
            print("Already exists:", filepath)

    def add_files(self, path, col_name, match_cols, ext='.csv', pattern=None):
        """Add files to the table.
        Walks down the path given in search for all files with extension
        ext. Adds them under the column named col_name and assigns its
        row using the pattern and the match_cols arguments.
        """
        if pattern is None:
            pattern = self.FILENAME_PATTERN
        # Does the col_name specified exists?
        if col_name not in self.table.columns:
            self.table[col_name] = ''
        print("Looking for tracker results in", path)
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(ext):
                    filepath = os.path.abspath(os.path.join(root, f))
                    filename = os.path.basename(filepath)

                    # Is the file already in the table?
                    if filepath not in self.table.loc[:, col_name].values:
                        # Add a new entry
                        print("Adding", filename)
                        match = re.fullmatch(pattern, filename)
                        if match:
                            matches = match.groupdict()
                            query_str = gen_query_string(matches, match_cols)
                            index = get_index_from_query(self.table, query_str)
                            self.table.loc[index, col_name] = filepath
                        else:
                            raise Warning("Match failed!")
                    else:
                        print("Already exists:", filepath)

    def generate_blind(self, path):
        """Generate blind.
        Copies all video files in `table` to the given `path` and
        renames them into the format `<codename>_<index>.avi`.
        """
        print("Blinding the data...")
        self.blind = pd.DataFrame(columns=['path_video',
                                           'courtship',
                                           'copulation',
                                           'comment'])
        blind_key = {}
        print("Creating the blind folder:", path)
        for idx, filepath in self.table.path_video.iteritems():
            ext = os.path.splitext(filepath)[1]
            blindfilename = '{}_{}'.format(self.codename, idx) + ext
            blindfilepath = os.path.join(path, blindfilename)
            blind_key[str(idx)] = filepath
            print("Copying:", filepath, "->", blindfilepath)
            shutil.copy(filepath, blindfilepath)
            self.blind.loc[idx, 'path_video'] = blindfilepath
        self.blind.index.name = 'id'

        with open(self.codename + '_blindkey.json', 'w') as f:
            json.dump(blind_key, f, indent=4)

        csvfile = self.codename + '_blind.csv'
        print("Saving experiment:", csvfile)
        self.blind.to_csv(csvfile)


def gen_query_string(d, keys):
    """Returns a query string.
    d = {'a': 'hello', 'b': 'yes'}
    keys = ['a']
    Returns: "a == 'hello'"
    """
    last_key = keys[-1]
    query_str = ""
    for key in keys:
        query_str += "{0} == '{1}'".format(key, d[key])
        if key != last_key:
            query_str += " and "
    return query_str


def get_index_from_query(df, query_str):
    """
    df: DataFrame
    s: query string
    returns int: index
    """
    # query fall back to the index name if no column exists but in case
    # we need to cast the index value to str, we reset it here anyway
    index_name = df.index.name
    index_dtype = df.index.dtype
    df = df.reset_index()
    df[index_name] = df[index_name].astype(str)
    df = df.query(query_str)
    df[index_name] = df[index_name].astype(index_dtype)
    df.set_index(index_name, inplace=True)
    if len(df) == 1:
        return df.index.values[0]
    else:
        raise Exception("Query was not enough to select only one row")
