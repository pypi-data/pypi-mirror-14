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

import six
from hamcrest import assert_that, raises
from hamcrest import equal_to

from test.vnx.nas_mock import MockXmlPost
from storops.exception import VNXException
from storops.vnx.enums import VNXError, VNXProvisionEnum, \
    VNXTieringEnum, VNXSPEnum, has_error, VNXRaidType, raise_if_err
from storops.vnx.resource.nas_client import NasXmlResponse


class VNXErrorTest(TestCase):
    def test_has_error(self):
        output = "The specified snapshot name is already in use. (0x716d8005)"
        self.assertTrue(has_error(output))

    def test_has_error_with_specific_error(self):
        output = "The specified snapshot name is already in use. (0x716d8005)"
        err = has_error(output, VNXError.SNAP_NAME_EXISTED)
        self.assertTrue(err)
        err = has_error(output, VNXError.LUN_ALREADY_EXPANDED)
        self.assertFalse(err)

    def test_has_error_not_found(self):
        output = "Cannot find the consistency group."
        err = has_error(output)
        self.assertTrue(err)

        err = has_error(output, VNXError.GENERAL_NOT_FOUND)
        self.assertTrue(err)

    def test_has_error_not_exist(self):
        output = "The specified snapshot does not exist."
        err = has_error(output, VNXError.GENERAL_NOT_FOUND)
        self.assertTrue(err)

        output = "The (pool lun) may not exist."
        err = has_error(output, VNXError.GENERAL_NOT_FOUND)
        self.assertTrue(err)

    def test_has_error_multi_line(self):
        output = """Could not retrieve the specified (pool lun).
                    The (pool lun) may not exist."""
        err = has_error(output, VNXError.GENERAL_NOT_FOUND)
        self.assertTrue(err)

    def test_has_error_regular_string_false(self):
        output = "Cannot unbind LUN because it's contained in a Storage Group."
        err = has_error(output, VNXError.GENERAL_NOT_FOUND)
        self.assertFalse(err)

    def test_has_error_multi_errors(self):
        output = "Cannot unbind LUN because it's contained in a Storage Group."
        err = has_error(output,
                        VNXError.LUN_IN_SG,
                        VNXError.GENERAL_NOT_FOUND)
        self.assertTrue(err)

        output = "Cannot unbind LUN because it's contained in a Storage Group."
        err = has_error(output,
                        VNXError.LUN_ALREADY_EXPANDED,
                        VNXError.LUN_NOT_MIGRATING)
        self.assertFalse(err)

    def test_has_error_ev_error(self):
        class ForTest(object):
            pass

        error = ForTest()
        error.where = 'EV_ScsiPipe::_sendCommand() - Sense Data'
        error.why = 'SP A: LUN already exists in the specified storage group.'
        error.who = '@(#)libconnect Revision 7.33.6.2.50 on 1/6/2015 21:54:55'

        err = has_error(error,
                        VNXError.SG_LUN_ALREADY_EXISTS)
        self.assertTrue(err)

    def test_sp_error_not_supported(self):
        out = ('Error returned from the target: 10.244.211.32\n'
               'CLI commands are not supported by the target storage system.')
        err = has_error(out, VNXError.NOT_A_SP)
        assert_that(err, equal_to(True))

    def test_sp_error_time_out(self):
        out = ("A network error occurred while "
               "trying to connect: '10.244.211.33'.\n"
               "Message : select: The connect timed out.")
        err = has_error(out, VNXError.SP_NOT_AVAILABLE)
        assert_that(err, equal_to(True))

    def test_raise_if_err_normal(self):
        raise_if_err('')
        # no raises

    def test_raise_if_err_non_empty(self):
        def f():
            raise_if_err('error msg', msg="error received")

        assert_that(f, raises(ValueError, "error received"))

    def test_raise_if_err_vnx_error(self):
        def f():
            raise_if_err('specified lun may not exist', VNXException,
                         expected_error=VNXError.GENERAL_NOT_FOUND)

        assert_that(f, raises(VNXException, 'specified lun may not exist'))

    def test_raise_if_err_nas_response_input(self):
        def f():
            resp = NasXmlResponse(MockXmlPost.read_file('fs_not_found.xml'))
            raise_if_err(resp, VNXException,
                         expected_error=VNXError.FS_NOT_FOUND)

        assert_that(f, raises(VNXException, 'not found'))


class VNXProvisionEnumTest(TestCase):
    def test_get_opt_dedup(self):
        opt = VNXProvisionEnum.get_opt(VNXProvisionEnum.DEDUPED)
        self.assertEqual('-type Thin -deduplication on',
                         ' '.join(opt))

    def test_get_opt_thin(self):
        opt = VNXProvisionEnum.get_opt(VNXProvisionEnum.THIN)
        self.assertEqual('-type Thin',
                         ' '.join(opt))

    def test_get_opt_thick(self):
        opt = VNXProvisionEnum.get_opt(VNXProvisionEnum.THICK)
        self.assertEqual('-type NonThin',
                         ' '.join(opt))

    def test_get_opt_compressed(self):
        opt = VNXProvisionEnum.get_opt(VNXProvisionEnum.COMPRESSED)
        self.assertEqual('-type Thin',
                         ' '.join(opt))

    def test_get_opt_not_available(self):
        self.assertRaises(ValueError, VNXProvisionEnum.get_opt, 'na')


class VNXTieringEnumTest(TestCase):
    def test_get_opt(self):
        opt = VNXTieringEnum.get_opt(VNXTieringEnum.HIGH_AUTO)
        self.assertEqual(
            '-initialTier highestAvailable -tieringPolicy autoTier',
            ' '.join(opt))

    def test_get_opt_not_available(self):
        self.assertRaises(ValueError, VNXTieringEnum.get_opt, 'na')


class VNXSPEnumTest(TestCase):
    def test_from_str(self):
        data = {
            'spa': VNXSPEnum.SP_A,
            'sp': None,
            'sp_a': VNXSPEnum.SP_A,
            'SP b': VNXSPEnum.SP_B,
            'a': VNXSPEnum.SP_A,
            'b': VNXSPEnum.SP_B,
            'cs': VNXSPEnum.CONTROL_STATION,
            'Celerra_CS0_21111': VNXSPEnum.CONTROL_STATION,
            'VPI-24092B': VNXSPEnum.SP_B
        }

        for k, v in six.iteritems(data):
            assert_that(VNXSPEnum.from_str(k), equal_to(v),
                        'input: {}'.format(k))

    def test_get_sp_index_err(self):
        def f():
            VNXSPEnum.get_sp_index('abc')

        assert_that(f, raises(ValueError, 'not a valid sp'))

    def test_get_sp_index(self):
        assert_that(VNXSPEnum.get_sp_index('spa'), equal_to('a'))


class VNXRaidTypeTest(TestCase):
    def test_from_str(self):
        assert_that(VNXRaidType.from_str('r5'), equal_to(VNXRaidType.RAID5))
