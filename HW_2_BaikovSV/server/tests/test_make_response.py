import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
sys.path.append(str(BASE_DIR))

from server.protocol import make_response


def test_make_400():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'user': 'User'
    }

    response = make_response(request, 200, 'Hello')

    assert response.get("code") == 200
    assert response.get("data") == 'Hello'
    assert response.get("user") == 'User'
    assert response.get("action") == 'now'
