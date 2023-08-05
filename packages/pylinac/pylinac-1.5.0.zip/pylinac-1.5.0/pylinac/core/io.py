"""I/O helper functions for pylinac."""
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve
import zipfile


class TemporaryZipDirectory(TemporaryDirectory):
    """Creates a temporary directory that unpacks a ZIP archive."""
    def __init__(self, zfile):
        """
        Parameters
        ----------
        zfile : str
            String that points to a ZIP archive.
        """
        super().__init__()
        zfiles = zipfile.ZipFile(zfile)
        zfiles.extractall(path=self.name)


def get_url(url, destination=None):
    """Download a URL to a local file.

    Parameters
    ----------
    url : str
        The URL to download.
    destination : str, None
        The destination of the file. If None is given the file is saved to a temporary directory.

    Returns
    -------
    filename : str
        The location of the downloaded file.
    """
    try:
        filename, _ = urlretrieve(url, filename=destination)
    except (HTTPError, URLError, ValueError) as e:
        raise e
    return filename
