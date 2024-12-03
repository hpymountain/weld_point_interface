from tokeo.ext.appshare import app
from ba_interface.core import consts
from ba_interface.core.pages import layout
from pathlib import Path

ui = app.nicegui.ui
ux = app.nicegui.ux


@app.nicegui.fastapi_app.get('/api')
async def get_api():
    return {'msg': 'json api result'}

@ui.page('/complete-notebook')
def show_full_notebook():
    with layout.page_layout():
        # test
        ux.p('hier kommt das ganze notebook hin').classes("text-sm font-semibold leading-6 text-gray-900")

# ist nur damit es läuft noch dabei..
# kann raus, wenn das richtige dsg file ausgegeben werden kann
def generate_dsg_file():
    """Generate a DSG file in the backend and return its path."""
    dsg_content = "Sample content for DSG file\n"  # Replace this with your actual DSG file generation logic
    dsg_file_path = Path("generated_file.dsg")
    dsg_file_path.write_text(dsg_content)
    return dsg_file_path

def default():
    with layout.page_layout():

        # Image-Upload
        with ux.div().classes("space-y-4 w-2/3"):  # Ensure consistent width
            ux.p('Upload file to analyze:').classes("text-sm font-semibold leading-6 text-gray-900")
            ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('w-full')

        # Threshold Contrast
        with ux.div().classes("space-y-2 mt-8 w-2/3"):
            ux.p('Contrast threshold:').classes("text-sm font-semibold leading-6 text-gray-900")
            ui.number(label='Set contrast threshold', value=80, format='%i', min=0, max=255).classes('w-full')

        # Crop-Option with Yes/No next to switch
        with ux.div().classes("flex items-center mt-8 space-x-4 w-2/3"):
            ux.p('Crop image to circle?').classes('text-sm font-semibold leading-6 text-gray-900')
            switch = ui.switch(value=True).classes('w-fit')
            label = ui.label('Yes').classes('w-fit')  # Default is "Yes"
            label.bind_text_from(switch, 'value', backward=lambda value: 'Yes' if value else 'No')

        # Run-Button
        ui.button('Process Image!', on_click=lambda: ui.notify('Analysis in progress!')).classes('mt-8 w-2/3')

        # DSG File Download Button
        ux.p('Download coordinates as DSG file:').classes('text-sm font-semibold leading-6 text-gray-900 mt-8')
        ui.button('Download Coordinates', on_click=lambda: ui.download(generate_dsg_file())).classes('mt-8 w-2/3')

        # Link to Notebook-View
        with ux.div().classes("mt-10 w-2/3"):
            ui.link('View Full Details', '/complete-notebook').classes("text-sm font-medium text-blue-600 hover:underline w-full")
