import asyncio
from django.db import models
from adrf import serializers as aserializers


# Как ListSerializer, но запускает сразу все таски to_representation, а не ждет поочередно каждую
class ParallelListSerializer(aserializers.ListSerializer):
    async def ato_representation(self, data):
        if isinstance(data, models.Manager):
            data = data.all()

        tasks = []
        if isinstance(data, models.query.QuerySet):
            tasks = [self.child.ato_representation(item) async for item in data]
        else:
            tasks = [self.child.ato_representation(item) for item in data]

        return await asyncio.gather(*tasks)
