# Copyright 2015 Internap.
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
import logging
from functools import wraps
import warnings

from tests.adapters.model_list import available_models
from netaddr import IPNetwork
from tests.adapters.shell.terminal_client_test import telnet_hook_to_reactor, ssh_hook_to_reactor
from global_reactor import ThreadedReactor


def setup():
    ThreadedReactor.start_reactor(available_models, reactor_hook_callbacks=[telnet_hook_to_reactor, ssh_hook_to_reactor])


def tearDown():
    ThreadedReactor.stop_reactor()


class ExactIpNetwork(object):
    def __init__(self, ip, mask=None):
        net = IPNetwork(ip)
        self.ip = net.ip
        self.mask = mask or net.prefixlen

    def __eq__(self, other):
        if not isinstance(other, IPNetwork):
            logging.error("{} is not an IPNetwork object".format(repr(other)))
            return False
        result = other.ip == self.ip and other.prefixlen == self.mask
        if not result:
            logging.error("Expected {}/{} and got {}/{}".format(self.ip, self.mask, other.ip, other.prefixlen))
        return result

    def __repr__(self):
        return "{}/{}".format(self.ip, self.mask)


def ignore_deprecation_warnings(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            ret = func(*args, **kwargs)
            return ret
    return func_wrapper
