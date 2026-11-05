#!/bin/sh

echo '=== Test procfs & sysfs ==='

if [ -d /sys/module/lab2_driver ]; then
    echo 'lab2_driver is already loaded.'
else
    insmod /lib/modules/5.15.0/lab2_driver.ko || {
        echo 'ERROR: Cannot load lab2_driver.ko'
        exit 1
    }
fi

mknod /dev/lab2 c 240 0 2>/dev/null

echo '--- /proc/lab2_info (before write) ---'
cat /proc/lab2_info

echo 'Embedded Linux Lab2 Test Data' > /dev/lab2

echo '--- /proc/lab2_info (after write) ---'
cat /proc/lab2_info

SYSFS=/sys/class/lab2_class/lab2

echo '--- sysfs attributes ---'
cat "$SYSFS/buffer_len"
cat "$SYSFS/open_count"
cat "$SYSFS/last_data"

echo '=== Test finished ==='
