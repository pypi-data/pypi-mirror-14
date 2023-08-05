# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import six

from openstack.tests.functional import base
from openstack.tests.functional.image.v2.test_image import TEST_IMAGE_NAME


class TestImage(base.BaseFunctionalTest):

    def test_images(self):
        images = list(self.conn.compute.images())
        self.assertGreater(len(images), 0)
        for image in images:
            self.assertIsInstance(image.id, six.string_types)

    def _get_non_test_image(self):
        images = self.conn.compute.images()
        image = next(images)

        if image.name == TEST_IMAGE_NAME:
            image = next(images)

        return image

    def test_find_image(self):
        image = self._get_non_test_image()
        self.assertIsNotNone(image)
        sot = self.conn.compute.find_image(image.id)
        self.assertEqual(image.id, sot.id)
        self.assertEqual(image.name, sot.name)

    def test_get_image(self):
        image = self._get_non_test_image()
        self.assertIsNotNone(image)
        sot = self.conn.compute.get_image(image.id)
        self.assertEqual(image.id, sot.id)
        self.assertEqual(image.name, sot.name)
        self.assertIn('links', image)
        self.assertIn('minDisk', image)
        self.assertIn('minRam', image)
        self.assertIn('metadata', image)
        self.assertIn('progress', image)
        self.assertIn('status', image)

    def test_image_metadata(self):
        image = self._get_non_test_image()
        sot = self.conn.compute.get_image(image.id)

        # Start by clearing out any other metadata.
        self.assertDictEqual(self.conn.compute.replace_image_metadata(sot),
                             {})

        # Insert first and last name metadata
        meta = {"first": "Matthew", "last": "Dellavedova"}
        self.assertDictEqual(
            self.conn.compute.create_image_metadata(sot, **meta), meta)

        # Update only the first name
        short = {"first": "Matt", "last": "Dellavedova"}
        self.assertDictEqual(
            self.conn.compute.update_image_metadata(sot,
                                                    first=short["first"]),
            short)

        # Get all metadata and then only the last name
        self.assertDictEqual(self.conn.compute.get_image_metadata(sot),
                             short)
        self.assertDictEqual(
            self.conn.compute.get_image_metadata(sot, "last"),
            {"last": short["last"]})

        # Replace everything with just a nickname
        nick = {"nickname": "Delly"}
        self.assertDictEqual(
            self.conn.compute.replace_image_metadata(sot, **nick),
            nick)
        self.assertDictEqual(self.conn.compute.get_image_metadata(sot),
                             nick)

        # Delete the only remaining key, make sure we're empty
        self.assertIsNone(
            self.conn.compute.delete_image_metadata(sot, "nickname"))
        self.assertDictEqual(self.conn.compute.get_image_metadata(sot), {})
