

from tortoise import Tortoise


async def dbConnect():
    await Tortoise.init(
        db_url='',
        modules={}
    )
    await Tortoise.generate_schemas()
