import docker
from datetime import datetime


class LogEntry:
    def __init__(self, timestamp: str, message: str):
        self.timestamp = timestamp
        self.message = message

    def __str__(self):
        return f"{self.timestamp}: {self.message}"


class ContainerInfo:
    @staticmethod
    def exists(container_id: int) -> bool:
        client = docker.from_env()
        try:
            client.containers.get(str(container_id))
            return True
        except docker.errors.NotFound:
            return False

    @staticmethod
    def get_logs(container_id: int) -> list:
        client = docker.from_env()
        container = client.containers.get(str(container_id))
        if container.status != "running":
            return []
        logs = container.logs().decode("utf-8") if container else ""
        log_entries = []
        for line in logs.splitlines():
            timestamp = datetime.now().isoformat()  # Replace with actual timestamp parsing if available
            log_entries.append(LogEntry(timestamp, line))
        return log_entries
