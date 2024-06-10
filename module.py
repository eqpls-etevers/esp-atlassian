# -*- coding: utf-8 -*-
'''
Equal Plus
@author: Hye-Churn Jang
'''

#===============================================================================
# Import
#===============================================================================
import os
import json
import shutil
import docker
import argparse
import configparser

#===============================================================================
# Implement
#===============================================================================
# load configs
path = os.path.dirname(os.path.realpath(__file__))
module = os.path.basename(os.path.normpath(path))
config = configparser.ConfigParser()
config.read(f'{path}/module.conf', encoding='utf-8')
client = docker.from_env()

# default configs
tenant = config['default']['tenant']
version = config['default']['version']
host = config['default']['host']
port = config['default']['port']
system_access_key = config['default']['system_access_key']
system_secret_key = config['default']['system_secret_key']


#===============================================================================
# Container Control
#===============================================================================
# build
def build(): client.images.build(nocache=True, rm=True, path=f'{path}', tag=f'{tenant}/{module}:{version}')


# deploy
def deploy():
    try: os.mkdir(f'{path}/conf.d')
    except: pass
    try: os.mkdir(f'{path}/data.d')
    except: pass
    
    with open(f'{path}/conf.d/{module}.conf', 'w') as fd:
        fd.write('''
# Configuration Here
        ''')

    client.containers.run(
        f'{tenant}/{module}:{version}',
        detach=True,
        name=module,
        network=tenant,
        ports={
            f'{port}/tcp': (host, int(port))
        },
        environment=[
        ],
        volumes=[
            f'{path}/conf.d:/conf.d',
            f'{path}/data.d:/data.d',
        ],
        healthcheck={
            'test': 'echo "OK"',
            'interval': 60 * 1000000000,
            'timeout': 2 * 1000000000
        }
    )


# start
def start():
    try:
        for container in client.containers.list(all=True, filters={'name': module}): container.start()
    except: pass


# restart
def restart():
    try:
        for container in client.containers.list(all=True, filters={'name': module}): container.restart()
    except: pass


# stop
def stop():
    try:
        for container in client.containers.list(all=True, filters={'name': module}): container.restart()
    except: pass


# clean
def clean():
    for container in client.containers.list(all=True, filters={'name': module}): container.remove(v=True, force=True)
    shutil.rmtree(f'{path}/conf.d', ignore_errors=True)
    shutil.rmtree(f'{path}/data.d', ignore_errors=True)


# purge
def purge():
    try:
        for container in client.containers.list(all=True, filters={'name': module}): container.remove(v=True, force=True)
    except: pass
    try: client.images.remove(image=f'{tenant}/{module}:{version}', force=True)
    except: pass
    shutil.rmtree(f'{path}/conf.d', ignore_errors=True)
    shutil.rmtree(f'{path}/data.d', ignore_errors=True)


# monitor
def monitor():
    try:
        for container in client.containers.list(all=True, filters={'name': module}): print(json.dumps(container.stats(stream=False), indent=2))
    except: pass


# logs
def logs():
    try:
        for container in client.containers.list(all=True, filters={'name': module}): print(container.logs(tail=100).decode('utf-8'))
    except: pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--build', action='store_true', help='build container')
    parser.add_argument('-d', '--deploy', action='store_true', help='deploy container')
    parser.add_argument('-s', '--start', action='store_true', help='start container')
    parser.add_argument('-r', '--restart', action='store_true', help='restart container')
    parser.add_argument('-t', '--stop', action='store_true', help='stop container')
    parser.add_argument('-c', '--clean', action='store_true', help='clean container')
    parser.add_argument('-p', '--purge', action='store_true', help='purge container')
    parser.add_argument('-l', '--logs', action='store_true', help='show container logs')
    parser.add_argument('-m', '--monitor', action='store_true', help='show container stats')

    args = parser.parse_args()
    if not (args.logs or args.monitor):
        argCount = 0
        argCount += 1 if args.build else 0
        argCount += 1 if args.deploy else 0
        argCount += 1 if args.start else 0
        argCount += 1 if args.restart else 0
        argCount += 1 if args.stop else 0
        argCount += 1 if args.clean else 0
        argCount += 1 if args.purge else 0
        if argCount > 1 or argCount == 0: parser.print_help()

    if args.build: build()
    elif args.deploy: deploy()
    elif args.start: start()
    elif args.restart: restart()
    elif args.stop: stop()
    elif args.clean: clean()
    elif args.purge: purge()
    if args.monitor: monitor()
    if args.logs: logs()
