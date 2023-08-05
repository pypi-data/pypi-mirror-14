"""
    holocron_clear_theme
    --------------------

    Holocron Clear Theme is a clear and simple theme for Holocron powered
    blogs.

    :copyright: (c) 2016 by Igor Kalnitsky
    :license: MIT, see LICENSE for details
"""

import pkg_resources

from holocron.ext import abc


class ClearTheme(abc.Extension):

    path = pkg_resources.resource_filename('holocron_clear_theme', 'theme')

    def __init__(self, app):
        app.add_theme(self.path)
