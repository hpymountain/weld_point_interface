from tokeo.ext.appshare import app
from database_object import DatabaseObject
from contract_class import Contract


class User(DatabaseObject):
    def __init__(self):
        self.ID: str = "" 
        self.forename: str = ""
        self.surname: str = ""
        self.address: str = ""
        self.zipcode: str = ""
        self.city: str = ""
        self.email: str = ""
        self.contracts: list[Contract] = []
    
    def read_from_query_object(self, query_object):
        self.ID = query_object.id
        self.forename = query_object.forename
        self.surname = query_object.surname
        self.address = query_object.address
        self.zipcode = query_object.zipcode
        self.city = query_object.city
        self.email = query_object.email
        self.fetch_all_contracts()
        return self
    
    def fetch_all_contracts(self):
        all_contracts = app.db.get_list('contracts')
        for contract in all_contracts:
            if contract.customer == self.ID:
                self.contracts.append(Contract.read_from_query_object(contract))
        return self
       
    def read_in_db(self, key:str):
        self.read_from_query_object(app.db.get_one('customers', key))
        return self
    
    def update_in_db(self, col_list: list[str]=None):
        col_dict = {
            'forename': self.forename,
            'surname': self.surname,
            'address': self.address,
            'zipcode': self.zipcode,
            'city': self.city,
            'email': self.email
            }
        if col_list is not None:
            col_dict_new = dict(col_dict)
            for col in col_list:
                col_dict_new.update({col: col_dict.get(col)})
            col_dict = col_dict_new
        app.db.update('customers', self.ID, col_dict)
        return self
        
    def delete_in_db(self):
        app.db.delete('customers', self.ID)
        return self


def read_user_list_from_db(filter = None) -> list[User]:
    ret_list: list[User] = []
    if filter is not None:
        user_query_list_object = app.db.get_list('customers', filter=filter)
    else:        
        user_query_list_object = app.db.get_list('customers')
    
    for account in user_query_list_object.items:
        ret_list.append(User().read_from_query_object(account))
    return ret_list