import asyncio

from getpass import getpass

from schema.user import UserInputSchema
from service.user import UserServiceV1


async def main():
    email = input("Email: ")
    if len(email) < 5:
        raise ValueError("Email length must be greater than 5")
    if "@" not in email:
        raise ValueError("Symbol '@' must be in email")
    password = getpass("Password: ")
    if len(password) < 8:
        raise ValueError("Password length must be greater than 7")
    confirmed_password = getpass("Enter password again: ")
    if password != confirmed_password:
        raise ValueError("Passwords don't match")

    await UserServiceV1().create(
        UserInputSchema(email=email, password=password),
        is_admin=True,
    )
    print("Success!")


if __name__ == "__main__":
    asyncio.run(main())
