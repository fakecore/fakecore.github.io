---
title: "NVIDIA GPU VFIO-Manager Overview"
date: 2024-11-11T23:39:53+08:00
# weight: 1
tags: ["k8s","gpu-operator"]
author: "fakecore"
# author: ["Me", "You"] # multiple authors
showToc: true
TocOpen: true
draft: false
UseHugoToc: true
hidemeta: false
comments: true
description: ""
disableHLJS: true # to disable highlightjs
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true
cover:
    image: "<image path/url>" # image path/url
    alt: "<alt text>" # alt text
    caption: "<text>" # display caption under cover
    relative: false # when using page bundles set this to true
    hidden: true # only hide on current single page
editPost:
    URL: "https://github.com/fakecore/content"
    Text: "Suggest Changes" # edit text
    appendFilePath: true # to append file path to Edit link
---

## NVidia's solution

In the GPU-Operator solution, there is a VFIO-Manager component that supports unbinding the GPU device from either the `GPU driver` or the `VFIO-PCI driver`, and binding it to the `VFIO-PCI driver`. The VFIO-Manager is controlled by the `vfio-manage.sh` script.

**vfio-manage.sh Functionality Overview**

Main Function:
`help`: display the help information
`bind`: bind the vfio-pci driver
`unbind`: unbind the vfio-pci driver

options:
`--all`: bind all devices
`--device_id`: bind a specified devices

### Function: bind

If a specific GPU is specified, bind only that GPU; otherwise, bind all devices

**bind all device**
Find all devices and bind each target GPU sequentially

**bind target gpu**

- Check if the device is not an NVIDIA GPU, return with an error
- Execute `bind_pci_device`:
    - Check if VFIO-PCI driver is already bound; if true, return
    - Execute unbind_from_other_device

    ``` bash
    # 1.Check if VFIO-PCI driver is already bound; if true, return
    [ -e "/sys/bus/pci/devices/$gpu/driver" ] || return 0

    #2. get current driver
    existing_driver=$(readlink -f "/sys/bus/pci/devices/$gpu/driver")
    existing_driver_name=$(basename "$existing_driver")

    #3. if current driver is vfio-pci, return
    [ "$existing_driver_name" != "vfio-pci" ] || return 0

    #4.unbind
    echo "$gpu" > "$existing_driver/unbind"
    echo > /sys/bus/pci/devices/$gpu/driver_override
    ```

    - Execute two bind operations:

    ``` bash
    echo "vfio-pci" > /sys/bus/pci/devices/$gpu/driver_override
    echo "$gpu" > /sys/bus/pci/drivers/vfio-pci/bind
    ```

- If the device is a graphic GPU, also bind the auxiliary device

### Function: unbind

If a specific GPU is specified, unbind only that GPU; otherwise, unbind all devices

**unbind all NVIDIA GPU**
Find all devices under `/sys/bus/pci/device`, check if the device manufacturer equals `0x10de`. If true, get the vendor ID and sequentially unbind each GPU.

> \[!tip\] vendor number
> NVIDIA device vendorID is 0x10de

**unbind target GPU**

- Check if it's an NVIDIA GPU; if not, return
- Execute `unbind_from_driver`:
    - Check If device is already bound; if not, return
    - Get current GPU bound driver path
- Execute two unbind operations:

``` bash
echo "$gpu" > "$existing_driver/unbind"
echo > /sys/bus/pci/devices/$gpu/driver_override
```

- If the device is a graphic GPU, also unbind the auxiliary device

## Appendix:

1.  https://code.google.com/archive/p/pci-hacking/wikis/bind_Uunbind_PCI.wiki
2.  https://github.com/NVIDIA/gpu-operator/blob/main/assets/state-vfio-manager/0400_configmap.yaml