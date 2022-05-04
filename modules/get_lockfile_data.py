from time import sleep

from psutil import process_iter


def parse_cmdline_args(cmdline_args):
    cmdline_args_parsed = {}
    for cmdline_arg in cmdline_args:
        if len(cmdline_arg) > 0 and '=' in cmdline_arg:
            key, value = cmdline_arg[2:].split('=')
            cmdline_args_parsed[key] = value
    return cmdline_args_parsed


def find_lcu_process():
    for process in process_iter():
        if process.name() in ['LeagueClientUx.exe', 'LeagueClientUx']:
            return process
    return None


async def get_lockfile_data():
    while True:
        process = find_lcu_process()
        if process is not None:
            raw_data = process.cmdline()
            data = parse_cmdline_args(cmdline_args=raw_data)
            return data

        print('Waiting for the League client to be open...')
        # Let's be nice to the cpu
        sleep(1)
