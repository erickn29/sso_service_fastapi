from datetime import datetime, timedelta
from uuid import UUID

import jwt
import pytz


def get_jwt(user_id: UUID, secret_key: str):
    token = jwt.encode(
        {
            "id": str(user_id),
            "exp": datetime.now(tz=pytz.utc) + timedelta(seconds=300),
        },
        secret_key,
        algorithm="HS256",
    )
    return token
