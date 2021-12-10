# digital-ocean-manager

## Usage

```shell
python3 -m pip install -r requirements.txt
python3 do-cli.py -h
```

```
usage: do-cli.py [-h] [-c] [-q] [-k] [-f FILE] [-d] [-t TOKEN] [-n NAME] [-r REGION] [-i IMAGE] [-s SIZE_SLUG] [-b]

Manage your Digital Ocean droplets by simple CLI.

optional arguments:
  -h, --help            show this help message and exit
  -c, --create          create a droplet.
  -q, --quiet           run without inquiry.
  -k, --no_upload_keys  do not upload all your ssh keys.
  -f FILE, --file FILE  load args from json file.
  -d, --destroy         destroy a droplet. (destroy all droplets if not name provided.)
  -t TOKEN, --token TOKEN
                        use token. (both $DIGITALOCEAN_ACCESS_TOKEN and secret.DIGITALOCEAN_ACCESS_TOKEN are ok.)
  -n NAME, --name NAME  droplet name.
  -r REGION, --region REGION
                        droplet region.
  -i IMAGE, --image IMAGE
                        droplet image.
  -s SIZE_SLUG, --size_slug SIZE_SLUG
                        droplet size.
  -b, --backups         enable droplet backups.
```

## Example

```shell
# Create a droplet from do-cli.json, wait key, and then destroy it.
python3 do-cli.py -f do-cli.json -c -d

Loaded args from do-cli.json: {'name': 'temp-droplet', 'region': 'sgp1', 'image': 'ubuntu-20-04-x64', 'size_slug': 's-1vcpu-1gb', 'backups': False}
Warning: will create the droplet and wait until key down.
args: {'backups': False, 'name': 'temp-droplet', 'region': 'sgp1', 'image': 'ubuntu-20-04-x64', 'size_slug': 's-1vcpu-1gb'}
Creating droplet: temp-droplet
will upload your ssh keys.
create droplet status: in-progress
create droplet status: in-progress
create droplet status: in-progress
create droplet status: in-progress
create droplet status: in-progress
create droplet status: in-progress
create droplet status: in-progress
create droplet status: in-progress
create droplet status: completed
Continue to destory this droplet (temp-droplet)? [Y/n]y
Destroying droplet: temp-droplet...
destroy droplet status: in-progress
destroy droplet status: completed
```

## Args

`DIGITALOCEAN_ACCESS_TOKEN`: You can generate it from [here](https://cloud.digitalocean.com/account/api/tokens). Set it as `$DIGITALOCEAN_ACCESS_TOKEN` or create python file named as `secrets.py` is ok.

`do-cli.json`:

```json
{
  "name": "temp-droplet",
  "region": "sgp1",
  "image": "ubuntu-20-04-x64",
  "size_slug": "s-1vcpu-1gb",
  "backups": false
}
```
