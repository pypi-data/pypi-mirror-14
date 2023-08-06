#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @date: Thu May 24 10:41:42 CEST 2012
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
from nose.plugins.skip import SkipTest

import bob.bio.base

def _check_database(database, groups = ('dev',), protocol = None, training_depends = False, models_depend = False):
  assert isinstance(database, bob.bio.base.database.DatabaseBob)

  if protocol: database.protocol = protocol
  assert len(database.all_files()) > 0
  assert len(database.training_files('train_extractor')) > 0
  assert len(database.arrange_by_client(database.training_files('train_enroller'))) > 0

  for group in groups:
    model_ids = database.model_ids(group)
    assert len(model_ids) > 0
    assert database.client_id_from_model_id(model_ids[0]) is not None
    assert len(database.enroll_files(model_ids[0], group)) > 0
    assert len(database.probe_files(model_ids[0], group)) > 0

  assert database.training_depends_on_protocol == training_depends
  assert database.models_depend_on_protocol == models_depend


def _check_database_zt(database, groups = ('dev', 'eval'), protocol = None, training_depends = False, models_depend = False):
  _check_database(database, groups, protocol, training_depends, models_depend)
  assert isinstance(database, bob.bio.base.database.DatabaseBobZT)
  for group in groups:
    t_model_ids = database.t_model_ids(group)
    assert len(t_model_ids) > 0
    assert database.client_id_from_model_id(t_model_ids[0]) is not None
    assert len(database.t_enroll_files(t_model_ids[0], group)) > 0
    assert len(database.z_probe_files(group)) > 0


def test_mobio():
  database = bob.bio.base.load_resource('mobio-video', 'database', preferred_package='bob.bio.video')
  try:
    _check_database_zt(database, models_depend=True)
    _check_database_zt(database, protocol = 'female', models_depend=True)
  except IOError as e:
    raise SkipTest("The database could not be queried; probably the db.sql3 file is missing. Here is the import error: '%s'" % e)

def test_youtube():
  database = bob.bio.base.load_resource('youtube', 'database', preferred_package='bob.bio.video')
  try:
    _check_database(database, training_depends=True, models_depend=True)
    _check_database(database, protocol = 'fold7', training_depends=True, models_depend=True)
  except IOError as e:
    raise SkipTest("The database could not be queried; probably the db.sql3 file is missing. Here is the import error: '%s'" % e)
