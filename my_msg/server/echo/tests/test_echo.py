import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from server.echo.controllers import get_echo


def test_get_echo():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'data': 'Hello'
    }

    response = get_echo(request)

    assert response.get('data') == 'Hello'
