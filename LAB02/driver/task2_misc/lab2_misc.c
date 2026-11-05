#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/proc_fs.h>
#include <linux/mutex.h>

#define DEVICE_NAME "lab2_misc"
#define PROC_NAME   "lab2_misc"
#define BUFFER_SIZE 1024

static char device_buffer[BUFFER_SIZE];
static size_t buffer_len;
static DEFINE_MUTEX(buffer_mutex);

/* ================= MISC DEVICE ================= */

static int misc_open(struct inode *inode, struct file *file)
{
    pr_info("lab2_misc: device opened\n");
    return 0;
}

static int misc_release(struct inode *inode, struct file *file)
{
    pr_info("lab2_misc: device closed\n");
    return 0;
}

static ssize_t misc_read(struct file *file,
                         char __user *user_buf,
                         size_t count,
                         loff_t *offset)
{
    size_t len;
    ssize_t ret;

    if (mutex_lock_interruptible(&buffer_mutex))
        return -ERESTARTSYS;

    len = buffer_len;

    if (*offset >= len) {
        ret = 0;
        goto out;
    }

    if (count > len - *offset)
        count = len - *offset;

    if (copy_to_user(user_buf, device_buffer + *offset, count)) {
        ret = -EFAULT;
        goto out;
    }

    *offset += count;
    ret = count;

out:
    mutex_unlock(&buffer_mutex);
    return ret;
}

static ssize_t misc_write(struct file *file,
                          const char __user *user_buf,
                          size_t count,
                          loff_t *offset)
{
    size_t len = min(count, (size_t)BUFFER_SIZE);
    ssize_t ret;

    if (mutex_lock_interruptible(&buffer_mutex))
        return -ERESTARTSYS;

    if (copy_from_user(device_buffer, user_buf, len)) {
        ret = -EFAULT;
        goto out;
    }

    buffer_len = len;
    *offset = len;

    pr_info("lab2_misc: received %zu bytes\n", len);
    ret = len;

out:
    mutex_unlock(&buffer_mutex);
    return ret;
}

static const struct file_operations misc_fops = {
    .owner   = THIS_MODULE,
    .open    = misc_open,
    .release = misc_release,
    .read    = misc_read,
    .write   = misc_write,
    .llseek  = default_llseek,
};

static struct miscdevice lab2_misc_device = {
    .minor = MISC_DYNAMIC_MINOR,
    .name  = DEVICE_NAME,
    .fops  = &misc_fops,
    .mode  = 0666,
};

/* ================= PROCFS ================= */

static ssize_t proc_read(struct file *file,
                         char __user *user_buf,
                         size_t count,
                         loff_t *offset)
{
    size_t len;
    ssize_t ret;

    if (mutex_lock_interruptible(&buffer_mutex))
        return -ERESTARTSYS;

    len = buffer_len;

    if (*offset >= len) {
        ret = 0;
        goto out;
    }

    if (count > len - *offset)
        count = len - *offset;

    if (copy_to_user(user_buf, device_buffer + *offset, count)) {
        ret = -EFAULT;
        goto out;
    }

    *offset += count;
    ret = count;

out:
    mutex_unlock(&buffer_mutex);
    return ret;
}

static ssize_t proc_write(struct file *file,
                          const char __user *user_buf,
                          size_t count,
                          loff_t *offset)
{
    size_t len = min(count, (size_t)BUFFER_SIZE);
    ssize_t ret;

    if (mutex_lock_interruptible(&buffer_mutex))
        return -ERESTARTSYS;

    if (copy_from_user(device_buffer, user_buf, len)) {
        ret = -EFAULT;
        goto out;
    }

    buffer_len = len;
    ret = len;

out:
    mutex_unlock(&buffer_mutex);
    return ret;
}

static const struct proc_ops proc_fops = {
    .proc_read  = proc_read,
    .proc_write = proc_write,
};

/* ================= MODULE INIT / EXIT ================= */

static struct proc_dir_entry *lab2_proc_entry;

static int __init lab2_misc_init(void)
{
    int ret;

    ret = misc_register(&lab2_misc_device);
    if (ret) {
        pr_err("lab2_misc: failed to register misc device\n");
        return ret;
    }

    lab2_proc_entry = proc_create(
        PROC_NAME, 0666, NULL, &proc_fops
    );

    if (!lab2_proc_entry) {
        misc_deregister(&lab2_misc_device);
        pr_err("lab2_misc: failed to create proc entry\n");
        return -ENOMEM;
    }

    pr_info("lab2_misc: registered successfully\n");
    pr_info("lab2_misc: device /dev/%s\n", DEVICE_NAME);
    pr_info("lab2_misc: proc /proc/%s\n", PROC_NAME);

    return 0;
}

static void __exit lab2_misc_exit(void)
{
    proc_remove(lab2_proc_entry);
    misc_deregister(&lab2_misc_device);

    pr_info("lab2_misc: unregistered successfully\n");
}

module_init(lab2_misc_init);
module_exit(lab2_misc_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Student");
MODULE_DESCRIPTION("LAB-02 Misc Device Driver with read, write and procfs");

