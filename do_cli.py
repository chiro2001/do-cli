import os
import json
import sys
import time
import importlib
import argparse
import digitalocean
from typing import List, Optional
from digitalocean.Droplet import Droplet
from digitalocean.Manager import Manager
from digitalocean.Project import Project
from digitalocean.SSHKey import SSHKey
from utils.logger import logger


class DoCli:
    def __init__(self, *args, token: str = None, quiet: bool = False, no_upload_keys: bool = False,
                 local_token: bool = False, **kwargs) -> None:
        self.quiet: bool = quiet
        self.upload_keys: bool = not no_upload_keys
        self.local_token: bool = local_token
        self.token: str = token

        self.init_token(*args, **kwargs, token=token)
        self.manager: Manager = None
        self.projects: List[Project] = None
        self.droplets: List[Droplet] = None
        self.keys: List[SSHKey] = None
        self.update_info()

    def update_info(self):
        if self.local_token:
            self.manager = digitalocean.Manager(token=self.token)
        else:
            self.manager = digitalocean.Manager()
        self.projects = self.manager.get_all_projects()
        self.droplets = self.manager.get_all_droplets()
        self.keys = self.manager.get_all_sshkeys()

    def init_token(self, token: str = None, *args, **kwargs) -> None:
        if self.local_token:
            self.token = token
        else:
            try:
                secrets = importlib.import_module('secrets')
            except ModuleNotFoundError:
                secrets = None

            if secrets is not None:
                os.environ['DIGITALOCEAN_ACCESS_TOKEN'] = secrets.DIGITALOCEAN_ACCESS_TOKEN
            if token is not None:
                os.environ['DIGITALOCEAN_ACCESS_TOKEN'] = token

    @staticmethod
    def wait(droplet: Droplet, task_name: str = 'task', target_state: str = 'completed',
             sleep_time: int = 2) -> bool:
        done = False
        while not done:
            try:
                actions = droplet.get_actions()
                for action in actions:
                    action.load()
                    status = action.status
                    logger.info(f"{task_name} status: {status}")
                    if target_state == status:
                        done = True
                        break
                time.sleep(sleep_time)
            except KeyboardInterrupt as e:
                logger.warning(f"{task_name} was cancelled by {e.__class__.__name__}")
                break
        return done

    def create(self, *args, with_keys: bool = False, wait_complete: bool = True, **kwargs) -> Optional[Droplet]:
        name = kwargs.get('name')
        logger.info(f"Creating droplet: {name}")
        if with_keys or self.upload_keys:
            logger.info(f"Will upload your ssh keys.")
            kwargs['ssh_keys'] = self.keys
        if self.local_token:
            kwargs['token'] = self.token
        droplet = digitalocean.Droplet(*args, **kwargs)
        droplet.create()
        if wait_complete:
            self.wait(droplet, task_name='Create droplet')
        self.update_info()
        return self.find_droplet(name=name)

    def find_droplet(self, name: str = None) -> Optional[Droplet]:
        li = [_ for _ in self.find_droplet_generator(name=name)]
        if len(li) == 0:
            return None
        return li[0]

    def find_droplets(self, name: str = None) -> List[Droplet]:
        return [_ for _ in self.find_droplet_generator(name=name)]

    def find_droplet_generator(self, name: str = None):
        for droplet in self.droplets:
            if name is None or droplet.name == name:
                yield droplet

    def destroy(self, *args, wait_complete: bool = True, name: str = None, **kwargs) -> bool:
        self.update_info()
        if name is not None:
            logger.info(f"Destroying droplet: {name}...")
        else:
            logger.info(f"Destroying all droplet...")
        if len(self.droplets) == 0:
            logger.warning(f"No droplets in your account.")
            return False
        confirm_destroy = name is not None or self.quiet
        destroyed = False
        # destroy all if no name provided
        for droplet in self.find_droplet_generator(name=name):
            if name is None and not confirm_destroy:
                has_input = False
                while not has_input:
                    val = input(
                        'Continue to destroy all the droplets? [Y/n]').lower()
                    if val == 'n':
                        return False
                    elif val == 'y':
                        confirm_destroy = True
                        has_input = True
            droplet.destroy()
            if wait_complete:
                self.wait(
                    droplet, task_name=f'Destroy{" all" if name is None else ""} droplet')
                destroyed = True
        # for droplet in self.droplets:
        #     if name is None or droplet.name == name:
        if not destroyed:
            logger.warning(f"Did not destroy any droplet!")
        return True


default_args = {
    'name': "temp-droplet",
    'region': 'sgp1',
    'image': 'ubuntu-20-04-x64',
    'size_slug': 's-1vcpu-1gb',
    'backups': False
}


def main():
    parser = argparse.ArgumentParser(
        description='Manage your Digital Ocean droplets by simple CLI.')
    parser.add_argument('-c', '--create', action='store_true',
                        help='create a droplet.')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='run without inquiry.')
    parser.add_argument('-k', '--no_upload_keys', action='store_true',
                        help='do not upload all your ssh keys.')
    parser.add_argument('-f', '--file', required=False, default="do-cli.json",
                        help='load args from json file.')
    parser.add_argument('-d', '--destroy', action='store_true',
                        help='destroy a droplet. (destroy all droplets if not name provided.)')
    parser.add_argument('-t', '--token', required=False,
                        help='use token. (both $DIGITALOCEAN_ACCESS_TOKEN and '
                             'secret.DIGITALOCEAN_ACCESS_TOKEN are ok.)')
    parser.add_argument('-n', '--name', required=False,
                        help='droplet name.')
    parser.add_argument('-r', '--region', required=False,
                        help='droplet region.')
    parser.add_argument('-i', '--image', required=False,
                        help='droplet image.')
    parser.add_argument('-s', '--size_slug', required=False,
                        help='droplet size.')
    parser.add_argument('-b', '--backups', required=False, action="store_true",
                        help='enable droplet backups.')
    control_keys = ['create', 'destroy', 'quiet', 'no_upload_keys']
    args_keys = ['name', 'region', 'image', 'size_slug', 'backups']
    args_raw = parser.parse_args().__dict__
    args = {k: args_raw[k] for k in args_raw if args_raw[k]
            is not None and k in args_keys}
    control_args = {k: args_raw[k] if isinstance(
        args_raw[k], bool) else False for k in args_raw if k in control_keys}
    if not control_args['create'] and not control_args['destroy']:
        logger.warning(f"No task to execute. exiting...")
        sys.exit(1)
    if 'file' in args_raw and args_raw['file'] is not None and os.path.exists(args_raw['file']):
        with open(args_raw['file'], 'r', encoding='utf8') as f:
            args_loaded = json.load(f)
            args_loaded.update(args)
            args = args_loaded
            logger.info(f"Loaded args from {args_raw['file']}: {args_loaded}")
    wait_key = not control_args['quiet']
    if control_args['create'] and control_args['destroy'] and not control_args['quiet']:
        logger.warning(f"Will create the droplet and wait until key down.")
        wait_key = True
    cli = DoCli(**control_args)
    if control_args['create']:
        args_needed = []
        for key in args_keys:
            if key not in args:
                args_needed.append(key)
        if len(args_needed) != 0:
            logger.error(f"arg(s) needed: {args_needed}")
            sys.exit(1)
        logger.info(f"args: {args}")
        droplet = cli.create(**args)
        if droplet is not None:
            logger.info(f"Created a droplet at {args.get('region')}, "
                        f"size: {droplet.size_slug}, "
                        f"ip address:\t{droplet.ip_address}\tuse:\tssh root@{droplet.ip_address}")
        else:
            logger.error(f"Cannot create droplet {args.get('name')}")
            sys.exit(1)
    while wait_key and control_args['create'] and control_args['destroy']:
        val = input(
            f'Continue to destroy this droplet ({args.get("name")})? [Y/n]').lower()
        if val == 'n':
            sys.exit(0)
        elif val == 'y':
            wait_key = False
    if control_args['destroy']:
        cli.destroy(**args)


def test():
    cli = DoCli()
    cli.create(**default_args, with_keys=True, wait_complete=True)
    cli.destroy()


if __name__ == '__main__':
    main()
    # test()
