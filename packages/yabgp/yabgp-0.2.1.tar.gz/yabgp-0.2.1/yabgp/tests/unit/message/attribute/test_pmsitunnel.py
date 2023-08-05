# Copyright 2016 Cisco Systems, Inc.
# All rights reserved.
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

"""Test PMSI Tunnel attribute
"""

import unittest

from yabgp.common.constants import ERR_MSG_UPDATE_ATTR_LEN
from yabgp.common import exception as excep
from yabgp.message.attribute.pmsitunnel import PMSITunnel


class TestPMSITunnel(unittest.TestCase):

    def test_parse(self):
        hex_valule = b'\x00\x06\x00\x27\x10\x04\x04\x04\x04'
        self.assertEqual({}, PMSITunnel.parse(hex_valule))

if __name__ == '__main__':
    unittest.main()
