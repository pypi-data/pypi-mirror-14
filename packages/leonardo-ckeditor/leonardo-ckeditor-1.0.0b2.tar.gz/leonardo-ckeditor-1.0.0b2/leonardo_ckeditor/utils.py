from __future__ import absolute_import

import os

from django.conf import settings
from django.core.files.storage import default_storage

SKIP_DIRECTORIES = [
    'cache',
    '_cache',
    'public_thumbnails',
]


def get_image_files(user=None, path=''):
    """
    Recursively walks all dirs under upload dir and generates a list of
    full paths for each file found.
    """
    # If a user is provided and CKEDITOR_RESTRICT_BY_USER is True,
    # limit images to user specific path, but not for superusers.
    STORAGE_DIRECTORIES = 0
    STORAGE_FILES = 1

    restrict = getattr(settings, 'CKEDITOR_RESTRICT_BY_USER', False)
    if user and not user.is_superuser and restrict:
        user_path = user.username
    else:
        user_path = ''

    browse_path = os.path.join(settings.CKEDITOR_UPLOAD_PATH, user_path, path)

    try:
        storage_list = default_storage.listdir(browse_path)
    except NotImplementedError:
        return
    except OSError:
        return

    for filename in storage_list[STORAGE_FILES]:
        if os.path.splitext(filename)[0].endswith('_thumb') or os.path.basename(filename).startswith('.'):
            continue
        filename = os.path.join(browse_path, filename)
        yield filename

    for directory in storage_list[STORAGE_DIRECTORIES]:
        if directory.startswith('.') or directory.startswith(tuple(SKIP_DIRECTORIES)):
            continue
        directory_path = os.path.join(path, directory)
        for element in get_image_files(user=user, path=directory_path):
            yield element


def monkey_patch_ckeditor():

    from ckeditor_uploader import views
    views.get_image_files = get_image_files
