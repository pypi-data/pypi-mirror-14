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

from storops.lib.common import daemon, cache
from storops.vnx.cli import CliClient
from storops.vnx.resource.block_pool import VNXPool, VNXPoolFeature
from storops.vnx.resource.cg import VNXConsistencyGroup
from storops.vnx.resource.disk import VNXDisk
from storops.vnx.resource.vnx_domain import VNXDomainMemberList, \
    VNXNetworkAdmin, VNXDomainNodeList
from storops.vnx.resource.lun import VNXLun
from storops.vnx.resource.migration import VNXMigrationSession
from storops.vnx.resource.ndu import VNXNdu, VNXNduList
from storops.vnx.resource.port import VNXConnectionPort, VNXSPPort
from storops.vnx.resource.resource import VNXCliResource
from storops.vnx.resource.rg import VNXRaidGroup
from storops.vnx.resource.sg import VNXStorageGroup
from storops.vnx.resource.snap import VNXSnap

__author__ = 'Cedric Zhuang'


class VNXSystem(VNXCliResource):
    """ The system class for VNX

    This class act as the entry point for VNX system.
    Various VNX resources could be retrieved with methods/properties
    of this class.
    """

    def __init__(self, ip=None,
                 username=None, password=None, scope=0, sec_file=None,
                 timeout=None,
                 heartbeat_interval=None,
                 naviseccli=None):
        """ initialize a `VNXSystem` instance

        The `VNXSystem` instance act as a entry point for all
        VNX resources.

        :param ip: ip of one block sp
        :param username: username for block system
        :param password: password for the specified block user
        :param scope: scope of the specified block user
        :param sec_file: security file used by naviseccli
        :param timeout: naviseccli command timeout
        :param heartbeat_interval: heartbeat interval used to check the
        alive of sp.  Set to 0 if heart beat is not required.
        :param naviseccli: binary location of naviseccli in your host.
        :return: vnx system instance
        """
        super(VNXSystem, self).__init__()
        self._cli = CliClient(ip,
                              username, password, scope,
                              sec_file,
                              timeout,
                              heartbeat_interval=heartbeat_interval,
                              naviseccli=naviseccli)

        self._ndu_list = VNXNduList(self._cli)
        self._ndu_list.with_no_poll()
        if heartbeat_interval:
            daemon(self._update_nodes_ip)

    def set_naviseccli(self, cli_binary):
        self._cli.set_binary(cli_binary)

    def set_block_credential(self,
                             username=None, password=None, scope=None,
                             sec_file=None):
        self._cli.set_credential(username, password, scope, sec_file)

    def _update_nodes_ip(self):
        self._cli.set_ip(self.spa_ip, self.spb_ip, self.control_station_ip)

    def update(self, data=None):
        super(VNXSystem, self).update(data)
        self._ndu_list.update()
        self._update_nodes_ip()

    @property
    def heartbeat(self):
        return self._cli.heartbeat

    @property
    @cache()
    def spa_ip(self):
        return VNXNetworkAdmin.get_spa_ip(self._cli)

    @property
    @cache()
    def spb_ip(self):
        return VNXNetworkAdmin.get_spb_ip(self._cli)

    @property
    @cache()
    def control_station_ip(self):
        return VNXDomainNodeList.get_cs_ip(self.serial, self._cli)

    @property
    def domain(self):
        return VNXDomainMemberList(self._cli)

    def _get_raw_resource(self):
        return self._cli.get_agent(poll=self.poll)

    def get_pool_feature(self):
        return VNXPoolFeature(self._cli)

    def get_pool(self, name=None, pool_id=None):
        return VNXPool.get(pool_id=pool_id, name=name, cli=self._cli)

    def get_lun(self, lun_id=None, name=None, lun_type=None):
        return VNXLun.get(self._cli, lun_id=lun_id, name=name,
                          lun_type=lun_type)

    def get_cg(self, name=None):
        return VNXConsistencyGroup.get(self._cli, name)

    def get_sg(self, name=None):
        return VNXStorageGroup.get(self._cli, name)

    def get_snap(self, name=None):
        return VNXSnap.get(self._cli, name)

    def get_migration_session(self, src_lun=None):
        return VNXMigrationSession.get(self._cli, src_lun)

    def get_ndu(self, name=None):
        return VNXNdu.get(self._cli, name)

    def get_connection_port(self, sp=None, port_id=None, vport_id=None):
        return VNXConnectionPort.get(self._cli, sp, port_id, vport_id)

    def get_sp_port(self, sp=None, port_id=None):
        return VNXSPPort.get(self._cli, sp, port_id)

    def remove_snap(self, name):
        self._remove_resource(VNXSnap(name, self._cli))

    def create_sg(self, name):
        return VNXStorageGroup.create(name, self._cli)

    def remove_sg(self, name):
        self._remove_resource(VNXStorageGroup(name, self._cli))

    def create_cg(self, name, members=None):
        return VNXConsistencyGroup.create(self._cli, name=name,
                                          members=members)

    def remove_cg(self, name):
        self._remove_resource(VNXConsistencyGroup(name, self._cli))

    def get_disk(self, disk_index=None):
        return VNXDisk.get(self._cli, disk_index)

    def get_available_disks(self):
        pool_feature = VNXPoolFeature(self._cli)
        pool_feature.poll = self.poll
        disks = pool_feature.available_disks
        disks.poll = self.poll
        return disks

    def remove_disk(self, disk_index):
        self._remove_resource(VNXDisk(disk_index, self._cli))

    def install_disk(self, disk_index):
        disk = VNXDisk(disk_index, self._cli)
        disk.install()

    def get_rg(self, rg_id=None):
        return VNXRaidGroup.get(self._cli, rg_id)

    def create_rg(self, rg_id, disks, raid_type=None):
        return VNXRaidGroup.create(self._cli, rg_id, disks, raid_type)

    def remove_rg(self, rg_id):
        self._remove_resource(VNXRaidGroup(rg_id, self._cli))

    def create_pool(self, name, disks, raid_type=None):
        return VNXPool.create(self._cli, name, disks, raid_type)

    def _remove_resource(self, resource):
        resource.poll = self.poll
        resource.remove()

    def remove_pool(self, name=None, pool_id=None):
        self._remove_resource(VNXPool(pool_id, name, self._cli))

    def stop_heart_beat(self):
        self._cli.heartbeat.stop()

    def is_compression_enabled(self):
        return self._ndu_list.is_compression_enabled()

    def is_dedup_enabled(self):
        return self._ndu_list.is_dedup_enabled()

    def is_snap_enabled(self):
        return self._ndu_list.is_snap_enabled()

    def is_mirror_view_async_enabled(self):
        return self._ndu_list.is_mirror_view_async_enabled()

    def is_mirror_view_sync_enabled(self):
        return self._ndu_list.is_mirror_view_sync_enabled()

    def is_mirror_view_enabled(self):
        return self._ndu_list.is_mirror_view_enabled()

    def is_thin_enabled(self):
        return self._ndu_list.is_thin_enabled()

    def is_sancopy_enabled(self):
        return self._ndu_list.is_sancopy_enabled()

    def is_auto_tiering_enabled(self):
        return self._ndu_list.is_auto_tiering_enabled()

    def is_fast_cache_enabled(self):
        return self._ndu_list.is_fast_cache_enabled()

    def __del__(self):
        del self._cli
