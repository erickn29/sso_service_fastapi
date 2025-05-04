import json

from fakeredis.aioredis import FakeRedis


async def set_initial_cache(redis: FakeRedis, init_data: dict):
    for user in init_data["fake_users"]:
        await redis.set(
            name=f"user:{str(user.id)}",
            value=json.dumps(
                {
                    "id": str(user.id),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "patronymic": user.patronymic,
                    "roles": user.roles,
                }
            ),
        )
    await redis.set(
        name=f"user:{str(init_data['bot_sonic'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["bot_sonic"].id),
                "first_name": init_data["bot_sonic"].first_name,
                "last_name": init_data["bot_sonic"].last_name,
                "patronymic": init_data["bot_sonic"].patronymic,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['bot_makar'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["bot_makar"].id),
                "first_name": init_data["bot_makar"].first_name,
                "last_name": init_data["bot_makar"].last_name,
                "patronymic": init_data["bot_makar"].patronymic,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['bot_notify'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["bot_notify"].id),
                "first_name": init_data["bot_notify"].first_name,
                "last_name": init_data["bot_notify"].last_name,
                "patronymic": init_data["bot_notify"].patronymic,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['alex'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["alex"].id),
                "first_name": init_data["alex"].first_name,
                "last_name": init_data["alex"].last_name,
                "patronymic": init_data["alex"].patronymic,
                "roles": init_data["alex"].roles,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['ivan'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["ivan"].id),
                "first_name": init_data["ivan"].first_name,
                "last_name": init_data["ivan"].last_name,
                "patronymic": init_data["ivan"].patronymic,
                "roles": init_data["ivan"].roles,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['oleg'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["oleg"].id),
                "first_name": init_data["oleg"].first_name,
                "last_name": init_data["oleg"].last_name,
                "patronymic": init_data["oleg"].patronymic,
                "roles": init_data["oleg"].roles,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['efim'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["efim"].id),
                "first_name": init_data["efim"].first_name,
                "last_name": init_data["efim"].last_name,
                "patronymic": init_data["efim"].patronymic,
                "roles": init_data["efim"].roles,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['anya'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["anya"].id),
                "first_name": init_data["anya"].first_name,
                "last_name": init_data["anya"].last_name,
                "patronymic": init_data["anya"].patronymic,
                "roles": init_data["anya"].roles,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['olga'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["olga"].id),
                "first_name": init_data["olga"].first_name,
                "last_name": init_data["olga"].last_name,
                "patronymic": init_data["olga"].patronymic,
                "roles": init_data["olga"].roles,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['artem'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["artem"].id),
                "first_name": init_data["artem"].first_name,
                "last_name": init_data["artem"].last_name,
                "patronymic": init_data["artem"].patronymic,
                "roles": init_data["artem"].roles,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['petr'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["petr"].id),
                "first_name": init_data["petr"].first_name,
                "last_name": init_data["petr"].last_name,
                "patronymic": init_data["petr"].patronymic,
                "roles": init_data["petr"].roles,
            }
        ),
    )
    await redis.set(
        name=f"user:{str(init_data['igor'].id)}",
        value=json.dumps(
            {
                "id": str(init_data["igor"].id),
                "first_name": init_data["igor"].first_name,
                "last_name": init_data["igor"].last_name,
                "patronymic": init_data["igor"].patronymic,
                "roles": init_data["igor"].roles,
            }
        ),
    )
