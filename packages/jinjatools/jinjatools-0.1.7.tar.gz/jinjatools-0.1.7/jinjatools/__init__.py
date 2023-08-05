# python-jinjatools
#
# Various tools for Jinja2,
# including new filters and tests based on python-moretools,
# a JinjaLoader class for Django,
# and a simple JinjaBuilder class for SCons.
#
# Copyright (C) 2011-2015 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# python-jinjatools is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-jinjatools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-jinjatools.  If not, see <http://www.gnu.org/licenses/>.

__import__('zetup').toplevel(__name__, [
    'Environment',
])

from .env import Environment
# from .filters import filters
