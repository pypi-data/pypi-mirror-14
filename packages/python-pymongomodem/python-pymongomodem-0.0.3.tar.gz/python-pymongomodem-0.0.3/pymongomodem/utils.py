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
from functools import wraps

token_substitutions = [
    ('.', '^')
]


def __sanitize_for_token(arg, token, substitute):
    if hasattr(arg, "__iter__"):
        for item in arg:
            __sanitize_for_token(item, token, substitute)

    if isinstance(arg, dict):
        for key in arg:
            _key = key
            if token in key:
                _key = key.replace(token, substitute)
                arg[_key] = arg.pop(key)

            if isinstance(arg[_key], dict):
                __sanitize_for_token(arg[_key], token, substitute)
    return arg


def __sanitize(arg):
    sanitized_arg = None
    for token, substitute in token_substitutions:
        sanitized_arg = __sanitize_for_token(arg, token, substitute)
    return sanitized_arg


def encode_input(function):
    @wraps(function)
    def encode(*args, **kwargs):
        sanitized_args = []
        for arg in args:
            sanitized_args.append(__sanitize(arg))

        sanitized_kwargs = {}
        for key, value in kwargs.iteritems():
            sanitized_kwargs[key] = __sanitize(value)

        return function(*sanitized_args, **sanitized_kwargs)

    return encode


def decode_output(function):
    @wraps(function)
    def decode(*args, **kwargs):
        result = function(*args, **kwargs)
        sanitized_result = None
        for token, substitute in token_substitutions:
            sanitized_result = __sanitize_for_token(result, substitute, token)
        return sanitized_result

    return decode
