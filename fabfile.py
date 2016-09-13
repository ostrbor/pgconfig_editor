"""
Changes ip address in pg_hba.conf on
remote server to client's ip, running
this script.
"""
from requests import get
from fabric.api import task, cd, env, sudo
from fabric.contrib.files import contains
from fabric.contrib.console import confirm

from config  import (WEB_SERVER, IPIFY_URL, PG_HBA_FILE,
                     PG_HBA_PATH, PG_HBA_LINE,
                     PG_RESTART_CMD, IP_CHANGER_COMMAND,
                     IP_GETTER_COMMAND)


env.hosts = [WEB_SERVER, ]

@task
def change_ip():
    my_ip = get(IPIFY_URL).text
    with cd(PG_HBA_PATH):
        remote_ip = sudo(IP_GETTER_COMMAND.format(LINE=PG_HBA_LINE, FILE=PG_HBA_FILE))
        if my_ip == remote_ip:
            print('Same ip.')
            return
        print('\npg_hba.conf: \n')
        sudo("cat %s"%PG_HBA_FILE)
        print('\nmy ip: %s'%my_ip)
        if confirm('\nCHANGE IP? '):
            sudo(IP_CHANGER_COMMAND.format(LINE=PG_HBA_LINE,
                                           FILE=PG_HBA_FILE,
                                           NEW_IP=my_ip))
            sudo(PG_RESTART_CMD)
