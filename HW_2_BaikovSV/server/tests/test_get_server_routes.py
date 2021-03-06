import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
sys.path.append(str(BASE_DIR))

from server.routes import get_server_routes


def test_get_server_routes():
    routes = get_server_routes()
    routes_mapping = {}
    for controller_route in routes or get_server_routes():
        for route in controller_route:
            routes_mapping[route['action']] = route['controller']

    assert routes_mapping.get('now') is not None
    assert routes_mapping.get('echo') is not None
    assert routes_mapping.get('bad_action') is None
