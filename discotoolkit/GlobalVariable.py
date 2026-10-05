"""
Settings shared by the rest of the package: logging, the request timeout and --
most importantly -- which DISCO server the toolkit talks to.

By default the toolkit talks to DISCO v1 (https://disco.bii.a-star.edu.sg). To use
another server:

    import discotoolkit as dt
    dt.set_server("v2")                          # a named preset
    dt.set_server("https://my.server/disco_v3_api/")   # any server with the same API

or set the DISCO_API_URL environment variable before importing the package.
"""

import logging
import os

logging.basicConfig(level=logging.INFO)

# seconds to wait for the server; the reference downloads are tens of MB
timeout = 600

# The API roots the toolkit knows by name. Both serve the same `toolkit/...` endpoints.
SERVERS = {
    "v1": "https://disco.bii.a-star.edu.sg/disco_v3_api/",
    "v2": "https://immunesinglecell.org/disco_v3_api/",
}
DEFAULT_SERVER = "v1"


def _normalise(server: str) -> str:
    """Turn a preset name or a URL into an API root that ends with exactly one '/'."""
    if not isinstance(server, str) or not server.strip():
        raise ValueError("server must be a preset name (%s) or a URL" % ", ".join(SERVERS))
    server = server.strip()
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
        server (str): "v1", "v2", or the full URL of an API root such as
            "https://disco.bii.a-star.edu.sg/disco_v3_api/".

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
