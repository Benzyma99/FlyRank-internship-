from app.repositories.interface import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def get_all(self):
        return self.tasks

    def get_by_id(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def create(self, title: str):
        task = {
            "id": self.next_id,
            "title": title,
            "done": False,
        }

        self.tasks.append(task)
        self.next_id += 1

        return task

    def update(self, task_id: int, title: str, done: bool):
        task = self.get_by_id(task_id)

        if task is None:
            return None

        task["title"] = title
        task["done"] = done

        return task

    def delete(self, task_id: int):
        task = self.get_by_id(task_id)

        if task is None:
            return False

        self.tasks.remove(task)
        return True