import abc


class Abstract_profile(abc.ABC):

    @abc.abstractmethod
    def add_dependency(self, dependency_name: str, dependency_version: str = ''):
        pass

    @abc.abstractmethod
    def remove_dependency(self, dependency_name: str):
        pass

    @staticmethod
    @abc.abstractmethod
    def create_tmp_profile(build_type):
        pass

    @abc.abstractmethod
    def init_profile(self):
        pass
