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

"""Test InvenioCelery extension."""

from __future__ import absolute_import, print_function

from mock import MagicMock, patch
from pkg_resources import EntryPoint

from invenio_celery import InvenioCelery


def _mock_entry_points(group, name=None):
    """Return EntryPoints from different groups."""
    data = {
        'only_first_tasks': [EntryPoint('first_tasks', 'first_tasks')],
        'only_second_tasks': [EntryPoint('second_tasks', 'second_tasks')],
        'invenio_celery.tasks': [
            EntryPoint('first_tasks', 'first_tasks'),
            EntryPoint('second_tasks', 'second_tasks'),
        ],
    }
    assert name is None
    for entry_point in data[group]:
        yield entry_point


def test_version():
    """Test version import."""
    from invenio_celery import __version__
    assert __version__


def test_init(app):
    """Test Celery initialization."""
    celery = InvenioCelery(app)
    assert app.extensions['invenio-celery'] == celery

    called = {}

    @celery.celery.task
    def test1():
        called['test1'] = True

    test1.delay()
    assert called['test1']


@patch("pkg_resources.iter_entry_points", _mock_entry_points)
def test_enabled_autodiscovery(app):
    """Test shared task detection."""
    ext = InvenioCelery(app)
    ext.load_entry_points()
    assert 'conftest.shared_compute' in ext.celery.tasks.keys()
    assert 'first_tasks.first_task' in ext.celery.tasks.keys()
    assert 'second_tasks.second_task_a' in ext.celery.tasks.keys()
    assert 'second_tasks.second_task_b' in ext.celery.tasks.keys()


@patch("pkg_resources.iter_entry_points", _mock_entry_points)
def test_only_first_tasks(app):
    """Test loading different entrypoint group."""
    ext = InvenioCelery(app, entry_point_group='only_first_tasks')
    ext.load_entry_points()
    assert 'conftest.shared_compute' in ext.celery.tasks.keys()
    assert 'first_tasks.first_task' in ext.celery.tasks.keys()
    assert 'second_tasks.second_task_a' not in ext.celery.tasks.keys()
    assert 'second_tasks.second_task_b' not in ext.celery.tasks.keys()


def test_disabled_autodiscovery(app):
    """Test disabled discovery."""
    ext = InvenioCelery(app, entry_point_group=None)
    ext.load_entry_points()
    assert 'conftest.shared_compute' in ext.celery.tasks.keys()
    assert 'first_tasks.first_task' not in ext.celery.tasks.keys()
    assert 'second_tasks.second_task_a' not in ext.celery.tasks.keys()
    assert 'second_tasks.second_task_b' not in ext.celery.tasks.keys()


@patch("pkg_resources.iter_entry_points", _mock_entry_points)
def test_worker_loading(app):
    """Test that tasks are only loaded on the worker."""
    ext = InvenioCelery(app)
    assert 'first_tasks.first_task' not in ext.celery.tasks.keys()
    ext.celery.loader.import_default_modules()
    assert 'first_tasks.first_task' in ext.celery.tasks.keys()


def test_get_queues(app):
    """Test get queues."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    assert ext.get_queues() == []


def test_enable_queue(app):
    """Test enable queues."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    ext.enable_queue('feed')


def test_disable_queue(app):
    """Test enable queues."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    ext.disable_queue('feed')


def test_get_active_tasks(app):
    """Test get active tasks."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    assert ext.get_active_tasks() == []


def test_suspend_queues(app):
    """Test suspend queues."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    c = {'i': 0}

    def _mock():
        c['i'] += 1
        return [] if c['i'] > 1 else ['test']

    ext.get_active_tasks = _mock
    ext.suspend_queues(['feed'], sleep_time=0.1)
