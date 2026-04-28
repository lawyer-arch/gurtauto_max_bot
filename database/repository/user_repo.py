from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import UserMax


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, user_id, username, first_name):

        result = await self.session.execute(
            select(UserMax).where(UserMax.user_id == user_id)
        )
        user = result.scalar_one_or_none()

        if user:
            return user

        user = UserMax(
            user_id=user_id,
            username=username,
            first_name=first_name
        )

        self.session.add(user)
        await self.session.commit()

        return user
