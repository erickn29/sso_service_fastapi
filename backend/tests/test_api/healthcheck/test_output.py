from datetime import datetime

import jwt

from core.config import config
from core.constants import TZ


async def test_healthcheck_admin_200(init_data, fake_redis, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": datetime.now(tz=TZ.MSK).timestamp() + 300,
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/api/healthcheck/")
    assert response.json() == {"status": "ok"}
