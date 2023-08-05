# Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""BigIP system failover module

REST URI
    ``http://localhost/mgmt/tm/sys/failover``

GUI Path
    ``System --> Failover``

REST Kind
    ``tm:sys:failover:*``
"""

from f5.bigip.mixins import UnnamedResourceMixin
from f5.bigip.resource import Resource


class Failover(UnnamedResourceMixin, Resource):
    '''BigIP Failover stats and state change.

    The failover object only supports load and update because it is an
    unnamed resource.

    To force the unit to standby call the ``update()`` method as follows:

    .. code-block:: python
        f.update(command='run', standby=None, trafficGroup='mytrafficgroup')

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    '''
    def __init__(self, sys):
        super(Failover, self).__init__(sys)
        endpoint = self.__class__.__name__.lower()
        self._meta_data['required_refresh_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:failover:failoverstats'
        self._meta_data['uri'] =\
            self._meta_data['container']._meta_data['uri'] + endpoint + '/'
