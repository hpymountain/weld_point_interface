from abc import ABC, abstractmethod

class DatabaseObject(ABC):
    @abstractmethod
    def read_from_query_object(self, query_object):
        return self
    
    @abstractmethod
    def read_in_db(self, key):
        return self
    
    @abstractmethod
    def update_in_db(self):
        return self
    
    @abstractmethod
    def delete_in_db(self):
        return self
        
    