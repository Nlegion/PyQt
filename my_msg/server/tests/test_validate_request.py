import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
sys.path.append(str(BASE_DIR))

from server.protocol import validate_request


def test_make_400():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'user': 'User'
    }

    is_valid = validate_request(request)

    assert is_valid is True

    request = {'user': 'User'}

    is_valid = validate_request(request)

    assert is_valid is False
