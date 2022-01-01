Current API: `https://beerpsi.me/api/v1/`

# API
A simple API intended for looking up bypass + app combinations. It currently has two public endpoints:

`GET /app?search=<app name>`: Lookup the app with the keyword `<app name>`  
**Request:** `/app?search=balls`
```json
{
    "status": "Successful",
    "data": [
        {
            "name": "8 Ball Pool",
            "uri": "https://apps.apple.com/us/app/8-ball-pool/id543186831",
            "bypasses": [
                {
                    "name": "Liberty Lite (Beta)",
                    "guide": "https://bypass.beerpsi.me/#/tools/tweaks?id=liberty-lite-beta",
                    "repository": {
                        "uri":"https://ryleyangus.com/repo"
                    }
                }
            ]
        }
    ]
}
```

`POST /gh-webhook`:
**Requires the API to be set up as a systemd service, see below**

As the name implies, this is where the GitHub webhook goes. When an appropriate `POST` request is sent, the database is refreshed.  
To prevent anyone from willy-nilly sending a POST request and refreshing the database, this endpoint is only active if the environment variable `GITHUB_WEBHOOK_SECRET` is set.


# Running the API yourself
Quickly set up a local dev server for testing changes:
```bash
# *nix
python -m venv env/ && source env/bin/activate
pip install -r openapi/requirements.txt
python3 openapi/api.py
```

```powershell
# Windows
python -m venv env/ && env\Scripts\Activate.ps1 # powershell
pip install -r openapi/requirements.txt
python3 openapi/api.py

# If Flask is complaining, try restarting the Host Networking Service
net stop hns && net start hns
```


# Making the API public
Here's how `https://beerpsi.me/api/v1` was set up, but depending on your webserver and stuff you can do it differently.

The API uses uWSGI, so you should install that:
```bash
pip install uwsgi
```

Then, create a file called `app.ini` that should ideally be under `openapi/`:
```ini
[uwsgi]
module = api:app

master = true
processes = 5

socket = api.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```

Create a systemd service (change `/var/www/jbdetectlist` to where you put the API):
```ini
[Unit]
Description='An API for querying jailbreak bypasses'
After=network.target

[Service]
Environment=GITHUB_WEBHOOK_SECRET=<This is for webhooking>
User=www-data
Group=root
WorkingDirectory=/var/www/jbdetectlist/openapi
ExecStart=/var/www/jbdetectlist/env/bin/uwsgi --ini api.ini

[Install]
WantedBy=multi-user.target
```

Allow the user running the API to restart the service without a password by creating `/etc/sudoers.d/auto-deploy` (important for auto-deploy):
```
Cmnd_Alias MYAPP_CMNDS = /bin/systemctl start jbdetectapi, /bin/systemctl stop jbdetectapi, /bin/systemctl restart jbdetectapi
www-data ALL=(ALL) NOPASSWD: MYAPP_CMNDS
```

Start and enable the service, then configure nginx:
```nginx
server {
    server_name beerpsi.me;
    location /api/v1 {
        rewrite ^/api/v1/(.*) /$1 break;
        include uwsgi_params;
        uwsgi_pass unix:/var/www/jbdetectlist/openapi/api.sock;
    }
}
```

and that's about it!
