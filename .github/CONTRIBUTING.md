# Adding a new bypass/app
The files to edit are all under `manifests/`:
- `bypasses.yaml` contains information on the bypass themselves; mainly, its name and the repo it's hosted on.
- `apps/` contains individual files for each app, containing basic information and which bypass to use.
    - Filename must be `<app name>.yaml`

As each already have their own defined structure, please follow the format on existing files.

All manifests must be encoded in UTF-8, with the newline being `\n` (Unix line endings)

## bypasses.yaml
Check with this file for available bypasses. Its structure is as follows:
- Root key is the name of the bypass. It should be as close to the name of the package as possible, so use `Liberty Lite (Beta)` instead of `Liberty Lite Beta`.
- Under the root key there are three keys that are made use of:
    - `notes`: Extra notes about the bypass that does not fit any of the keys below.
    - `repo`: APT (Sileo, Cydia, etc.) source of the bypass. If the bypass is not hosted in a repo, please link the canonical source in the `notes` key (see: GenshinJailbreakBypass)
    - `guide`: Guide link for the bypass. If you want to add a guide, please do so under the `docsify` branch.

## App manifest
Each app has its own individual manifest under the `apps/` directory, which has this structure:
- Filename: `<app name>.yaml`. It should be as close to the app name on App Store as possible; however, there are a few allowed exceptions:
    1. If the app name contains any of the following characters: `< > : " / \ ? *`, it should be omitted.
    2. If the app name contains a short description, such as [YONO SBI:Banking and Lifestyle](https://apps.apple.com/us/app/yono-sbi-banking-and-lifestyle/id1231393474), the description should be cut off (YONO SBI).
    3. If the app name is written in a non-English script, it should be romanized (e.g. Альфа-Банк -> Alfa-Bank).
- Inside the file are a few keys, in order:
    - `name`, whose value should be the name of the app. Again, it should be as close to the app name on App Store as possible, but exception ii applies.
    - `uri` must contain an App Store URL to the app. This can be easily acquired by googling `site:apps.apple.com <app name>`. If the link is not English, suffix the link with `?l=en` (e.g. `https://apps.apple.com/hk/app/aastocks-m-mobile/id368726182?l=en`).
    - `bypasses` contain information on how to bypass the app's detection:
        - If there is no known bypasses, the key's value is `null`:
            ```yaml
            bypasses: null
            ```
        - If there are bypasses, the key contains an array, with each item containing these keys:
            - `name`: The name of the bypass, must be the same as a known bypass in `bypasses.yaml`
            - `notes`: Extra notes about using the bypass
            - `version`: Specify a version to downgrade to for the bypass  
            Either `name` or `notes` must exist.
