# Non-bypasses
These tools are used for disabling and configuring tweak injection into processes.

?> For further support in English, ask for help in the [r/Jailbreak Discord server](https://discord.gg/jb).

## Choicy

> If you're using a jailbreak with libhooker, such as Chimera, Odyssey, odysseyra1n or Taurine, please use [libhooker-configurator](#libhooker-configurator), as Choicy's functions have been implemented into it.

?> Available from [opa334's repo](https://opa334.github.io/).

1. Launch Settings
2. Scroll down to Choicy
3. Tap on Applications
4. Choose the application with jailbreak detection.
  - For Snapchat, Clash of Clans (as well as a few other apps), toggle `Disable Tweak Injection` instead and skip the next steps.

For apps that don't respond well to tweak injection, yet have bypasses, complete the steps above, then:
1. Toggle `Custom Tweak Configuration`
2. Change the mode to `Allow`
3. Toggle the switch for the bypass you're using.
  - For [Liberty Lite (Beta)](/tools/tweaks?id=liberty-lite-beta), the switch would be `zzzzzLiberty`
  - For [A-Bypass](/tools/tweaks?id=a-bypass), the switch would be `!ABypass2`


## libhooker-configurator

!> libhooker-configurator is only available for Procursus-based jailbreaks. eg: Taurine/Odyssey(ra1n). If you use a Substrate or Substitute based jailbreak, such as checkra1n or unc0ver, use [Choicy](#choicy) instead.

1. Open the `libhooker` application
2. Tap on Applications
3. Select the application with jailbreak detection. You can either disable tweaks entirely by toggling off `Enable Tweaks`, or allow/deny specific tweaks:
  - To configure individual tweaks, enable `Override Configuration`, which will allow you to only allow or deny specific tweaks.
  - For example, to allow only [Liberty Lite (Beta)](/tools/tweaks?id=liberty-lite-beta), you'd select Allow, then select `zzzzzLiberty`.
