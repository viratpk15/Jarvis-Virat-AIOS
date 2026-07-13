from app.Memory.storage import storage


class MemoryManager:
    @staticmethod
    def get_conversation(session_id: str):
        return storage.get_memory(session_id)


memory_manager = MemoryManager()
