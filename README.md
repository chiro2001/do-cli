# digital-ocean-manager

## Usage

### Install requirements

```shell
python3 -m pip install -r requirements.txt
```

### CLI Usage

```shell
python3 do_cli.py -h
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

### Example

```shell
# Create a droplet from do-cli.json, wait key, and then destroy it.
python3 do_cli.py -f do-cli.json -c -d

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

### Args

`DIGITALOCEAN_ACCESS_TOKEN`: You can generate it from [here](https://cloud.digitalocean.com/account/api/tokens). Set it
as `$DIGITALOCEAN_ACCESS_TOKEN` or create python file named as `secrets.py` is ok.

`do-cli.json`: It's an optional file to provide default value. Args from command line will override it.

```json
{
  "name": "temp-droplet",
  "region": "sgp1",
  "image": "ubuntu-20-04-x64",
  "size_slug": "s-1vcpu-1gb",
  "backups": false
}
```

## Server Usage

You should provide `Token` in every request.

```shell
python3 server.py
```

To change listen address and port, modify `data/config.py`.

### API Document

Visit `/api/v2/docs` to get API document.

```json
{
  "code": 200,
  "data": {
    "document": {
      "/docs": {
        "disc": "Document test",
        "methods": {
          "get": {
            "disc": "Get all docs for APIs"
          }
        }
      },
      "/": {
        "disc": "API for do-cli",
        "methods": {
          "delete": {
            "disc": "Destroy your droplet\n:return:",
            "args": [
              {
                "name": "Token",
                "type": "str",
                "location": [
                  "headers"
                ],
                "help": "token of your digital ocean api",
                "choices": []
              },
              {
                "name": "name",
                "type": "str",
                "location": [
                  "args"
                ],
                "help": "name of droplet (destroy all if None)",
                "choices": []
              }
            ]
          },
          "get": {
            "disc": "Get your droplet list\n:return: List[Droplet]",
            "args": [
              {
                "name": "Token",
                "type": "str",
                "location": [
                  "headers"
                ],
                "help": "token of your digital ocean api",
                "choices": []
              },
              {
                "name": "name",
                "type": "str",
                "location": [
                  "args"
                ],
                "help": "name to use filter (fetch all if None)",
                "choices": []
              }
            ]
          },
          "post": {
            "disc": "Create a droplet\n:return: 200 if ok",
            "args": [
              {
                "name": "Token",
                "type": "str",
                "location": [
                  "headers"
                ],
                "help": "token of your digital ocean api",
                "choices": []
              },
              {
                "name": "name",
                "type": "str",
                "location": [
                  "json"
                ],
                "help": "name of droplet",
                "choices": []
              },
              {
                "name": "region",
                "type": "str",
                "location": [
                  "json"
                ],
                "help": "region of droplet",
                "choices": []
              },
              {
                "name": "image",
                "type": "str",
                "location": [
                  "json"
                ],
                "help": "image of droplet",
                "choices": []
              },
              {
                "name": "size_slug",
                "type": "str",
                "location": [
                  "json"
                ],
                "help": "size of droplet",
                "choices": []
              },
              {
                "name": "backups",
                "type": "bool",
                "location": [
                  "json"
                ],
                "help": "enable backup",
                "choices": []
              }
            ]
          }
        }
      }
    }
  }
}
```

See `test/test_api.py` for more.