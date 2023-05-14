from app.models import Task
from core.repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """
    Task repository provides all the database operations for the Task model.
    """

    async def get_by_author_id(
        self, author_id: int
    ) -> list[Task]:
        """
        Get all tasks by author id.

        :param author_id: The author id to match.
        :param join_: The joins to make.
        :return: A list of tasks.
        """
        return await self.model_class.objects.filter(
            task_author_id=author_id
        )
