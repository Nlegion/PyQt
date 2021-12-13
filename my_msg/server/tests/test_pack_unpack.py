import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
sys.path.append(str(BASE_DIR))

from core import jim


def test_pack_unpack():
    request = {
        'time': datetime.now().timestamp(),
        'action': 'now',
        'data': 'Hello'
    }

    b_request = jim.pack(request)
    request = jim.unpack(b_request)

    assert request.get('action') == 'now'
    assert request.get('data') == 'Hello'
