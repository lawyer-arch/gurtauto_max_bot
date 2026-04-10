from database.session import async_session


class DBSessionMiddleware:
    async def __call__(self, handler, event, data):
        async with async_session() as session:
            data["session"] = session
            return await handler(event, data)
