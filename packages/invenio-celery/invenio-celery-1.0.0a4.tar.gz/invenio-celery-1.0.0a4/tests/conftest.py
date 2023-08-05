# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import sys

from celery import shared_task, Celery
from flask import Flask
import pytest


@pytest.yield_fixture()
def app(request):
    """Flask app fixture."""
    app = Flask("testapp")
    app.config.update(dict(
        CELERY_ALWAYS_EAGER=True,
        CELERY_RESULT_BACKEND="cache",
        CELERY_CACHE_BACKEND="memory",
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True
    ))

    @shared_task
    def shared_compute():
        """Dummy function."""
        pass

    yield app

    import celery._state
    celery._state._apps.discard(
        app.extensions['invenio-celery'].celery._get_current_object()
    )
    celery._state._on_app_finalizers = set()
    celery._state.set_default_app(Celery())

    # Clear our modules to get them re-imported by Celery.
    if 'first_tasks' in sys.modules:
        del sys.modules['first_tasks']
    if 'second_tasks' in sys.modules:
        del sys.modules['second_tasks']
