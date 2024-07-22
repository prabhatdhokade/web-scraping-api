from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    async def notify(self, message: str):
        pass


class ConsoleNotification(NotificationStrategy):
    async def notify(self, message: str):
        print(message)
