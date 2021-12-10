import digitalocean
import importlib
import time
import os

try:
    secrets = importlib.import_module('secrets')
except ModuleNotFoundError:
    secrets = None

if secrets is not None:
    os.environ['DIGITALOCEAN_ACCESS_TOKEN'] = secrets.DIGITALOCEAN_ACCESS_TOKEN

def test_manager():
    manager = digitalocean.Manager()
    return manager


def test_project():
    manager = test_manager()
    my_projects = manager.get_all_projects()
    project = my_projects[0]
    print(my_projects)
    # print(project, dir(project), help(project))
    return project


def test_droplet_list():
    # project = test_project()
    # recources = project.get_all_resources()
    # print(recources)
    # return recources
    manager = test_manager()
    droplets = manager.get_all_droplets()
    print(droplets)
    for droplet in droplets:
        print(droplet)
        print(dir(droplet))
    return droplets

def test_droplet_destroy():
    droplets = test_droplet_list()
    for droplet in droplets:
        droplet.destroy()

def test_add_keys():
    manager = test_manager()
    keys = manager.get_all_sshkeys()
    print(keys)
    return keys


def test_droplet_create():
    droplet = digitalocean.Droplet(name='Example',
                                   region='sgp1',
                                   image='ubuntu-20-04-x64',
                                   size_slug='s-1vcpu-1gb',
                                   backups=False)
    droplet.create()
    while True:
        actions = droplet.get_actions()
        for action in actions:
            action.load()
            # Once it shows "completed", droplet is up and running
            print(action.status)
        time.sleep(2)


if __name__ == '__main__':
    # test_project()
    # test_droplet_create()
    # test_droplet_list()
    # test_add_keys()
    test_droplet_destroy()
