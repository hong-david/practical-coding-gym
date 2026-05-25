class MessageBoard:
    def create_user(self, username: str) -> dict:
        raise NotImplementedError
    def create_post(self, user_id: int, title: str, body: str) -> dict:
        raise NotImplementedError
    def list_posts(self, limit: int = 20, offset: int = 0) -> list[dict]:
        raise NotImplementedError
    def add_comment(self, user_id: int, post_id: int, body: str) -> dict:
        raise NotImplementedError
    def delete_post(self, user_id: int, post_id: int) -> bool:
        raise NotImplementedError
    def delete_comment(self, user_id: int, comment_id: int) -> bool:
        raise NotImplementedError
