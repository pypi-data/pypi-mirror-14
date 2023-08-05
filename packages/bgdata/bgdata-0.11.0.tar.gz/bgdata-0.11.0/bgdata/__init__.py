import logging
import os
from bgdata import errors, downloader

DEVELOP = downloader.DEVELOP
LATEST = downloader.LATEST

DatasetError = errors.DatasetError
Downloader = downloader.Downloader

# Logging config
logger = logging.getLogger(__name__)


def remote_repository_url():
    """
    Returns the remote BGDATA repository URL. It returns the OS environment variable BGDATA_REMOTE if it's defined, otherwise the official URL.

    :return: The BGDATA remote repository URL
    """
    return os.environ.get("BGDATA_REMOTE", "http://bg.upf.edu/bgdata")


def local_repository_url():

    # Check environment variable
    repository = os.path.expanduser(os.environ.get("BGDATA_LOCAL", "~/.bgdata"))

    # Create the local repository
    if not os.path.exists(repository):
        os.makedirs(repository)

    return repository

# Create a default downloader
downloader = Downloader(
    local_repository=local_repository_url(),
    remote_repository=remote_repository_url(),
    num_connections=4
)

# Shortcut to default methods
get_path = downloader.get_path
is_downloaded = downloader.is_downloaded
