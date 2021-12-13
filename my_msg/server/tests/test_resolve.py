import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
sys.path.append(str(BASE_DIR))

from server.routes import resolve


def test_resolve():
    controller = resolve('now')
    assert controller is not None

    controller = resolve('echo')
    assert controller is not None

    controller = resolve('bad_action')
    assert controller is None
