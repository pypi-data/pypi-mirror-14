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
import unittest

from hamcrest import assert_that, has_entry

from pymongomodem.utils import encode_input, decode_output


@encode_input
def encode_input_decorated_function(n1, n2=None):
    return


@decode_output
def decode_output_decorated_function(n1):
    return n1


class PyMongoModemTest(unittest.TestCase):
    def test_encode_input_basic_replace_dot_in_keys(self):
        n1 = {
            'patate.poil': 'value.patate'
        }

        n2 = {
            'a.key.to.sanitize': 'some.value'
        }

        encode_input_decorated_function(n1, n2=n2)

        assert_that(n1, has_entry('patate^poil', 'value.patate'))
        assert_that(n2, has_entry('a^key^to^sanitize', 'some.value'))

    def test_encode_input_recursive_replace_dot_in_keys(self):
        notification = {
            'patate.poil': 'value.patate',
            'a.key.to.sanitize': 'some.value',
            'payload': {
                'an.other_key.to_sanitize': 'some.value_value',
            }
        }

        encode_input_decorated_function(notification)

        assert_that(notification, has_entry('patate^poil', 'value.patate'))
        assert_that(notification, has_entry('a^key^to^sanitize', 'some.value'))
        assert_that(notification.get('payload'), has_entry('an^other_key^to_sanitize', 'some.value_value'))

    def test_decode_output_replace_caret_in_keys(self):
        notification = {
            'patate^poil': 'value.patate',
            'a^key^to^sanitize': 'some.value',
            'payload': {
                'an^other_key^to_sanitize': 'some.value_value',
            }
        }

        decode_output_decorated_function(notification)

        assert_that(notification, has_entry('patate.poil', 'value.patate'))
        assert_that(notification, has_entry('a.key.to.sanitize', 'some.value'))
        assert_that(notification.get('payload'), has_entry('an.other_key.to_sanitize', 'some.value_value'))

    def test_decode_output_replace_caret_in_keys_for_list(self):
        notifications = [{
            'patate^poil': 'value.patate',
            'payload': {
                'an^other_key^to_sanitize': 'some.value_value',
            }
        },
            {
                'key^2': 'value.key.2',
                'payload': {
                    'sanitize^that^key_2': 'sanitize_value.2',
                }
            }
        ]

        decode_output_decorated_function(notifications)

        assert_that(notifications[0], has_entry('patate.poil', 'value.patate'))
        assert_that(notifications[0].get('payload'), has_entry('an.other_key.to_sanitize', 'some.value_value'))
        assert_that(notifications[1], has_entry('key.2', 'value.key.2'))
        assert_that(notifications[1].get('payload'), has_entry('sanitize.that.key_2', 'sanitize_value.2'))
