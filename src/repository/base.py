from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import Select, and_, func, select
from sqlalchemy.orm import InstrumentedAttribute, joinedload, selectinload

from core.database import DatabaseHelper, db_conn
from model.base import Base


T = TypeVar("T", bound=Base)


class BaseRepo(Generic[T]):
    model: type[T]

    def __init__(self, connection: DatabaseHelper = db_conn):
        self._db = connection

    async def all(
        self,
        joined_load: list[InstrumentedAttribute] | None = None,
        select_in_load: list[InstrumentedAttribute] | None = None,
        order_by: list[InstrumentedAttribute] | None = None,
    ) -> Sequence[T]:
        """
        Возвращает список объектов модели.

        Args:
            joined_load: Список отношений для использования joinedload.
            (many-to-one, one-to-one)
            select_in_load: Список отношений для использования selectinload.
            (one-to-many, many-to-many)
            order_by: Список атрибутов для сортировки результата. По умолчанию = None.

        Returns:
            Sequence[ModelObject]: Список объектов модели.
        """
        statement = self.get_statement(
            joined_load=joined_load,
            select_in_load=select_in_load,
            order_by=order_by,
        )
        async with self._db.get_session() as session:
            result = await session.scalars(statement=statement)
            return result.all()

    async def count(
        self,
        excludes: dict[InstrumentedAttribute, Any] | None = None,
        **filters,
    ) -> int:
        """
        Возвращает количество объектов модели, удовлетворяющих заданным фильтрам.

        Args:
            excludes: Словарь атрибутов и значений для исключения из результата.
            **filters: Именованные аргументы для добавления в фильтр запроса.

        Returns:
            int: Количество записей модели.
        """
        statement = self.get_statement(
            count=True,
            excludes=excludes,
            **filters,
        )
        async with self._db.get_session() as session:
            result = await session.scalar(statement=statement)
            return result

    async def exists(
        self,
        excludes: dict[InstrumentedAttribute, Any] | None = None,
        **filters,
    ) -> bool:
        """
        Проверяет наличие записей модели, удовлетворяющих заданным фильтрам.

        Args:
            excludes: Словарь атрибутов и значений для исключения из результата.
            **filters: Именованные аргументы для добавления в фильтр запроса.

        Returns:
            bool: True, если есть записи модели, иначе False.
        """
        subquery = self.get_statement(excludes=excludes, **filters)
        statement = select(1).where(subquery.exists())
        async with self._db.get_session() as session:
            result = await session.scalar(statement=statement)
            return bool(result)

    async def filter(
        self,
        excludes: dict[InstrumentedAttribute, Any] | None = None,
        joined_load: list[InstrumentedAttribute] | None = None,
        select_in_load: list[InstrumentedAttribute] | None = None,
        order_by: list[InstrumentedAttribute] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        **filters,
    ) -> Sequence[T]:
        """
        Возвращает список записей модели, удовлетворяющих заданным фильтрам.

        Args:
            excludes: Словарь атрибутов и значений для исключения из результата.
            joined_load: Список отношений для использования joinedload.
            (many-to-one, one-to-one)
            select_in_load: Список отношений для использования selectinload.
            (one-to-many, many-to-many)
            order_by: Список атрибутов для сортировки результата.
            limit: Максимальное количество результатов.
            offset: Порядковый номер начального результата (сдвиг).
            **filters: Именованные аргументы для добавления в фильтр запроса.

        Returns:
            Sequence[T]: Список записей модели.
        """

        statement = self.get_statement(
            excludes=excludes,
            joined_load=joined_load,
            select_in_load=select_in_load,
            order_by=order_by,
            limit=limit,
            offset=offset,
            **filters,
        )
        async with self._db.get_session() as session:
            result = await session.scalars(statement=statement)
            return result.all()

    async def get(
        self,
        excludes: dict[InstrumentedAttribute, Any] | None = None,
        joined_load: list[InstrumentedAttribute] | None = None,
        select_in_load: list[InstrumentedAttribute] | None = None,
        **filters,
    ) -> T:
        """
        Возвращает единственную запись модели, удовлетворяющую заданным фильтрам.

        Args:
            excludes: Словарь атрибутов и значений для исключения из результата.
            joined_load: Список отношений для использования joinedload.
            (many-to-one, one-to-one)
            select_in_load: Список отношений для использования selectinload.
            (one-to-many, many-to-many)
            **filters: Именованные аргументы для добавления в фильтр запроса.

        Returns:
            T: Единственная запись модели, удовлетворяющая заданным фильтрам.

        Raises:
            NoResultFound: Если не найдена единственная запись
            MultipleResultsFound: Если найдено более одной записи.
        """
        statement = self.get_statement(
            excludes=excludes,
            joined_load=joined_load,
            select_in_load=select_in_load,
            **filters,
        )
        async with self._db.get_session() as session:
            result = await session.execute(statement=statement)
            return result.scalar_one()

    async def get_or_none(self, **filters):
        """
        Ищет единственную запись модели по заданным фильтрам и возвращает ее, если она
        существует, или None, если не найдена.

        Args:
            **filters: Набор ключевых слов для поиска экземпляра модели.

        Returns:
            ModelObject | None: Первая запись модели, удовлетворяющая фильтрам,
            или None если не найдено ни одной.

        Raises:
            MultipleResultsFound: Если найдено более одной записи.
        """
        statement = self.get_statement(**filters)
        async with self._db.get_session() as session:
            result = await session.execute(statement=statement)
            return result.scalar_one_or_none()

    async def find(
        self,
        excludes: dict[InstrumentedAttribute, Any] | None = None,
        joined_load: list[InstrumentedAttribute] | None = None,
        select_in_load: list[InstrumentedAttribute] | None = None,
        order_by: list[InstrumentedAttribute] | None = None,
        **filters,
    ) -> T | None:
        """
        Возвращает первую запись модели, удовлетворяющую заданным фильтрам,
        или None, если не найдено ни одной.

        Args:
            excludes: Словарь атрибутов и значений для исключения из результата.
            joined_load: Список отношений для использования joinedload.
            (many-to-one, one-to-one)
            select_in_load: Список отношений для использования selectinload.
            (one-to-many, many-to-many)
            order_by: Список атрибутов для сортировки результата.
            **filters: Именованные аргументы для добавления в фильтр запроса.

        Returns:
            T | None: Первая запись модели, удовлетворяющая заданным фильтрам,
            или None, если не найдено ни одной.
        """
        statement = self.get_statement(
            excludes=excludes,
            joined_load=joined_load,
            select_in_load=select_in_load,
            order_by=order_by,
            **filters,
        )
        async with self._db.get_session() as session:
            result = await session.scalar(statement=statement)
            return result

    async def create(self, **model_data) -> T:
        """
        Создает новую запись модели и сохраняет ее в базе данных.

        Args:
            **model_data: Атрибуты и значения нового экземпляра модели.
        Returns:
            T: Созданная и сохраненная запись модели.
        """
        instance = self.model(**model_data)
        async with self._db.get_session() as session, session.begin():
            session.add(instance)
            return instance

    async def update(self, instance: T, **model_data) -> T:
        """
        Обновляет существующую запись модели и сохраняет изменения в базе данных.

        Args:
            instance: Экземпляр модели для обновления.
            **model_data: Атрибуты и значения для обновления экземпляра модели.

        Returns:
            ModelObject: Обновленный экземпляр модели.
        """
        for key, value in model_data.items():
            setattr(instance, key, value)
        async with self._db.get_session() as session, session.begin():
            session.add(instance)
            return instance

    async def delete(self, instance: T) -> None:
        """
        Удаляет существующую запись модели из базы данных.

        Args:
            instance: Экземпляр модели для удаления.
        """
        async with self._db.get_session() as session, session.begin():
            await session.delete(instance)

    async def get_or_create(self, filters: list[str], **model_data) -> tuple[T, bool]:
        """
        Ищет существующую запись модели по заданным фильтрам или создаёт новую запись,
        если не найдена.

        Args:
            filters: Список ключевых слов для поиска экземпляра модели.
            **model_data: Атрибуты и значения нового экземпляра модели.

        Returns:
            tuple[T, bool]: Кортеж: созданный или найденный экземпляр
            модели и флаг, указывающий, была ли запись
            создана (True) или найдена (False).
        """
        created = True
        get_filters = {
            filter_: model_data.get(filter_) for filter_ in filters
        } or model_data
        if instance := await self.find(**get_filters):
            created = False
            return instance, created
        return await self.create(**model_data), created

    async def update_or_create(
        self, filters: dict[str, Any], **model_data
    ) -> tuple[T, bool]:
        """
        Обновляет существующую запись модели по заданным фильтрам или создаёт новую
        запись, если не найдена.

        Parameters:
            filters (dict[str, Any]): Словарь ключевых слов и значений для поиска
            экземпляра модели.
            **model_data: Атрибуты и значения нового экземпляра модели.

        Returns:
            tuple[ModelObject, bool]: Пару значения: обновленный или созданный экземпляр
            модели и флаг, указывающий, была ли запись
            создана (True) или найдена (False)
        """
        created = True
        if instance := await self.get_or_none(**filters):
            created = False
            return (
                await self.update(instance=instance, **model_data),
                created,
            )
        model_data.update(filters)
        return await self.create(**model_data), created

    def _get_filters(self, filters: dict):
        filter_conditions = []
        for key, value in filters.items():
            column = getattr(self.model, key)
            if not isinstance(value, dict):
                value = {FilterCondition.EXACT: value}
            for operator, operand in value.items():
                condition = FilterCondition.get_by_expr(operator)
                if condition:
                    filter_conditions.append(condition(column, operand))
        return (
            and_(*filter_conditions)
            if len(filter_conditions) > 1
            else filter_conditions[0]
        )

    def get_statement(
        self,
        excludes: dict[InstrumentedAttribute, Any] | None = None,
        joined_load: list[InstrumentedAttribute] | None = None,  # type: ignore
        select_in_load: list[InstrumentedAttribute] | None = None,  # type: ignore
        order_by: list[InstrumentedAttribute] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        count: bool = False,
        **filters,
    ) -> Select:
        statement = (
            select(self.model)
            if not count
            else select(func.count(1)).select_from(self.model)
        )
        if filters:
            filter_query = self._get_filters(filters)
            statement = statement.filter(filter_query)
        if excludes:
            for field, value in excludes.items():
                statement = statement.where(field != value)
        if joined_load:
            statement = statement.options(*[joinedload(item) for item in joined_load])
        if select_in_load:
            statement = statement.options(
                *[selectinload(item) for item in select_in_load]
            )
        if offset is not None:
            statement = statement.offset(offset)
        if limit is not None:
            statement = statement.limit(limit)
        if not count:
            order_by = order_by if order_by is not None else self.model.ordering()
            statement = statement.order_by(*order_by)
        return statement


class FilterCondition:
    EXACT = "exact"
    NOT_EXACT = "not_exact"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    LIKE = "like"
    ILIKE = "ilike"
    BETWEEN = "between"
    ANY = "any"

    @classmethod
    def get_by_expr(cls, expr: str = EXACT):
        conditions_map = {
            cls.EXACT: lambda column, value: column == value,
            cls.NOT_EXACT: lambda column, value: column != value,
            cls.GT: lambda column, value: column > value,
            cls.GTE: lambda column, value: column >= value,
            cls.LT: lambda column, value: column < value,
            cls.LTE: lambda column, value: column <= value,
            cls.IN: lambda column, value: column.in_(value),
            cls.NOT_IN: lambda column, value: column.not_in(value),
            cls.LIKE: lambda column, value: column.like(f"%{value}%"),
            cls.ILIKE: lambda column, value: column.ilike(f"%{value}%"),
            cls.BETWEEN: lambda column, value: column.between(*value),
            cls.ANY: lambda column, value: column.any(value),
        }
        return conditions_map.get(expr)

    @classmethod
    def get_filter(cls, value: Any, expr: str = EXACT):
        return {expr: value}
