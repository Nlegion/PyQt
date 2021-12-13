import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from server.echo.controllers import get_echo


def test_echo_bad_request():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now'
    }

    response = get_echo(request)

    assert response.get('code') == 400
