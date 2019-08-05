import os

from django.core.files.storage import FileSystemStorage

from BosvogelWebPlatform.settings import MEDIA_ROOT


class OverwriteOnSameNameStorage(FileSystemStorage):
    media_root = MEDIA_ROOT  # to let the unit tests change media_root

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(self.media_root, name))
        return name
