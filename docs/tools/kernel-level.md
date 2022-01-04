# Kernel-Level Bypasses

!> Kernel-level bypasses are experimental. Exercise caution.

?> For further support in English, ask for help in the [r/Jailbreak Discord server](https://discord.gg/jb).

## KernBypass

!> Do not use KernBypass on any iOS version above 14.2 or below 12.0.
KernBypass will not work on iOS 14 using unc0ver. Use [vnodebypass](#vnodebypass) instead.

?> Available from [ichitaso's repo.](https://cydia.ichitaso.com/)

1. Launch Settings
2. Open the prefs for KernBypass
3. Tap `Enable KernBypass`
4. Enable all the apps you want to block jailbreak detection for.

## vnodebypass

!> vnodebypass will disable tweaks globally as well as hide many crucial jailbreak-related files. Make sure to disable vnodebypass once you're finished using the app you're attempting to bypass.

?> Available from [ichitaso's repo.](https://cydia.ichitaso.com/)

> Users on unc0ver (iOS 14+) must also install Siguza's `libkrw` from Elucubratus, else vnodebypass will fail to enable. If enabling still fails, reinstall libkrw.

1. After installation, an app will appear on your homescreen named `vnodebypass`.
2. Launch it and press the `Enable` button.
3. When you're done using the app with jailbreak detection, launch the app again and tap `Disable`.

### Unable to disable vnodebypass?

First step: **don't panic!**

A reboot will revert changes made by vnodebypass, but you can run `vnodebypass -r` in a shell to revert as well.
