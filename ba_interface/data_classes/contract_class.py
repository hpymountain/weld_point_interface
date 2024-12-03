from database_object import DatabaseObject
from tokeo.ext.appshare import app

class Contract(DatabaseObject):
    def __init__(self) -> None:
        self.ID = ""
        self.customer = ""
        self.subscription = ""
        self.basic_fee = ""
        self.minutes_included = ""
        self.price_per_extra_minute = ""
        self.data_volume = ""
        self.imsi = ""
        self.terminal_type = ""
    
    def read_from_query_object(self, query_object):
        self.ID = query_object
        self.customer = query_object
        self.subscription = query_object
        self.basic_fee = query_object
        self.minutes_included = query_object
        self.price_per_extra_minute = query_object
        self.data_volume = query_object
        self.imsi = query_object
        self.terminal_type = query_object
        return self
    
    def read_in_db(self, key):
        self.read_from_query_object(app.db.get_one('contracts', key))
        return self
    
    def update_in_db(self, col_list: list[str]=None):
        col_dict = {
            'customer': self.customer,
            'subscription': self.subscription,
            'basic_fee': self.basic_fee,
            'minutes_included': self.minutes_included,
            'price_per_extra_minute': self.price_per_extra_minute,
            'data_volume': self.data_volume,
            'imsi': self.imsi,
            'terminal_type': self.terminal_type
            }
        if col_list is not None:
            col_dict_new = dict(col_dict)
            for col in col_list:
                col_dict_new.update({col: col_dict.get(col)})
            col_dict = col_dict_new
        app.db.update('contracts', self.ID, col_dict)
        return self
    
    def delete_in_db(self):
        app.db.delete('contracts', self.ID)
        return self

def get_all_contracts_in_db(filter=None) -> list[Contract]:
    ret_list: list[Contract] = []
    if filter is not None:
        user_query_list_object = app.db.get_list('customers', filter=filter)
    else:        
        user_query_list_object = app.db.get_list('customers')
    
    for contract in user_query_list_object.items:
        ret_list.append(Contract().read_from_query_object(contract))
    return ret_list
        