from app.backend_pre_start import main as pre_start
from app.initial_data import main as init_data


def pre_config():
    pre_start()
    init_data()
