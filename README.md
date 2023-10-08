# minisforum HX80G/HX90G/HX99G miniPC Hackintosh

![release version](https://img.shields.io/github/v/release/daliansky/minisforum-HX90G-Hackintosh?style=for-the-badge) 

[![OpenCore version](https://img.shields.io/badge/OpenCore-0.9.0-informational.svg)](https://github.com/acidanthera/OpenCorePkg)![MacOS version](https://img.shields.io/badge/Ventura-13.2.1-informational.svg)![MacOS version](https://img.shields.io/badge/Monterey-12.6.1%2021G115-informational.svg)

[![HX90G_1920](ScreenShots/HX90G_1920.png)](https://item.taobao.com/item.htm?id=689916679408)

## 电脑配置

|   规格   |                           详细信息                           |
| :------: | :----------------------------------------------------------: |
| 电脑型号 |                minisforum HX90G/HX99G miniPC                 |
| 操作系统 |                 macOS `Ventura` / `Monterey`                 |
|  处理器  |       AMD 锐龙 R7-5800H 8核16线程[HX80G] `完美黑苹果`        |
|  处理器  |       AMD 锐龙 R9-5900HX 8核16线程[HX90G] `完美黑苹果`       |
|  处理器  |    AMD 锐龙 R9-6900HX 8核16线程[HX99G] `黑苹果适配中...`     |
|   内存   |            64 GB DDR4 3200MHz / 64GB DDR5 4800MHz            |
| 硬盘1/2  |                 支持双NVMe或NVMe+SATA自适应                  |
|   显卡   |                 AMD Radeon RX6600m 8GB GDDR6                 |
| 显示接口 | USB4 x2(8K@60Hz)[HX99G] / DP 1.4x2(4K@144Hz) [HX90G/HX80G] + HDMI 2.1x2(4K@144Hz) |
|   声卡   |                       USB Audio Device                       |
| 无线网卡 | m.2 NGFF插槽，默认出厂为 `Mediatek RZ608` 已更换为[BCM94360Z3](https://blog.daliansky.net/uploads/WeChatandShop.png) |
| 有线网卡 |               Intel Ethernet Controller I225-V               |

## 更新日志

- 10-8-2023
  - 更新 `OpenCore` 到 `v0.9.5`
  - 更新对 `Sonoma` 的支持，博通网卡需要使用 `OCLP` 打补丁
  
- 4-24-2023
  - 更新 `OpenCore` 到 `v0.9.1`
  - 此版本命名为 `夏凉版` ，禁用该参数，就是 `暖手宝` 版 `^_^`
  - 注入了 `PP_PhmSoftPowerPlayTable` 参数，让显卡风扇持续工作，相应地会带来些风噪，但是机器温度却会保持在 `30-40` 度区间
- 3-13-2023
  - 更新 `OpenCore` 到 `v0.9.0`
  - 更新了 `Intel I225-V` 的驱动方法
  - 更新对 `Ventura 13.3+` 的支持
- 02-28-2023
  * 更新 `OpenCore` 到 `v0.8.9`

  * 更新 `AMD_Vanilla` 到 `202302`

  * 更新 `AppleALC` 到 `v1.7.9`

  * 更新 `WhateverGreen` 到 `v1.6.4`
- 11-17-2022

  - 更新 `OpenCore` 到 `v0.8.6`

## 应用兼容列表

> 多亏了[AMD vanilla 补丁](https://github.com/AMD-OSX/AMD_Vanilla)，我们甚至可以在现代 AMD 机器上运行最新的 macOS，而无需创建自定义内核，但仍有一些警告。
> 
> 某些应用程序使用臭名昭著的英特尔 MKL 库，现在称为英特尔 OneAPI：这些库兼容 x86_64，但在 macOS 移植中，某些功能仅适用于真正的英特尔 CPU：它们是 __intel_fast_memset.A 和 __intel_fast_memcpy.A。
> 
> 我们可以欺骗这些库，将这些调用重定向到 __intel_fast_memset.J 和 __intel_fast_memcpy.J，它们在 AMD Hackintoshes 上完美运行，并且考虑到我们缺少 AVX512 的事实，尽可能快。
> 
> 但是我们还需要欺骗他们更改函数 __mkl_serv_intel_cpu_true 来返回 TRUE，即使在 AMD cpus 上运行也是如此。
> 
> 仅使用这三个"补丁"，我们就可以使每个仅英特尔应用程序在我们的 AMD Hacks 上本地运行，而无需使用虚拟机管理程序，也无需绕过或删除我们特定应用程序的重要功能/文件。

请移步：[这里](https://www.macos86.it/topic/5479-amd-new-applications-life/)

用到的工具：[这里](https://github.com/NyaomiDEV/AMDFriend)

## 截屏

![1.About](ScreenShots/0About.png)

![2.About](ScreenShots/1About.png)

![Bluetooth](ScreenShots/Bluetooth.png)

![I225-V_DHCP](ScreenShots/I225-V_DHCP.png)

![I225-V_Hardware](ScreenShots/I225-V_Hardware.png)

![Audio](ScreenShots/Audio.png)

![Bluetooth](ScreenShots/Bluetooth.png)

![Bluetooth2](ScreenShots/Bluetooth2.png)

![BT](ScreenShots/BT.png)

![Displays](ScreenShots/Displays.png)

![Ethernet](ScreenShots/Ethernet.png)

![Graphics](ScreenShots/Graphics.png)

![Hackintool_Kexts](ScreenShots/Hackintool_Kexts.png)

![Hackintool_MISC](ScreenShots/Hackintool_MISC.png)

![Hackintool_NVRAM](ScreenShots/Hackintool_NVRAM.png)

![Hackintool_OC](ScreenShots/Hackintool_OC.png)

![Hackintool_PM](ScreenShots/Hackintool_PM.png)

![Hackintool_USB](ScreenShots/Hackintool_USB.png)

![Hackintool](ScreenShots/Hackintool.png)

![Hardware](ScreenShots/Hardware.png)

![Memory](ScreenShots/Memory.png)

![NVMe](ScreenShots/NVMe.png)

![Power](ScreenShots/Power.png)

![Sounds](ScreenShots/Sounds.png)

![USB](ScreenShots/USB.png)

![WallPaper](ScreenShots/WallPaper.png)

![Wi-Fi](ScreenShots/Wi-Fi.png)

![WIFI](ScreenShots/WIFI.png)

![CineBenchR23](ScreenShots/CineBenchR23.png)

## 鸣谢

- [macos86.it](https://www.macos86.it/)
- 
