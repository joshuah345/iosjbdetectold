# Adding a new bypass/app
The files to edit are all under `manifests/`:
- `bypasses.yaml` contains information on the bypass themselves; mainly, its name and the repo it's hosted on.
- `apps/` contains individual files for each app, containing basic information and which bypass to use.
        - Filename must be `<app name>.yaml`

As each already have their own defined structure, please follow the format on existing files.

All manifests must be encoded in UTF-8.