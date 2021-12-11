import requests
import json
import secrets


def test_api():
    # List all droplets
    req = requests.get('http://localhost:9981/api/v2/', headers={
        "Token": secrets.DIGITALOCEAN_ACCESS_TOKEN
    })
    js = req.json()
    print(js)
    # List droplets by name
    req = requests.get('http://localhost:9981/api/v2/?name=keys', headers={
        "Token": secrets.DIGITALOCEAN_ACCESS_TOKEN
    })
    js = req.json()
    print(js)
    # Create a droplet, full args needed
    req = requests.post('http://localhost:9981/api/v2/', headers={
        "Token": secrets.DIGITALOCEAN_ACCESS_TOKEN
    }, json={
        "name": "test-droplet",
        "region": "sgp1",
        "image": "ubuntu-20-04-x64",
        "size_slug": "s-1vcpu-1gb",
        "backups": False
    })
    js = req.json()
    print(js)
    # Destroy the droplet by name (all droplet with this name will be destroyed!)
    req = requests.delete('http://localhost:9981/api/v2/?name=test-droplet', headers={
        "Token": secrets.DIGITALOCEAN_ACCESS_TOKEN
    })
    js = req.json()
    print(js)


if __name__ == '__main__':
    test_api()
