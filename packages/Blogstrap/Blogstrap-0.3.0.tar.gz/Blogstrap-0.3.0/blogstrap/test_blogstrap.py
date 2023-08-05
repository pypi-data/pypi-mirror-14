# Copyright 2015 Joe H. Rahme <joehakimrahme@gmail.com>
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
import os.path
import tempfile
import unittest

import blogstrap


class BlogstrapTest(unittest.TestCase):

    def setUp(self):
        super(BlogstrapTest, self).setUp()
        application = blogstrap.create_app(".blogstrap.conf")
        self.app = application.test_client()

    def test_success(self):
        # This is just a base test
        response = self.app.get("/")
        self.assertIn(b"SUCCESS", response.data)

    def test_get_article(self):
        # Create a tempfile and GET its url
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix="blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertEqual(200, response.status_code)
        self.assertNotIn(b"SUCCESS", response.data)
        self.tempfile.close()

    def test_get_hidden(self):
        self.tempfile = tempfile.NamedTemporaryFile(
            dir=".",
            prefix=".blogstrap-test-")
        blogpost = os.path.basename(self.tempfile.name)
        response = self.app.get(blogpost)
        self.assertEqual(404, response.status_code)

    def test_get_nonexistent(self):
        response = self.app.get("nonexistent")
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
