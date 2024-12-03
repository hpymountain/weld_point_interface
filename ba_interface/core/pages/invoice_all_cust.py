from tokeo.ext.appshare import app
from ba_interface.core import consts
from ba_interface.core.pages import layout

ui = app.nicegui.ui
ux = app.nicegui.ux

@ui.page('/invoice-all')
def page_invoice_all():
    ux.h1('Generate invoices')
    contracts = app.db.get_list('contracts', page=1, perPage=50, filter='', sort='customer.surname,customer.forename,terminal_type', q=dict(expand='customer'))
    for c in contracts.items:
        ux.p(f'{c.expand["customer"].surname}, {c.expand["customer"].forename}, {c.id}')
        ui.navigate.to(f'/invoice/create/{c.id}/?approve=0', new_tab=True)

