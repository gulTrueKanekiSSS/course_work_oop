class Vacancie:

    def __init__(self, search_request: str, platform: str, amount: int, name: str, salary: int, url: str,
                 requirement: str):
        super().__init__(search_request, platform, amount)
        self.name: str = name
        self.salary: int = salary
        self.url: str = url
        self.requirement: str = requirement
