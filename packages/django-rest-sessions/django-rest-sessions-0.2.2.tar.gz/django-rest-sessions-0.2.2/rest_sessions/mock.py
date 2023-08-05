from unittest.mock import patch

from django.contrib.sessions.backends.base import SessionBase


def mock_session(**session_data):
    class TestSessionStore(SessionBase):
        _session_cache = session_data

        def save(self):
            pass

    def decorator(f):
        return patch('rest_sessions.SessionStore', TestSessionStore)(f)
    return decorator

