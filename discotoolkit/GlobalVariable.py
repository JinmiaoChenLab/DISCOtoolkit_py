"""
Settings shared by the rest of the package: logging, the request timeout and --
most importantly -- which DISCO server the toolkit talks to.

The toolkit is built for, and tested against, DISCO v1 (https://disco.bii.a-star.edu.sg), and
talks to it by default. DISCO v2 is not supported: it has its own R package (DISCOtoolkit).

For a mirror or a test copy of DISCO v1 there is still a way to point it elsewhere:

    import discotoolkit as dt
    dt.set_server("https://my.mirror/disco_v3_api/")

or set the DISCO_API_URL environment variable before importing the package.
"""

import logging
import os

logging.basicConfig(level=logging.INFO)

# seconds to wait for the server; the reference downloads are tens of MB
timeout = 600

# The API roots the toolkit knows by name.
SERVERS = {
    "v1": "https://disco.bii.a-star.edu.sg/disco_v3_api/",
}
DEFAULT_SERVER = "v1"

# Removed in 1.3.0: the toolkit was never tested against DISCO v2, which has its own R package.
_UNSUPPORTED = {
    "v2": "DISCO v2 is not supported by the Python toolkit, which is built and tested for DISCO v1 "
          "(the default). For DISCO v2 use its R package: https://github.com/JinmiaoChenLab/DISCOtoolkit",
}


def _normalise(server: str) -> str:
    """Turn a preset name or a URL into an API root that ends with exactly one '/'."""
    if not isinstance(server, str) or not server.strip():
        raise ValueError("server must be a preset name (%s) or a URL" % ", ".join(SERVERS))
    server = server.strip()
    if server.lower() in _UNSUPPORTED:
        raise ValueError(_UNSUPPORTED[server.lower()])
    if server.lower() in SERVERS:
        return SERVERS[server.lower()]
    if not server.lower().startswith(("http://", "https://")):
        raise ValueError(
            "unknown server %r: use one of %s or a full http(s):// URL" % (server, ", ".join(SERVERS))
        )
    return server.rstrip("/") + "/"


_server = _normalise(os.environ.get("DISCO_API_URL") or DEFAULT_SERVER)


def set_server(server: str) -> str:
    """Choose which DISCO server the toolkit uses for the rest of the session.

    Args:
        server (str): "v1" (DISCO v1, the default), or the full URL of the API root of a mirror
            or test copy of DISCO v1, such as "http://127.0.0.1:8889/disco_v3_api/".

    Returns:
        str: the API root now in use.
    """
    global _server
    _server = _normalise(server)
    logging.info("DISCOtoolkit is using %s", _server)
    return _server


def get_server() -> str:
    """The API root the toolkit is currently using."""
    return _server


def api_url(path: str) -> str:
    """Full URL for an API path, e.g. api_url("toolkit/getSampleMetadata").

    Looked up on every call, so set_server() takes effect immediately everywhere.
    """
    return _server + path.lstrip("/")


def __getattr__(name):
    # `prefix_disco_url` was a plain variable in earlier releases; keep it readable.
    if name == "prefix_disco_url":
        return _server
    raise AttributeError("module %r has no attribute %r" % (__name__, name))
