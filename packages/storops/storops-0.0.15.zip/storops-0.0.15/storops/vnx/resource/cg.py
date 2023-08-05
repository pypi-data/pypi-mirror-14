# coding=utf-8
# Copyright (c) 2015 EMC Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import unicode_literals

import storops.vnx.resource.lun
from storops.vnx.enums import raise_if_err
from storops.vnx.resource.resource import VNXCliResource, VNXCliResourceList
from storops import exception as ex

__author__ = 'Cedric Zhuang'


class VNXConsistencyGroupList(VNXCliResourceList):
    @classmethod
    def get_resource_class(cls):
        return VNXConsistencyGroup

    def _get_raw_resource(self):
        return self._cli.get_cg(poll=self.poll)

    def remove_member(self, *lun_list):
        for cg in self:
            cg.remove_member(*lun_list)


class VNXConsistencyGroup(VNXCliResource):
    def __init__(self, name=None, cli=None):
        super(VNXConsistencyGroup, self).__init__()
        self._cli = cli
        self._name = name

    def _get_raw_resource(self):
        return self._cli.get_cg(name=self._name, poll=self.poll)

    @classmethod
    def get(cls, cli, name=None):
        if name is None:
            ret = VNXConsistencyGroupList(cli)
        else:
            ret = VNXConsistencyGroup(name, cli)
        return ret

    @classmethod
    def create(cls, cli, name, members=None, auto_delete=None):
        out = cli.create_cg(name, members, auto_delete)
        raise_if_err(out, ex.VNXCreateConsistencyGroupError,
                     'error creating cg {}.'.format(name))
        return VNXConsistencyGroup(name=name, cli=cli)

    def remove(self):
        name = self._get_name()
        out = self._cli.remove_cg(name, poll=self.poll)
        raise_if_err(out, ex.VNXConsistencyGroupError,
                     'error remove cg "{}".'.format(name))

    def _cg_member_op(self, op, lun_list):
        clz = storops.vnx.resource.lun.VNXLun
        id_list = clz.get_id_list(*lun_list)
        name = self._get_name()
        out = op(name, *id_list, poll=self.poll)
        raise_if_err(out, ex.VNXConsistencyGroupError,
                     'error change member of "{}".'.format(name))

    def add_member(self, *lun_list):
        self._cg_member_op(self._cli.add_cg_member, lun_list)

    def remove_member(self, *lun_list):
        lun_list = list(filter(self.has_member, lun_list))
        self._cg_member_op(self._cli.remove_cg_member, lun_list)

    def replace_member(self, *lun_list):
        self._cg_member_op(self._cli.replace_cg_member, lun_list)

    def has_member(self, lun):
        clz = storops.vnx.resource.lun.VNXLun
        lun_id = clz.get_id(lun)
        return lun_id in self.lun_list
