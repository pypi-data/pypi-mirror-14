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

from unittest import TestCase

from hamcrest import assert_that, raises, equal_to, has_item, none

from test.vnx.cli_mock import patch_cli, t_cli
from test.vnx.resource.fakes import STORAGE_GROUP_HBA
from storops.vnx.enums import VNXSPEnum, VNXPortType
from storops.vnx.resource.port import VNXHbaPort, VNXSPPort, \
    VNXConnectionPort
from storops.vnx.resource.sg import VNXStorageGroupHBA

__author__ = 'Cedric Zhuang'


class VNXSPPortTest(TestCase):
    @patch_cli()
    def test_port_list(self):
        ports = VNXSPPort.get(t_cli())
        assert_that(len(ports), equal_to(32))

    @patch_cli()
    def test_port_get_sp(self):
        ports = VNXSPPort.get(t_cli(), VNXSPEnum.SP_B)
        assert_that(len(ports), equal_to(16))

    @patch_cli()
    def test_port_get_id(self):
        ports = VNXSPPort.get(t_cli(), port_id=5)
        assert_that(len(ports), equal_to(2))

    @patch_cli()
    def test_index_sequence(self):
        # this test will fail if the index is not used as splitter is wrong
        port = VNXSPPort.get(t_cli(), VNXSPEnum.SP_A, 15)
        assert_that(port.wwn, equal_to(
            '50:06:01:60:B6:E0:16:81:50:06:01:67:36:E4:16:81'))

    @patch_cli()
    def test_get_port(self):
        port = VNXSPPort.get(t_cli(), VNXSPEnum.SP_A, 0)
        assert_that(port.sp, equal_to(VNXSPEnum.SP_A))
        assert_that(port.port_id, equal_to(0))
        assert_that(port.wwn, equal_to(
            '50:06:01:60:B6:E0:16:81:50:06:01:60:36:E0:16:81'))
        assert_that(port.link_status, equal_to('Up'))
        assert_that(port.port_status, equal_to('Online'))
        assert_that(port.switch_present, equal_to(True))
        assert_that(port.speed_value, equal_to('8Gbps'))
        assert_that(port.registered_initiators, equal_to(3))
        assert_that(port.logged_in_initiators, equal_to(1))
        assert_that(port.not_logged_in_initiators, equal_to(2))


class VNXHbaPortTest(TestCase):
    def test_from_storage_group_hba(self):
        hba = VNXStorageGroupHBA.parse(STORAGE_GROUP_HBA)
        port = VNXHbaPort.from_storage_group_hba(hba)
        assert_that(port.sp, equal_to(VNXSPEnum.SP_A))
        assert_that(port.port_id, equal_to(3))
        assert_that(port.vport_id, equal_to(1))
        assert_that(port.type, equal_to(VNXPortType.ISCSI))
        assert_that(port.host_initiator_list,
                    has_item('iqn.1991-05.com.microsoft:abc.def.dev'))

    def test_hash(self):
        ports = {
            VNXHbaPort.create(VNXSPEnum.SP_A, 1),
            VNXHbaPort.create(VNXSPEnum.SP_B, 1),
            VNXHbaPort.create(VNXSPEnum.SP_A, 1)
        }
        self.assertEqual(2, len(ports))

    def test_set_sp(self):
        port = VNXHbaPort.create('A', 3)
        self.assertEqual(VNXSPEnum.SP_A, port.sp)

    def test_set_sp_error(self):
        port = VNXHbaPort.create('Z', 3)
        self.assertEqual(False, port.is_valid())
        self.assertIsNone(port.sp)

    def test_set_number_error(self):
        def f():
            port = VNXHbaPort.create('A', 'a1')
            self.assertEqual(False, port.is_valid())
            self.assertIsNone(port.port_id)

        assert_that(f, raises(ValueError, 'must be an integer.'))

    def test_create_tuple_input(self):
        inputs = ('a', 5)
        port = VNXHbaPort.create(*inputs)
        self.assertEqual(VNXSPEnum.SP_A, port.sp)
        self.assertEqual(5, port.port_id)

    def test_get_sp_index(self):
        port = VNXHbaPort.create('spb', '5')
        self.assertEqual('b', port.get_sp_index())
        self.assertEqual(5, port.port_id)

    def test_equal(self):
        spa_1 = VNXHbaPort.create(VNXSPEnum.SP_A, 1)
        spa_1_dup = VNXHbaPort.create(VNXSPEnum.SP_A, 1)
        spa_2 = VNXHbaPort.create(VNXSPEnum.SP_A, 2)
        self.assertEqual(spa_1, spa_1_dup)
        self.assertEqual(False, spa_1 == spa_2)

    def test_as_tuple(self):
        port = VNXHbaPort.create(VNXSPEnum.SP_A, 1)
        self.assertEqual(('SP A', 1), port.as_tuple())

    def test_repr(self):
        port = VNXHbaPort.create(VNXSPEnum.SP_B, 3)
        self.assertEqual(port.__repr__(),
                         '<VNXPort {sp: SP B, port_id: 3, '
                         'vport_id: 0, host_initiator_list: ()}>')


class VNXConnectionPortTest(TestCase):
    def test_port(self):
        return VNXConnectionPort(sp='a', port_id=4, cli=t_cli())

    @patch_cli()
    def test_properties(self):
        port = self.test_port()
        assert_that(port.sp, equal_to(VNXSPEnum.SP_A))
        assert_that(port.port_id, equal_to(4))
        assert_that(port.wwn,
                    equal_to('iqn.1992-04.com.emc:cx.apm00153906536.a4'))
        assert_that(port.iscsi_alias, equal_to('6536.a4'))
        assert_that(port.enode_mac_address, equal_to('00-60-16-45-5D-FC'))
        assert_that(port.virtual_port_id, equal_to(0))
        assert_that(port.vlan_id, none())
        assert_that(port.current_mtu, equal_to(1500))
        assert_that(port.auto_negotiate, equal_to(False))
        assert_that(port.port_speed, equal_to('10000 Mb'))
        assert_that(port.host_window, equal_to('256K'))
        assert_that(port.replication_window, equal_to('256K'))
        assert_that(port.ip_address, equal_to('192.168.4.52'))
        assert_that(port.subnet_mask, equal_to('255.255.255.0'))
        assert_that(port.gateway_address, equal_to('0.0.0.0'))
        assert_that(port.existed, equal_to(True))

    @patch_cli()
    def test_get_all(self):
        ports = VNXConnectionPort.get(t_cli())
        assert_that(len(ports), equal_to(20))

    @patch_cli()
    def test_get_by_sp(self):
        ports = VNXConnectionPort.get(t_cli(), VNXSPEnum.SP_A)
        assert_that(len(ports), equal_to(10))

    @patch_cli()
    def test_get_by_port(self):
        ports = VNXConnectionPort.get(t_cli(), port_id=8)
        assert_that(len(ports), equal_to(2))

    @patch_cli()
    def test_get_single(self):
        port = VNXConnectionPort.get(t_cli(), VNXSPEnum.SP_A, 4)
        assert_that(port, equal_to([]))
