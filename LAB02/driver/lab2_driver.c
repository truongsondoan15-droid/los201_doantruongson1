
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/init.h>
#include <linux/device.h>
#include <linux/mutex.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>

#define DEVICE_NAME "lab2"
#define CLASS_NAME "lab2_class"
#define BUF_SIZE 256
#define LAB2_MAJOR 240

static int major_number = LAB2_MAJOR;
static struct class *lab2_class;
static struct device *lab2_device;
static char device_buffer[BUF_SIZE];
static size_t data_size;
static bool reverse_read;
static unsigned long overwrite_count;
static DEFINE_MUTEX(lab2_mutex);
static struct proc_dir_entry *lab2_proc;

static int lab2_open(struct inode *inode, struct file *file)
{
    pr_info("lab2: device opened\n");
    return 0;
}

static int lab2_release(struct inode *inode, struct file *file)
{
    pr_info("lab2: device closed\n");
    return 0;
}

static ssize_t lab2_read(struct file *file, char __user *buffer,
                         size_t count, loff_t *offset)
{
    size_t len, i;
    char temp[BUF_SIZE];

    if (*offset < 0)
        return -EINVAL;

    mutex_lock(&lab2_mutex);

    if ((size_t)*offset >= data_size) {
        mutex_unlock(&lab2_mutex);
        return 0;
    }

    len = min(count, data_size - (size_t)*offset);

    if (reverse_read) {
        for (i = 0; i < len; i++)
            temp[i] = device_buffer[data_size - 1 - (size_t)*offset - i];

        if (copy_to_user(buffer, temp, len)) {
            mutex_unlock(&lab2_mutex);
            return -EFAULT;
        }
    } else {
        if (copy_to_user(buffer, device_buffer + *offset, len)) {
            mutex_unlock(&lab2_mutex);
            return -EFAULT;
        }
    }

    *offset += len;
    mutex_unlock(&lab2_mutex);
    return len;
}

static ssize_t lab2_write(struct file *file, const char __user *buffer,
                          size_t count, loff_t *offset)
{
    size_t len = min(count, (size_t)BUF_SIZE - 1);
    char temp[BUF_SIZE];

    if (copy_from_user(temp, buffer, len))
        return -EFAULT;

    mutex_lock(&lab2_mutex);

    if (data_size > 0)
        overwrite_count++;

    memcpy(device_buffer, temp, len);
    device_buffer[len] = '\0';
    data_size = len;

    mutex_unlock(&lab2_mutex);

    pr_info("lab2: received %zu bytes\n", len);
    return len;
}

static loff_t lab2_llseek(struct file *file, loff_t offset, int whence)
{
    loff_t new_pos;
    loff_t max_size;

    mutex_lock(&lab2_mutex);
    max_size = data_size;

    switch (whence) {
    case SEEK_SET:
        new_pos = offset;
        break;
    case SEEK_CUR:
        new_pos = file->f_pos + offset;
        break;
    case SEEK_END:
        new_pos = max_size + offset;
        break;
    default:
        mutex_unlock(&lab2_mutex);
        return -EINVAL;
    }

    if (new_pos < 0 || new_pos > max_size) {
        mutex_unlock(&lab2_mutex);
        return -EINVAL;
    }

    file->f_pos = new_pos;
    mutex_unlock(&lab2_mutex);
    return new_pos;
}

static ssize_t reverse_read_show(struct device *dev,
                                 struct device_attribute *attr, char *buf)
{
    ssize_t ret;

    mutex_lock(&lab2_mutex);
    ret = sysfs_emit(buf, "%d\n", reverse_read ? 1 : 0);
    mutex_unlock(&lab2_mutex);

    return ret;
}

static ssize_t reverse_read_store(struct device *dev,
                                  struct device_attribute *attr,
                                  const char *buf, size_t count)
{
    bool value;
    int ret;

    ret = kstrtobool(buf, &value);
    if (ret)
        return -EINVAL;

    mutex_lock(&lab2_mutex);
    reverse_read = value;
    mutex_unlock(&lab2_mutex);

    return count;
}

static DEVICE_ATTR_RW(reverse_read);

static ssize_t overwrite_count_show(struct device *dev,
                                    struct device_attribute *attr, char *buf)
{
    ssize_t ret;

    mutex_lock(&lab2_mutex);
    ret = sysfs_emit(buf, "%lu\n", overwrite_count);
    mutex_unlock(&lab2_mutex);

    return ret;
}

static DEVICE_ATTR_RO(overwrite_count);

static int lab2_proc_show(struct seq_file *m, void *v)
{
    mutex_lock(&lab2_mutex);
    seq_printf(m, "Device         : %s\n", DEVICE_NAME);
    seq_printf(m, "Major          : %d\n", major_number);
    seq_printf(m, "Buffer size    : %zu\n", data_size);
    seq_printf(m, "Reverse read   : %d\n", reverse_read ? 1 : 0);
    seq_printf(m, "Overwrites     : %lu\n", overwrite_count);
    mutex_unlock(&lab2_mutex);

    return 0;
}

static int lab2_proc_open(struct inode *inode, struct file *file)
{
    return single_open(file, lab2_proc_show, NULL);
}

static const struct proc_ops lab2_proc_ops = {
    .proc_open = lab2_proc_open,
    .proc_read = seq_read,
    .proc_lseek = seq_lseek,
    .proc_release = single_release,
};

static const struct file_operations lab2_fops = {
    .owner = THIS_MODULE,
    .open = lab2_open,
    .release = lab2_release,
    .read = lab2_read,
    .write = lab2_write,
    .llseek = lab2_llseek,
};

static int __init lab2_init(void)
{
    int ret;

data_size = 0;
overwrite_count = 0;
reverse_read = 0;

ret = register_chrdev(LAB2_MAJOR, DEVICE_NAME, &lab2_fops);
if (ret < 0)
    return ret;

major_number = LAB2_MAJOR;

    lab2_class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(lab2_class)) {
        ret = PTR_ERR(lab2_class);
        unregister_chrdev(LAB2_MAJOR, DEVICE_NAME);
        return ret;
    }

    lab2_device = device_create(lab2_class, NULL,
                                MKDEV(major_number, 0),
                                NULL, DEVICE_NAME);
    if (IS_ERR(lab2_device)) {
        ret = PTR_ERR(lab2_device);
        class_destroy(lab2_class);
        unregister_chrdev(LAB2_MAJOR, DEVICE_NAME);
        return ret;
    }

    ret = device_create_file(lab2_device, &dev_attr_reverse_read);
    if (ret)
        goto error_device;

    ret = device_create_file(lab2_device, &dev_attr_overwrite_count);
    if (ret)
        goto error_reverse;

    lab2_proc = proc_create("lab2_info", 0444, NULL, &lab2_proc_ops);
    if (!lab2_proc) {
        ret = -ENOMEM;
        goto error_overwrite;
    }

    pr_info("lab2: module loaded, major=%d\n", major_number);
    return 0;

error_overwrite:
    device_remove_file(lab2_device, &dev_attr_overwrite_count);
error_reverse:
    device_remove_file(lab2_device, &dev_attr_reverse_read);
error_device:
    device_destroy(lab2_class, MKDEV(major_number, 0));
    class_destroy(lab2_class);
    unregister_chrdev(LAB2_MAJOR, DEVICE_NAME);
    return ret;
}

static void __exit lab2_exit(void)
{
    proc_remove(lab2_proc);
    device_remove_file(lab2_device, &dev_attr_overwrite_count);
    device_remove_file(lab2_device, &dev_attr_reverse_read);
    device_destroy(lab2_class, MKDEV(major_number, 0));
    class_destroy(lab2_class);
    unregister_chrdev(LAB2_MAJOR, DEVICE_NAME);

    pr_info("lab2: module unloaded\n");
}

module_init(lab2_init);
module_exit(lab2_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Embedded Linux Lab");
MODULE_DESCRIPTION("LAB-02 character device driver");
MODULE_VERSION("1.0");

