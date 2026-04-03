from os.path import exists

from Constants import IN_APP_SETTINGS_NAME
from core.BotLogger import BotLogger
from core.entities.CMD import CMD
from core.entities.Cmake_cmd import Cmake_cmd
from core.entities.Make_cmd import Make_cmd
from core.entities.Meson_cmd import Meson_cmd
from core.util.Wrappers import (
    safe_log,
    log
)

# Global entities:
cmd: CMD
backend_local_logger: BotLogger = BotLogger()


@safe_log
def build_sys_fabric(cmd_name: str = 'cmake'):
    match cmd_name:
        case 'cmake':
            backend_local_logger.log('Choose cmake')
            return Cmake_cmd()
        case 'make':
            backend_local_logger.log('Choose make')
            return Make_cmd()
        case 'meson':
            backend_local_logger.log('Choose meson')
            return Meson_cmd()
        case _:
            raise NotImplementedError('Implement build system object first')


@log
def decide_build_system():
    global cmd
    if exists(IN_APP_SETTINGS_NAME):
        backend_local_logger.log('In app settings exists')
        with open(IN_APP_SETTINGS_NAME, 'r') as settings:
            build_sys_name = settings.read()
            backend_local_logger.log(f'Choose build system from settings - {build_sys_name}')
            cmd = build_sys_fabric(build_sys_name)
    else:
        pass


@log
def init_conan():
    pass


@log
def add_dependencies():
    pass


@log
def remove_dependencies():
    pass


@log
def update_dependencies():
    cmd.update_dependencies()


@log
def show_path_to_config():
    pass
