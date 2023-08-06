# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import re
import logging


class Base(object):
    """Base for Schemas."""

    def __init__(self, path, **kwargs):
        self.path = path
        self.kwargs = kwargs

    def __getitem__(self, item):
        """Get attribute from class."""
        return getattr(self, item)

    @property
    def directories(self):
        return re.split(os.path.sep, os.path.split(self.path)[0])

    @property
    def filename(self):
        return os.path.split(self.path)[1]

    @property
    def basename(self):
        return os.path.splitext(self.filename)[0]

    @property
    def extension(self):
        return os.path.splitext(self.filename)[1]

    @property
    def edition(self):
        edition = self._search(r'(ed|Ed|ED|edition|Edition|EDITION)([a-zA-Z\d]+)', self.basename, 2)
        if edition:
            try:
                return int(edition)
            except:
                return edition

    @property
    def accuracy(self):
        total = 0
        exists = 0

        # Summarize Property tags
        exclude = ['json', 'accuracy', 'validation', 'extension', 'basename',
                   'filename', 'directory', 'path', 'errors', 'kwargs']
        for key in dir(self):
            if not key.startswith('_') and key not in exclude:
                total += 1
                if self[key]:
                    exists += 1
                else:
                    logging.error('Missing Tag [{}]'.format(key))

        # Summarize Validation Items
        for key, value in self.validation.items():
            total += 1
            if value:
                exists += 1
            else:
                logging.error('Validation[{}]'.format(key))

        return int(float(exists) / float(total) * 100)

    def _search(self, pattern, string, group=1):
        match = re.search(pattern, string)
        if match:
            return match.group(group)
