from abc import ABC, abstractmethod


class Job(ABC):

    @abstractmethod
    def get_data_and_save(self):
        pass

    @abstractmethod
    def return_data(self):
        pass

    @abstractmethod
    def salary_to_rubles(self):
        pass

    @abstractmethod
    def return_top_vacancies(self):
        pass
