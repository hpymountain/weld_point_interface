from tokeo.ext.appshare import app
from contextlib import contextmanager


ui = app.nicegui.ui
ux = app.nicegui.ux


@contextmanager
def page_layout():
    with ux.div().classes('w-5/6 md:w-3/4 xl:w-1/2 mx-auto my-8'):
        ux.h1('Vortex Solutions').classes('w-full text-4xl center')
        ux.p('- unchallenged perfection as promised -').classes('w-full text-xl center mt-8')
        with ux.div().classes('mt-10 mb-16'):
            ui.link('Home', '/')

        with ux.div().classes('w-full').style('max-width: 36rem mx-auto'):
            yield

        ux.p('(C)2024 all together').classes('mt-20')

