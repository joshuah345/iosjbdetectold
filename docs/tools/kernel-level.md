# Kernel-Level Bypasses

!> Kernel-level bypasses are experimental. Exercise caution.

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

> Users on unc0ver (iOS 14.4+) must also install Siguza's `libkrw` from Elucubratus, else vnodebypass will fail to enable. If enabling still fails, reinstall libkrw.

1. After installation, an app will appear on your homescreen named `vnodebypass`. 
2. Launch it and press the `Enable` button.
3. When you're done using the app with jailbreak detection, launch the app again and tap `Disable`.

