from tokeo.ext.appshare import app
from ba_interface.core import consts
from ba_interface.core.pages import layout
import asyncio
import random
import math

ui = app.nicegui.ui
ux = app.nicegui.ux


@ui.page('/session/new')
def page_session_new():

    form_values = dict(
        contract_id='',
        terminal_type='',
        ran_type='',
        signal_quality=None,
        cur_throughput=None,
        service_type='',
        duration=0,
        sim_duration=1,
    )


    def contract_select_on_change(e):
        form_values['contract_id'] = e.value
        form_values['terminal_type'] = app.db.get_one('contracts', form_values['contract_id']).terminal_type
        network_random_change()


    def contract_selection():
        contracts = app.db.get_list('contracts', page=1, perPage=50, filter='', sort='customer.surname,customer.forename,terminal_type', q=dict(expand='customer'))
        contract_select_options = dict()
        for c in contracts.items:
            contract_select_options[c.id] = f'{c.expand["customer"].surname}, {c.expand["customer"].forename}, {consts.TERMINAL_TYPES[c.terminal_type]["desc"]}'
        ui.select(
            label='Kunde und Vertrag:',
            options=contract_select_options,
            on_change=lambda e: contract_select_on_change(e),
        ).classes('w-full')


    def network_random_change():
        if form_values['contract_id'] == '':
            return
        ran_type_rnd = random.randint(0,consts.TERMINAL_TYPES[form_values['terminal_type']]['max_ran_type_idx'])
        form_values['ran_type'] = list(consts.RAN_TYPES.keys())[ran_type_rnd]
        signal_quality_rnd = random.randint(0,3)
        form_values['signal_quality'] = list(consts.SIGNAL_QUALITIES.keys())[signal_quality_rnd]
        form_values['cur_throughput'] = form_values['signal_quality'] * consts.RAN_TYPES[form_values['ran_type']]['kbyte_sec']
        network_information.refresh()
        service_type_selection.refresh()


    @ui.refreshable
    def network_information():
        ran_type_desc = consts.RAN_TYPES[form_values['ran_type']]['desc'] if form_values['ran_type'] != '' else ''
        signal_quality_desc = consts.SIGNAL_QUALITIES[form_values['signal_quality']] if form_values['signal_quality'] is not None else ''
        max_throughput_desc = consts.RAN_TYPES[form_values['ran_type']]['max_throughput_desc'] if form_values['ran_type'] else ''
        cur_throughput_desc = f'{form_values["cur_throughput"]*8/1000} Mbit/s' if form_values['cur_throughput'] is not None else ''
        network_desc = f'{ran_type_desc}, Signal {signal_quality_desc}, {max_throughput_desc}, Cur {cur_throughput_desc}' if ran_type_desc != '' else ''
        ui.label(f'Network: {network_desc}').classes('w-full mt-8')


    def service_type_select_on_change(e):
        form_values['service_type'] = e.value


    @ui.refreshable
    def service_type_selection():
        form_values['service_type'] = ''
        service_type_select_options = dict()
        if form_values['cur_throughput'] is not None:
            for service_type in consts.SERVICE_TYPES:
                if consts.SERVICE_TYPES[service_type]['min_throughput_kbytes_per_sec'] <= form_values['cur_throughput']:
                    service_type_select_options[service_type] = consts.SERVICE_TYPES[service_type]['desc']
        ui.select(
            label='Service type:',
            options=service_type_select_options,
            on_change=lambda e: service_type_select_on_change(e),
        ).classes('w-full max-w-96 mt-8')


    def duration_input_on_change(e):
        form_values['duration'] = e.value


    def duration_input():
        ui.number(
            label=f'Duration (1..{consts.SERVICE_MAX_DURATION_MINUTES})',
            value=1,
            min=1,
            max=consts.SERVICE_MAX_DURATION_MINUTES,
            format='%0.0f',
            on_change=lambda e: duration_input_on_change(e),
        ).classes('w-full mt-8')


    def sim_duration_select_on_change(e):
        form_values['sim_duration'] = e.value


    def sim_duration_selection():
        sim_duration_options = {
          1: '1 sec',
          2: '2 sec',
          5: '5 sec',
          10: '10 sec',
          15: '15 sec',
          30: '30 sec',
        }
        ui.select(
            label='Sim duration:',
            options=sim_duration_options,
            value=1,
            on_change=lambda e: sim_duration_select_on_change(e),
        ).classes('w-full mt-8')


    def validate_sim_values():
        result = True
        if form_values['contract_id'] == '':
            result = False
        if form_values['service_type'] == '':
            result = False
        return result


    def get_data_volume_left_of_contract():
        sum_session_per_contract = app.db.get_one('sum_sessions_per_contract', form_values['contract_id'])
        contract = app.db.get_one('contracts', form_values['contract_id'])
        data_volume_left = contract.data_volume - sum_session_per_contract.data_volume_sum
        return data_volume_left

    def validate_session(percentage, must_have_data_voluem_left):
        if form_values['service_type'] == 'call':
            return True
        sum_session_per_contract = app.db.get_one('sum_sessions_per_contract', form_values['contract_id'])
        contract = app.db.get_one('contracts', form_values['contract_id'])
        cur_kbytes = percentage * (form_values['duration'] * 60 * form_values['cur_throughput'])
        data_volume_left = contract.data_volume - sum_session_per_contract.data_volume_sum - cur_kbytes
        if must_have_data_voluem_left:
            return data_volume_left > 0
        else:
            return data_volume_left >= 0


    async def run_simulation(button):
        progress = None
        button.disable()
        try:
            if not validate_sim_values():
                ui.notify('Not all values to run a simulation filled in!')
                return

            ui.notify('Simulation started')
            progress = ui.linear_progress(value=0.0, show_value=False, size=8).props('instant-feedback').classes('w-full')
            sim_duration = form_values['sim_duration']
            done_percentage = 0.0

            try:
                # before start check general avaliable data
                if not validate_session(done_percentage, True):
                    raise Exception('No data volume left to start session!')

                for secs in range(0, sim_duration):
                    await asyncio.sleep(1)
                    done_percentage = (secs + 1) / sim_duration
                    progress.set_value(done_percentage)

                    if not validate_session(done_percentage, False):
                        raise Exception('All data volume used!')

                # all data received, write session
                ui.notify('Session completed')
                used_data_in_session = 0 if form_values['service_type'] == 'call' else form_values['duration'] * 60 * form_values['cur_throughput']
                used_duration_in_session = form_values['duration']

            except Exception as err:
                ui.notify('Error during session: ' + str(err))
                if done_percentage > 0:
                    # consume all data and store
                    used_data_in_session = get_data_volume_left_of_contract()
                    used_duration_in_session = math.ceil(used_data_in_session / form_values['cur_throughput'] / 60)

            # session store
            if done_percentage > 0:
                app.db.create(
                    'sessions',
                    dict(
                        contract=form_values['contract_id'],
                        service_type=form_values['service_type'],
                        duration=used_duration_in_session,
                        ran_type=form_values['ran_type'],
                        signal_quality=form_values['signal_quality'],
                        cur_throughput=form_values['cur_throughput'],
                        data_volume=used_data_in_session,
                    )
                )

        finally:
            if progress:
                progress.delete()
            button.enable()


    def sim_button():
        ui.button('Run', on_click=lambda e: run_simulation(e.sender)).classes('w-full mt-8')


    # page_session_new
    with layout.page_layout():
        contract_selection()
        network_information()
        ui.button('Refresh network', on_click=lambda: network_random_change()).classes('w-full mt-8')
        service_type_selection()
        duration_input()
        sim_duration_selection()
        sim_button()
