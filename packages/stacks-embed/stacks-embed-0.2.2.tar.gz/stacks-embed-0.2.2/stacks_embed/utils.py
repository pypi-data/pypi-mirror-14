import tempfile

from django.core.files import File

import requests


class ImageNotAvailable(Exception):
    pass


def retrieve_file_from_url(url_to_image):
    """
    Returns a 2-tuple of a filename and a django File object instance of
    an image at `url_to_image`

    Raises ImageNotAvailable if an image could not be retrieved.
    """
    # Stream the image from the url
    request = requests.get(url_to_image, stream=True)
    # Was the request OK?
    if request.status_code == 200:
        # Get the filename from the url, used for saving later
        filename = url_to_image.split('/')[-1]
        # Create a temporary file
        streamed_file = tempfile.NamedTemporaryFile()
        # Read the streamed image in sections
        for block in request.iter_content(1024 * 8):

            # If no more file then stop
            if not block:
                break

            # Write image block to temporary file
            streamed_file.write(block)
        return (filename, File(streamed_file))
    else:
        raise ImageNotAvailable(
            'There was a problem retrieving an image from: {}'.format(
                url_to_image
            )
        )
