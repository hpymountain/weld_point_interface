from tokeo.ext.appshare import app
from ba_interface.core import consts
import asyncio

ui = app.nicegui.ui
ux = app.nicegui.ux


@ui.page('/invoice/create/{contract_id}')
def page_invoice(contract_id, approve: int = 1):

    ux.h1(f'Show invoice for contract: {contract_id}').classes('text-2xl m-2')
    contract = app.db.get_one('contracts', contract_id)
    customer = app.db.get_one('customers', contract.customer)
    sum_sessions_per_contract = app.db.get_one('sum_sessions_per_contract', contract.id)
    sessions = app.db.get_list('sessions', page=1, perPage=10000, filter=f'contract="{contract.id}"', sort='created,service_type', cache=False)

    ux.p(customer.forename)
    ux.p(customer.surname)
    ux.p(customer.address)
    ux.p(customer.zipcode)
    ux.p(customer.city)
    ux.p(customer.email)
    ux.p('---')
    ux.p(f'{contract.subscription} {consts.SUBSCRIPTIONS[contract.subscription]}')
    ux.p(f'{contract.basic_fee} EUR')
    ux.p(f'{contract.minutes_included} Minuten enthalten')
    ux.p(contract.price_per_extra_minute)
    ux.p(f'{contract.data_volume} KBytes / {contract.data_volume / 1000 / 1000} GB')
    ux.p(contract.imsi)
    ux.p(contract.terminal_type)
    ux.p('---')
    ux.p('Usage')
    ux.p(f'{sum_sessions_per_contract.call_duration_sum} gesamt Minuten Call')
    ux.p(f'{sum_sessions_per_contract.data_duration_sum} gesamt Minuten Daten genutzt')
    ux.p(f'{sum_sessions_per_contract.data_volume_sum} gesamt KBytes(!) Daten genutzt')
    ux.p('---')
    ux.p('Kosten')
    diff_call_minutes = sum_sessions_per_contract.call_duration_sum - contract.minutes_included
    costs_call_extra_minutes_sum = diff_call_minutes * contract.price_per_extra_minute if diff_call_minutes > 0 else 0
    diff_data_volume = contract.data_volume - sum_sessions_per_contract.data_volume_sum
    ux.p(f'Extra zu bezahlende Minuten Call: {diff_call_minutes if diff_call_minutes > 0 else 0}')
    ux.p(f'Extra Minuten Kosten: {costs_call_extra_minutes_sum}')
    ux.p(f'Restvolumen Data: {diff_data_volume} KBytes(!) / {diff_data_volume / 1000 / 1000} GB')
    ux.p('---')
    ux.p('Rechnungssumme')
    costs_sum = contract.basic_fee + costs_call_extra_minutes_sum
    costs_sum_vat = costs_sum / 119 * 19
    ux.p(f'Kosten: {costs_sum} EUR')
    ux.p(f'Enthaltene Mehrwertsteuer 19%: {costs_sum_vat} EUR')
    ux.p('---')
    ux.p('Session Verlauf')
    for s in sessions.items:
        ux.p(f'{s.service_type}, {s.created}, {s.duration}, {s.ran_type}, {s.signal_quality}, {s.cur_throughput}, {s.data_volume}')
    ux.p('---')


    def clear_sessions():
        for s in sessions.items:
            app.db.delete('sessions', s.id)


    async def send_and_clear():
        ui.notify(f'Send email to {customer.email}')
        await asyncio.sleep(3)
        clear_sessions()
        ui.navigate.to('/invoice/done')

    if approve != 0:
        ui.button('Send and clear', on_click=lambda: send_and_clear())
    else:
        clear_sessions()
        ux.p('Invoice was sent and session are cleared. Close windows.')


@ui.page('/invoice/done')
def page_invoice_done():
    ux.h1('Invoice successfully sent and cleared').classes('text-2xl m-2')
    ux.p('Please close this window')

