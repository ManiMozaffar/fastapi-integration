from typing import Any, Generic, Type, TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Base
from core.orm.models import AbstractModel

ModelType = TypeVar("ModelType", bound=Union[AbstractModel, Base])


class BaseRepository(Generic[ModelType]):
    """Base class for data repositories."""

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.session = db_session
        self.model_class: Type[ModelType] = model

    async def filter_and_count(
        self,
        order_by: str = None,
        limit: int = None,
        skip: int = None,
        **kwargs
    ):
        """
        Returns a dictionary containing filtered results and its counts.

        :param order_by: Order by attribute to sort results
        :param limit: Limit and slice the results from db
        :param skip: Skip index results from db

        :return: The created model instance.
        """
        results = self._order_by(
                order_by=order_by,
                limit=limit,
                skip=skip,
                **kwargs
        )
        count = self._count(
            order_by=order_by,
            limit=limit,
            skip=skip,
            **kwargs
        )
        return dict(
            results=await results,
            count=await count
        )

    async def create(self, **kwargs) -> ModelType:
        """
        Creates the model instance.

        :param attributes: The attributes to create the model with.
        :return: The created model instance.
        """
        return await self.model_class.objects.create(
            db_session=self.session,
            **kwargs
        )

    async def update(
        self,
        update_data: dict,
        skip: int = None,
        limit: int = None,
        **kwargs
    ):
        """
        Returns a list of records based on pagination params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :param join_: The joins to make.
        :return: A list of records.
        """

        return await self.model_class.objects.update(
            db_session=self.session,
            skip=skip,
            limit=limit,
            update_data=update_data,
            **kwargs
        )

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        **kwargs: dict
    ) -> list[ModelType]:
        """
        Returns a list of model instances.

        :param skip: The number of records to skip.
        :param limit: The number of record to return.
        :param join_: The joins to make.
        :return: A list of model instances.
        """
        return await self.model_class.objects.filter(
            limit=limit,
            skip=skip,
            **kwargs
        ).execute(
            db_session=self.session
        )

    async def get_by(
        self,
        field: str,
        value: Any,
        skip: int = None,
        limit: int = None
    ) -> ModelType:
        """
        Returns the model instance matching the field and value.

        :param field: The field to match.
        :param value: The value to match.
        :param join_: The joins to make.
        :return: The model instance.
        """
        filter_args = {
            field: value
        }
        return await self.model_class.objects.filter(
            limit=limit,
            skip=skip,
            **filter_args
        ).execute(
            db_session=self.session
        )

    async def get(
        self,
        skip: int = None,
        limit: int = None,
        **kwargs
    ) -> ModelType:
        """
        Returns the model instance matching the field and value.

        :param field: The field to match.
        :param value: The value to match.
        :param join_: The joins to make.
        :return: The model instance.
        """
        return await self.model_class.objects.get(
            db_session=self.session,
            limit=limit,
            skip=skip,
            **kwargs
        )

    async def delete(self, **kwargs: dict) -> None:
        """
        Deletes the model.

        :param kwargs: The query to delete.
        :return: None
        """
        return await self.model_class.objects.delete(
            db_session=self.session,
            **kwargs
        )

    async def _count(
            self,
            order_by: str = None,
            limit: int = None,
            skip: int = None,
            **kwargs: dict
    ) -> int:
        """
        Returns the count of the records.

        :param kwargs: The query that needs to be counted.
        """
        return await self.model_class.objects.filter(
            order_by=order_by,
            limit=limit,
            skip=skip,
            **kwargs
        ).count(
            db_session=self.session
        )

    async def _order_by(
        self,
        order_by: str = None,
        limit: int = None,
        skip: int = None,
        **kwargs
    ):
        """
        Returns the query sorted by the given column.

        :param query: The query to sort.
        :param sort_by: The column to sort by.
        :param order: The order to sort by.
        :param model: The model to sort.
        :return: The sorted query.
        """
        return await self.model_class.objects.filter(
            order_by=order_by,
            limit=limit,
            skip=skip,
            **kwargs
        ).execute(
            db_session=self.session
        )
