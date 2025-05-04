import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from model import User
from service.user import UserServiceV1


async def set_initial_data(session: AsyncSession):
    admin = User(
        password=UserServiceV1().get_password_hash(str(uuid.uuid4())),
        email=str(uuid.uuid4().hex) + "@mail.com",
        first_name=str(uuid.uuid4().hex[:7]),
        last_name=str(uuid.uuid4().hex[:7]),
        is_active=True,
        is_admin=True,
        is_service=False,
    )
    session.add(admin)
    await session.flush()

    service = User(
        password=UserServiceV1().get_password_hash(str(uuid.uuid4())),
        email=str(uuid.uuid4().hex) + "@mail.com",
        first_name=str(uuid.uuid4().hex[:7]),
        last_name=str(uuid.uuid4().hex[:7]),
        is_active=True,
        is_admin=False,
        is_service=True,
    )
    session.add(service)
    await session.flush()

    blocked_service = User(
        password=UserServiceV1().get_password_hash(str(uuid.uuid4())),
        email=str(uuid.uuid4().hex) + "@mail.com",
        first_name=str(uuid.uuid4().hex[:7]),
        last_name=str(uuid.uuid4().hex[:7]),
        is_active=False,
        is_admin=False,
        is_service=True,
    )
    session.add(blocked_service)
    await session.flush()

    return {"admin": admin, "service": service, "blocked_service": blocked_service}
