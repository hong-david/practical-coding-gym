class SearchService:
    def add_document(self, doc_id: str, title: str, body: str, tags=None) -> None:
        raise NotImplementedError
    def search(self, query: str, tags=None, limit: int = 10, offset: int = 0) -> list[dict]:
        raise NotImplementedError
