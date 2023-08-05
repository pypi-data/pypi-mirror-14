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

from yabgp.message.attribute import Attribute
from yabgp.message.attribute import AttributeFlag
from yabgp.message.attribute import AttributeID


class PMSITunnel(Attribute):
    """
    RFC 6514#section-5
    """
    ID = AttributeID.EXTENDED_COMMUNITY
    FLAG = AttributeFlag.OPTIONAL + AttributeFlag.TRANSITIVE

    @classmethod
    def parse(cls, value):
        """
        +---------------------------------+
        |  Flags (1 octet)                |
        +---------------------------------+
        |  Tunnel Type (1 octets)         |
        +---------------------------------+
        |  MPLS Label (3 octets)          |
        +---------------------------------+
        |  Tunnel Identifier (variable)   |
        +---------------------------------+
        """
        flag = value[0]
        tunnel_type = value[1]
        mpls_label = value[2: 5]
        tunnel_id = value[5:]

        return {
            'leaf_info_required': flag,
            'tunnel_type': tunnel_type,
            'mpsl_label': mpls_label,
            'tunnel_id': tunnel_id
        }

    @classmethod
    def construct(cls, value):
        pass

