from __future__ import absolute_import

import os
import errno


def get_exception_detail(e):
    if not isinstance(e, Exception):
        return u''
    return u'%s: %s' % (e.__class__.__name__, e.message)


def ensure_dir(dirname):
    """Ensure the directory exists.

    No error if existing, make parent directories as needed.
    """
    try:
        os.makedirs(dirname)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise e
