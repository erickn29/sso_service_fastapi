from datetime import datetime
from uuid import UUID

import jwt

from core.constants import TZ


def get_jwt(user_id: UUID, secret_key: str):
    token = jwt.encode(
        {
            "id": str(user_id),
            "expat": datetime.now(tz=TZ.MSK).timestamp() + 300,
        },
        secret_key,
        algorithm="HS256",
    )
    return token
