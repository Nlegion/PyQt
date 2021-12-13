import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from server.dates.controllers import get_date_now


def test_get_date_now():
    date = datetime.now()
    s_date = date.strftime('%Y.%m.%d')

    request = {
        'time': datetime.now().timestamp(),
        'action': 'now'
    }

    response = get_date_now(request)

    assert response.get('data') == s_date
