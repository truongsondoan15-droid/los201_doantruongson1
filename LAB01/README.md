# LAB01 – Embedded Linux Systems

## Student Information
- Full Name: Doan Truong Son
- Student ID: SE200908
- Lab: LAB01

## Project Description
This lab builds and boots an Embedded Linux system using:
- Linux Kernel 5.15
- U-Boot 2022.04
- BusyBox 1.36.1
- QEMU vexpress-a9
- ARM Cortex-A9

Note: The BusyBox version used is 1.36.1 instead of the required 1.35.0.

## Directory Structure

```text
LAB01/
├── README.md
├── output/
│   ├── zImage
│   ├── vexpress-v2p-ca9.dtb
│   └── initramfs.cpio.gz
├── configs/
│   ├── kernel.config
│   └── busybox.config
├── rootfs/
│   └── initramfs/
├── bao_cao/
│   └── SE200908_Lab01_BaoCao.pdf
└── rootfs.tar.gz
```

## Run QEMU

```bash
qemu-system-arm \
-M vexpress-a9 \
-cpu cortex-a9 \
-m 512M \
-smp 2 \
-nographic \
-kernel output/zImage \
-dtb output/vexpress-v2p-ca9.dtb \
-initrd output/initramfs.cpio.gz \
-append "console=ttyAMA0,115200 rdinit=/sbin/init mem=512M"
```

## Expected Result

The system boots into the Embedded Linux environment and displays:

```text
Boot completed! Welcome to Embedded Linux Lab 1
```

## Report

The lab report is available at:

`bao_cao/SE200908_Lab01_BaoCao.pdf`
