# Special workarounds

!> This page usually deals with editing files that normally are left untouched. Workarounds may break, so exercise caution.

?> For further support in English, ask for help in the [r/Jailbreak Discord server](https://discord.gg/jb).

## Hang Seng Personal Banking
After downgrading to version 5.0, locate the app's Info.plist (typically `/var/containers/Bundle/Application/<app name>/<app name>.app/Info.plist` if you use Filza), expand the `Root` key and select the (i) button on `CFBundleVersion`. Set the value to `999`, then save and exit the file.

If app still refuses to open, install AntiProfilesRevoke from BigBoss.