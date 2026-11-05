#!/bin/sh

echo "========== ASGN2 SENSOR TEST =========="

mkdir -p /dev /proc /sys /tmp

mount -t proc proc /proc 2>/dev/null
mount -t sysfs sysfs /sys 2>/dev/null
mount -t devtmpfs devtmpfs /dev 2>/dev/null

MODULE=/lib/modules/5.15.0/sms_sensor_driver.ko

if [ ! -d /sys/module/sms_sensor_driver ]; then
    echo "[1] Loading driver..."
    insmod "$MODULE" || {
        echo "ERROR: insmod failed"
        dmesg | tail -30
        exit 1
    }
fi

echo "[2] Checking misc device"
grep sms_sensor /proc/misc

MINOR="$(awk '$2 == "sms_sensor" {print $1}' /proc/misc)"

if [ -z "$MINOR" ]; then
    echo "ERROR: Device not found"
    exit 1
fi

mknod /dev/sms_sensor c 10 "$MINOR" 2>/dev/null
chmod 666 /dev/sms_sensor

echo "[3] Device information"
ls -l /dev/sms_sensor

echo "[4] Driver statistics before test"
cat /proc/sms_stats

echo "[5] Run application"
 /usr/bin/sms_app_arm -v -d 15

echo "[6] Driver statistics after test"
cat /proc/sms_stats

echo "[7] Kernel messages"
dmesg | grep sms_sensor | tail -20

echo "========== TEST FINISHED =========="
