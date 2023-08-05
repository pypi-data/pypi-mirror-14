# Copyright 2014 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test Motor with callbacks and asyncio."""

import asyncio
import unittest

from pymongo.errors import DuplicateKeyError

from test.asyncio_tests import asyncio_test, AsyncIOTestCase


class TestAsyncIOCallbacks(AsyncIOTestCase):
    @asyncio_test
    def test_callbacks(self):
        future = asyncio.Future(loop=self.loop)

        def callback(res, error):
            if error:
                future.set_exception(error)
            else:
                future.set_result(res)

        yield from self.collection.remove()
        yield from self.collection.insert({'_id': 1})
        self.collection.find_one(callback=callback)
        result = yield from future
        self.assertEqual({'_id': 1}, result)

        # Reset the Future.
        future = asyncio.Future(loop=self.loop)
        self.collection.insert({'_id': 1}, callback=callback)
        with self.assertRaises(DuplicateKeyError):
            yield from future


if __name__ == '__main__':
    unittest.main()
