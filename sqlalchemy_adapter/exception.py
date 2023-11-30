class SessionNotInitializedError(Exception):
    def __init__(self) -> None:
        super().__init__("Session not initialized")
