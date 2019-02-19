import os
import shutil
from io import BytesIO

from PIL import Image
from django.test import TestCase, override_settings

from BosvogelWebPlatform.settings import BASE_DIR
from utils.model_utils import OverwriteOnSameNameStorage

TEST_IMAGE_NAME = 'test_image.png'


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media_root'))
class ModelUtilsTestCase(TestCase):

    test_dir = os.path.join(BASE_DIR, 'test_media_root')

    def setUp(self):
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_saving_file(self):
        self.assertEqual(os.listdir(self.test_dir), [], 'No file should exist yet')

        # Build
        file = BytesIO()
        test_image = Image.new('RGBA', size=(500, 500), color=(155, 0, 0))
        test_image.save(file, 'png')
        file.name = 'test_image.png'

        storage = OverwriteOnSameNameStorage()

        # Operate
        storage.save(name=file.name, content=file)

        # Check
        self.assertEqual(os.listdir(self.test_dir), ['test_image.png'], 'The test image should have been created')

    def test_overwriting_file_with_same_name(self):
        self.assertEqual(os.listdir(self.test_dir), [], 'No file should exist yet')

        # Build
        first_file = BytesIO()
        test_image = Image.new('RGBA', size=(500, 500), color=(155, 0, 0))
        test_image.save(first_file, 'png')
        first_file.name = TEST_IMAGE_NAME

        second_file = BytesIO()
        test_image = Image.new('RGBA', size=(100, 100), color=(0, 155, 0))
        test_image.save(second_file, 'png')
        second_file.name = TEST_IMAGE_NAME

        storage = OverwriteOnSameNameStorage()
        storage.media_root = self.test_dir

        # Operate
        storage.save(name=first_file.name, content=first_file)
        old_image = Image.open(os.path.join(self.test_dir, TEST_IMAGE_NAME))
        self.assertEqual(old_image.size, (500, 500), 'The red 500x500px image should be saved')
        storage.save(name=second_file.name, content=second_file)

        # Check
        self.assertEqual(os.listdir(self.test_dir), [TEST_IMAGE_NAME], 'Only one file should exist')

        new_image = Image.open(os.path.join(self.test_dir, TEST_IMAGE_NAME))
        self.assertEqual(new_image.size, (100, 100),
                         'The red 500x500px image should be replaced with a green 100x100px')
