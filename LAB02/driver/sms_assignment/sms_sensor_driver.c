#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/uaccess.h>
#include <linux/random.h>
#include <linux/ktime.h>
#include <linux/math64.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/mutex.h>
#include <linux/slab.h>
#include <linux/version.h>

#include "sms_sensor_ioctl.h"

#define DRIVER_NAME "sms_sensor"
#define DEFAULT_INTERVAL_MS 100
#define MIN_INTERVAL_MS 1
#define MAX_INTERVAL_MS 60000

static DEFINE_MUTEX(sensor_lock);

static unsigned int min_interval_ms = DEFAULT_INTERVAL_MS;
static u64 read_count;
static u64 start_time_ms;
static unsigned int last_temperature = 15000;
static unsigned int last_humidity = 30000;
static u64 last_read_ms;
static struct proc_dir_entry *stats_entry;

static int sms_open(struct inode *inode, struct file *file)
{
    return 0;
}

static ssize_t sms_read(struct file *file,
                        char __user *buffer,
                        size_t count,
                        loff_t *offset)
{
    char data[128];
    int len;
    u32 random_temp, random_hum;
    u64 now_ms;
    unsigned int temperature, humidity;

    if (count == 0)
        return 0;

    mutex_lock(&sensor_lock);

    if (*offset > 0) {
        mutex_unlock(&sensor_lock);
        return 0;
    }

    now_ms = ktime_to_ms(ktime_get());

    if (last_read_ms != 0 &&
        now_ms - last_read_ms < min_interval_ms) {
        mutex_unlock(&sensor_lock);
        return -EAGAIN;
    }

    random_temp = get_random_u32();
    random_hum = get_random_u32();

    temperature = 15000 + (random_temp % 30001);

    humidity = 30000 + (random_hum % 60001);

    read_count++;
    last_temperature = temperature;
    last_humidity = humidity;
    last_read_ms = now_ms;

    len = scnprintf(data, sizeof(data),
                    "%llu,%u.%03u,%u.%03u\n",
                    (unsigned long long)now_ms,
                    temperature / 1000, temperature % 1000,
                    humidity / 1000, humidity % 1000);

    mutex_unlock(&sensor_lock);

    if (len > count)
        return -EINVAL;

    if (copy_to_user(buffer, data, len))
        return -EFAULT;

    *offset += len;
    return len;
}

static long sms_ioctl(struct file *file,
                      unsigned int cmd,
                      unsigned long arg)
{
    unsigned int interval;

    if (cmd != SMS_SET_INTERVAL)
        return -ENOTTY;

    if (copy_from_user(&interval,
                       (unsigned int __user *)arg,
                       sizeof(interval)))
        return -EFAULT;

    if (interval < MIN_INTERVAL_MS ||
        interval > MAX_INTERVAL_MS)
        return -EINVAL;

    mutex_lock(&sensor_lock);
    min_interval_ms = interval;
    mutex_unlock(&sensor_lock);

    return 0;
}

static int sms_stats_show(struct seq_file *m, void *v)
{
    u64 now_ms;

    mutex_lock(&sensor_lock);

    now_ms = ktime_to_ms(ktime_get());

    seq_printf(m, "read_count: %llu\n",
               (unsigned long long)read_count);
    seq_printf(m, "last_temperature: %u.%03u\n",
               last_temperature / 1000, last_temperature % 1000);
    seq_printf(m, "last_humidity: %u.%03u\n",
               last_humidity / 1000, last_humidity % 1000);
    seq_printf(m, "uptime_seconds: %llu\n",
               (unsigned long long)
               div_u64(now_ms - start_time_ms, 1000));

    mutex_unlock(&sensor_lock);
    return 0;
}

static int sms_stats_open(struct inode *inode, struct file *file)
{
    return single_open(file, sms_stats_show, NULL);
}

static const struct proc_ops sms_proc_ops = {
    .proc_open = sms_stats_open,
    .proc_read = seq_read,
    .proc_lseek = seq_lseek,
    .proc_release = single_release,
};

static const struct file_operations sms_fops = {
    .owner = THIS_MODULE,
    .open = sms_open,
    .read = sms_read,
    .unlocked_ioctl = sms_ioctl,
    .llseek = no_llseek,
};

static struct miscdevice sms_device = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = DRIVER_NAME,
    .fops = &sms_fops,
    .mode = 0666,
};

static int __init sms_init(void)
{
    int ret;

    start_time_ms = ktime_to_ms(ktime_get());

    ret = misc_register(&sms_device);
    if (ret) {
        pr_err("sms_sensor: failed to register device: %d\n", ret);
        return ret;
    }

    stats_entry = proc_create("sms_stats", 0444, NULL,
                              &sms_proc_ops);
    if (!stats_entry) {
        misc_deregister(&sms_device);
        pr_err("sms_sensor: failed to create /proc/sms_stats\n");
        return -ENOMEM;
    }

    pr_info("sms_sensor: driver loaded, interval=%u ms\n",
            min_interval_ms);
    return 0;
}

static void __exit sms_exit(void)
{
    proc_remove(stats_entry);
    misc_deregister(&sms_device);
    pr_info("sms_sensor: driver unloaded\n");
}

module_init(sms_init);
module_exit(sms_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Embedded Linux Assignment");
MODULE_DESCRIPTION("Simulated temperature and humidity sensor driver");
MODULE_VERSION("1.0");
