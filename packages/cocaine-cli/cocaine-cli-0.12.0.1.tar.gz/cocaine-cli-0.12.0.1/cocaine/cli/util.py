from cStringIO import StringIO
import tarfile
import urlparse
import posixpath

import logging
import re

log = logging.getLogger("cocaine-cli.util")

root_logger = logging.getLogger()


def make_archive(path, logger=root_logger):
    stream = StringIO()
    try:
        tar = tarfile.open(mode='w', fileobj=stream)
        tar.add(path, arcname='.')
        logger.info(tar.getnames())
        return stream.getvalue()
    finally:
        stream.close()


def normalize_url(url):
    u1 = urlparse.urlparse(url)
    log.debug("u1 = urlparse.urlparse(url) %s", u1)
    u2 = [c for c in u1]
    log.debug("u2 = [c for c in u1] %s", u2)

    if not u2[2]:
        u2[2] = "/"

    u2[2] = posixpath.normpath(u2[2])
    log.debug("u2[2] = posixpath.normpath(u1.path) %s", u2[2])

    u2[2] = re.sub(r'//', '/', u2[2])
    log.debug("re.sub(r'//', '/', u1.path) %s", u2[2])

    if u1.path and u1.path[-1] == "/":
        u2[2] += "/"

    log.debug("u2 %s", u2)

    u3 = urlparse.urlunparse(u2)
    return u3
