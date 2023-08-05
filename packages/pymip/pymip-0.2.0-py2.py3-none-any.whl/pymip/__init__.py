# -*- coding: utf-8 -*-
"""
pymip
~~~~~~~~~~~~~~~~~~~

Provides a Python API to manipulate MIP

:copyright: (c) 2015 by Robin Andeer
:licence: MIT, see LICENCE for more details
"""
import logging
from pkg_resources import get_distribution

# Generate your own AsciiArt at:
# patorjk.com/software/taag/#f=Calvin%20S&t=PyMIP
__banner__ = r"""
╔═╗┬ ┬╔╦╗╦╔═╗
╠═╝└┬┘║║║║╠═╝
╩   ┴ ╩ ╩╩╩    by Robin Andeer
"""

__title__ = 'pymip'
__summary__ = 'Provides a Python API to manipulate MIP'
__uri__ = 'https://github.com/robinandeer/pymip'

__version__ = get_distribution(__title__).version

__author__ = 'Robin Andeer'
__email__ = 'robin.andeer@gmail.com'

__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Robin Andeer'

# the user should dictate what happens when a logging event occurs
logging.getLogger(__name__).addHandler(logging.NullHandler())
