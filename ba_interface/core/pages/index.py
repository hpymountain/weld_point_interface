from tokeo.ext.appshare import app
from ba_interface.core import consts
from ba_interface.core.pages import layout

ui = app.nicegui.ui
ux = app.nicegui.ux


@app.nicegui.fastapi_app.get('/api')
async def get_api():
    return {'msg': 'json api result'}


# @ui.page('/show-services-trackings')
# def show_users():
#     ui.label('Show services trackings!').classes('text-2xl m-2')
#     customers = app.db.get_list('customers', page=1, perPage=20, filter='', sort='created', cache=False)
#     for customer in customers.items:
#         with ux.ul().classes("divide-y divide-gray-100"):
#             with ux.li().classes("flex justify-between gap-x-6 py-5"):
#                 with ux.div().classes("flex min-w-0 gap-x-4"):
#                     ux.h2(f'{customer.surname}, {customer.forename}').classes("text-sm font-semibold leading-6 text-gray-900")
#                     tracked = app.db.get_list('services_tracked', page=1, perPage=20, filter=f'account="{customer.id}"', sort='created', cache=False)
#                     for service in tracked.items:
#                         with ux.div().classes("min-w-0 flex-auto"):
#                             ux.p(service.service).classes("text-sm font-semibold leading-6 text-gray-900")
#                             ux.p(f'{service.duration} min').classes("mt-1 truncate text-xs leading-5 text-gray-500")


@ui.page('/show-customers-and-contracts')
def show_customers_and_contracts():
    with layout.page_layout():
        ui.label('Übersicht Kunden und deren Verträge!').classes('text-2xl m-2')
        customers = app.db.get_list('customers', page=1, perPage=50, filter='', sort='surname,forename', cache=False)
        for customer in customers.items:
            contracts = app.db.get_list('contracts', page=1, perPage=50, filter=f'customer="{customer.id}"')
            with ux.ul().classes("divide-y divide-gray-100"):
                with ux.li().classes("flex justify-between gap-x-6 py-5"):
                    with ux.div().classes("flex min-w-0 gap-x-4"):
                        with ux.div().classes("min-w-0 flex-auto"):
                            ux.p(customer.surname).classes("text-sm font-semibold leading-6 text-gray-900")
                            ux.p(customer.forename).classes("mt-1 truncate text-xs leading-5 text-gray-500")
                            ux.p('Verträge')
                            for contract in contracts.items:
                                ux.p(f'{contract.subscription}, {contract.terminal_type}')
                                # Nicegui Doc lesen, entsprechende funktionen finden
                                ui.link('Ansicht Rechnung', f'/invoice/create/{contract.id}')
                                ui.button('Ansicht Rechnung', on_click=lambda invoice_url=f'/invoice/create/{contract.id}': ui.navigate.to(invoice_url, new_tab=True))


# @ui.page('/manage-contracts')
# def manage_contracts():
#     contracts = app.db.get_list('contracts', page=1, perPage=50, filter='')
#     for contract in contracts.items:
#         app.db.delete('contracts', contract.id)





def default():
    with layout.page_layout():
        ux.h1('This is the homepage!').classes('w-full mt-10')
        #ui.link('Übersicht der User', '/show-users').classes('block')
        #ui.link('Übersicht Tracked Services', '/show-services-trackings').classes('block')
        #ui.link('Übersicht Justus', '/show-justus')
        ui.link('Erstelle Rechnungen', '/show-customers-and-contracts').classes('block')
        ui.link('Session-Simulation', '/session/new').classes('block')
        ui.link('Invoice all customers', '/invoice-all').classes('block')
        ui.link('Manage contracts', '/manage-contracts').classes('block')

