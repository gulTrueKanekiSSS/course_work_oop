class Vacancie:

    def __init__(self, search_request, platform, amount, name, salary, url, requirement):
        super().__init__(search_request, platform, amount)
        self.name = name
        self.salary = salary
        self.url = url
        self.requirement = requirement