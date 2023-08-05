# Copyright 2016 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from hamcrest import assert_that, is_
from netman.core.objects.exceptions import UnknownInterface
from netman.core.objects.interface_states import ON, OFF

from tests.adapters.configured_test_case import ConfiguredTestCase


class UnsetInterfaceStateTest(ConfiguredTestCase):
    _dev_sample = "juniper"

    def test_returns_an_interface_to_default_state(self):

        default_state = self.client.get_interface(self.test_port).shutdown

        self.try_to.set_interface_state(self.test_port, ON)
        self.client.unset_interface_state(self.test_port)

        assert_that(self.client.get_interface(self.test_port).shutdown, is_(default_state))

        self.try_to.set_interface_state(self.test_port, OFF)
        self.client.unset_interface_state(self.test_port)

        assert_that(self.client.get_interface(self.test_port).shutdown, is_(default_state))

    def test_fails_with_unknown_interface(self):
        with self.assertRaises(UnknownInterface):
            self.client.unset_interface_state('ge-0/0/1nonexistent2000')

    def tearDown(self):
        super(UnsetInterfaceStateTest, self).tearDown()
