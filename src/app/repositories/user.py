from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_username(
        self, username: str
    ) -> User | None:
        """
        Get user by username.

        :param username: Username.
        :param join_: Join relations.
        :return: User.
        """
        return await self.get(
            username__iexact=username, limit=1
        )

    async def get_by_email(
        self, email: str
    ) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :return: User.
        """
        return await self.get(
            email__iexact=email, limit=1
        )

    async def _join_tasks(self, query: Select) -> Select:
        """
        Join tasks.

        :param query: Query.
        :return: Query.
        """
        return query.options(joinedload(User.tasks)).execution_options(
            contains_joined_collection=True
        )
