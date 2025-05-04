import uuid

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from model import Message, MessageStatus, Room, UserRoom
from repository.user import User
from schema.enum import MessageStatusChoices


def create_user(
    first_name: str = "",
    last_name: str = "",
    patronymic: str = "",
    id: uuid.UUID = None,
    avatar: str = "",
    roles: list[str] = None,
    is_admin: bool = False,
    is_service: bool = False,
    description: str = "",
    is_anonymous: bool = False,
):
    return User(
        id=id or uuid.uuid4(),
        first_name=first_name or uuid.uuid4().hex[:6] if not is_anonymous else "",
        last_name=last_name or uuid.uuid4().hex[:6] if not is_anonymous else "",
        patronymic=patronymic or uuid.uuid4().hex[:6] if not is_anonymous else "",
        avatar=avatar,
        roles=roles or ["Ученик"],
        is_admin=is_admin,
        is_service=is_service,
        description=description or uuid.uuid4().hex[:6] if not is_anonymous else "",
        is_anonymous=is_anonymous,
    )


async def create_users(num: int) -> list[User]:
    return [create_user() for _ in range(num)]


async def create_room(
    session: AsyncSession,
    users: list[User],
    title: str = "",
    type: str = "private",
    order_group: int = 99,
    has_message: bool = False,
    avatar: str = "",
    created_at: datetime = None,
    updated_at: datetime = None,
    last_update: datetime = None,
):
    if len(users) != 2:
        raise ValueError("Должно быть два пользователя в комнате")
    created_at = created_at or datetime.now()
    updated_at = updated_at or datetime.now()
    last_update = last_update or datetime.now()
    if not title:
        title = f"{users[0].full_name} - {users[1].full_name}"
    room = Room(
        title=title,
        type=type,
        order_group=order_group,
        has_message=has_message,
        avatar=avatar,
        created_at=created_at,
        updated_at=updated_at,
        last_update=last_update,
    )
    session.add(room)
    await session.flush()

    for user in users:
        user_room = UserRoom(user_id=user.id, room_id=room.id)
        session.add(user_room)

    await session.flush()
    return room


async def create_message(
    session: AsyncSession,
    sender_id: uuid.UUID,
    receiver_id: uuid.UUID,
    room_id: uuid.UUID,
    mark_read: bool = False,
    text: str = "test",
    message_before_id: uuid.UUID = None,
    is_deleted=False,
    is_edited=False,
    created_at: datetime = None,
    updated_at: datetime = None,
):
    read = MessageStatusChoices.read.value
    unread = MessageStatusChoices.unread.value
    message = Message(
        user_id=sender_id,
        room_id=room_id,
        text=text,
        message_before_id=message_before_id,
        created_at=created_at or datetime.now(),
        updated_at=updated_at or datetime.now(),
        is_deleted=is_deleted,
        is_edited=is_edited,
    )
    session.add(message)
    await session.flush()
    session.add(MessageStatus(message_id=message.id, status=read, user_id=sender_id))
    session.add(
        MessageStatus(
            message_id=message.id,
            status=read if mark_read else unread,
            user_id=receiver_id,
        )
    )
    await session.flush()
    return message
