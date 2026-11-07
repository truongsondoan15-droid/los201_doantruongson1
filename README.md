# LOS201 - Hệ thống Linux nhúng (Embedded Linux Systems)

**Repository lưu trữ các bài thực hành (Lab) và bài tập cá nhân của môn học Hệ thống Linux nhúng.**

Repository này tổng hợp quá trình thực hành và phát triển hệ thống Linux nhúng trên nền tảng ARM. Nội dung tập trung vào cấu hình Linux Kernel, xây dựng hệ thống khởi động, lập trình Linux Kernel Module, phát triển Device Driver, quản lý hệ thống tập tin, gỡ lỗi, phân tích hiệu năng và đánh giá khả năng lập lịch thời gian thực.

## 1. Môi trường phát triển

| Thành phần | Cấu hình |
|---|---|
| Hệ điều hành máy chủ | Ubuntu Linux |
| Kiến trúc mục tiêu | ARMv7 Cortex-A9 |
| Trình giả lập | QEMU Versatile Express (vexpress-a9) |
| Phiên bản Linux Kernel | 5.15 |
| Bộ biên dịch chéo | `arm-linux-gnueabihf` |
| Công cụ hệ thống | BusyBox |
| Công cụ gỡ lỗi | GDB, Valgrind, strace |
| Công cụ phân tích hiệu năng | perf, cyclictest |
| Ngôn ngữ lập trình | C, Shell Script |

---

## 2. Cấu trúc Repository

```text
LOS201-Embedded-Linux/
│
├── lab01/
│   ├── logs/
│   ├── scripts/
│   └── README.md
│
├── lab02/
│   ├── driver/
│   ├── init-scripts/
│   ├── logs/
│   └── scripts/
│
├── lab03/
│   ├── apps/
│   └── logs/
│
├── asgn01/
│   ├── task1_ioctl/
│   ├── task2_misc/
│   └── logs/
│
├── asgn02/
│   ├── driver/
│   ├── application/
│   ├── tests/
│   └── logs/
│
└── README.md
```

---

# 3. Các bài thực hành (Laboratory Exercises)

## LAB-01: Cấu hình Kernel và khởi động Linux nhúng

### Mục tiêu

- Cấu hình và biên dịch chéo Linux Kernel cho kiến trúc ARM.
- Tìm hiểu vai trò của U-Boot trong quá trình khởi động Linux.
- Tìm hiểu Device Tree và Device Tree Blob (DTB).
- Xây dựng hệ thống tập tin gốc (Root Filesystem) sử dụng BusyBox.
- Tạo ảnh initramfs.
- Khởi động hệ thống Linux nhúng trên QEMU.

### Nội dung thực hiện

- Cấu hình Linux Kernel.
- Biên dịch chéo cho ARM.
- Tìm hiểu Bootloader U-Boot.
- Phân tích quá trình Linux Boot.
- Tạo và cấu hình Device Tree.
- Xây dựng Root Filesystem với BusyBox.
- Khởi động Linux trên QEMU.

### Các tệp trong Repository

```text
lab01/
├── logs/
│   ├── kernel-panic.txt
│   ├── linux-boot-success.txt
│   ├── u-boot-environment.txt
│   └── u-boot-startup.txt
└── scripts/
    └── boot-linux-qemu.sh
```

---

## LAB-02: Device Driver và quản lý hệ thống tập tin

### Mục tiêu

- Xây dựng và quản lý Linux Kernel Module.
- Tìm hiểu Character Device Driver.
- Triển khai các thao tác `open()`, `read()`, `write()` và `release()`.
- Tìm hiểu cơ chế giao tiếp giữa Kernel Space và User Space.
- Thực hành xây dựng và quản lý ProcFS, SysFS.
- Tìm hiểu MTD và hệ thống tập tin JFFS2.
- Cấu hình các tập lệnh khởi tạo BusyBox.

### Nội dung thực hiện

- Phát triển Linux Kernel Module.
- Xây dựng Character Device Driver.
- Triển khai các thao tác đọc và ghi dữ liệu.
- Giao tiếp giữa chương trình User Space và Kernel Space.
- Tạo và kiểm tra giao diện ProcFS, SysFS.
- Quản lý thiết bị lưu trữ MTD.
- Thực hành hệ thống tập tin JFFS2.

### Các tệp trong Repository

```text
lab02/
├── driver/
│   ├── Makefile
│   └── lab2_driver.c
├── init-scripts/
│   ├── test_driver.sh
│   └── test_procfs.sh
├── logs/
│   ├── boot_log.txt
│   ├── driver_test.txt
│   ├── mtd_jffs2.txt
│   └── procfs_test.txt
└── scripts/
    └── run_mtd_test.sh
```

---

## LAB-03: Gỡ lỗi và phân tích hiệu năng hệ thống

### Mục tiêu

- Gỡ lỗi chương trình C bằng GDB.
- Phân tích lỗi quản lý bộ nhớ bằng Valgrind.
- Theo dõi System Calls bằng strace.
- Phân tích hiệu năng CPU bằng perf.
- Đánh giá độ trễ lập lịch thời gian thực bằng cyclictest.

### Nội dung thực hiện

| Công cụ | Chức năng |
|---|---|
| GDB | Gỡ lỗi chương trình, sử dụng breakpoint và phân tích backtrace. |
| Valgrind | Phát hiện lỗi quản lý bộ nhớ và Memory Leak. |
| strace | Theo dõi và phân tích các System Calls. |
| perf | Phân tích hiệu năng CPU và xác định các điểm nghẽn. |
| cyclictest | Đánh giá Scheduling Latency và độ trễ thời gian thực. |

### Các tệp trong Repository

```text
lab03/
├── apps/
│   ├── buggy_app.c
│   ├── leaky_app.c
│   ├── leaky_app_arm_measure.c
│   ├── leaky_app_fixed.c
│   └── perf_target.c
└── logs/
    ├── final_check_summary.txt
    ├── gdb_bug1.txt
    ├── gdb_bug2_3.txt
    ├── gdb_session.txt
    ├── hist_standard.txt
    ├── hist_standard_raw.txt
    └── hist_under_load.txt
```

---

# 4. Các bài tập lớn (Individual Assignments)

## ASSIGNMENT-01: Tìm hiểu và xây dựng Linux Device Driver

### Mục tiêu

- Mở rộng Linux Device Driver với giao diện IOCTL.
- Tìm hiểu và triển khai Misc Device Driver.
- Phân tích các phương pháp đăng ký thiết bị trong Linux Kernel.
- So sánh Character Device Driver và Misc Device Driver.

### Task 1: Triển khai IOCTL Interface

Xây dựng Character Device Driver có hỗ trợ giao tiếp thông qua IOCTL, cho phép chương trình User Space gửi lệnh điều khiển và trao đổi dữ liệu với Kernel Space.

**Các tệp mã nguồn:**

```text
asgn01/task1_ioctl/
├── Makefile
├── asgn1_ctl.c
├── asgn1_driver.c
├── asgn1_ioctl.h
└── test_asgn1.sh
```

### Task 2: Xây dựng Misc Device Driver

Triển khai Counter Driver sử dụng Misc Device Framework của Linux Kernel.

**Các tệp mã nguồn:**

```text
asgn01/task2_misc/
├── Makefile
├── counter_driver.c
└── test_counter.sh
```

### Kết quả kiểm thử

```text
asgn01/logs/
├── dmesg_full.txt
├── qemu_session.txt
├── test_asgn1_output.txt
└── test_counter_output.txt
```

---

# 5. ASSIGNMENT-02: Hệ thống giám sát cảm biến (Sensor Monitoring System)

**Bài tập lớn môn Hệ thống Linux nhúng - Embedded Linux Systems Capstone Assignment**

## 5.1. Giới thiệu đề tài

Xây dựng hệ thống giám sát nhiệt độ và độ ẩm trên nền tảng Embedded Linux bằng cách kết hợp Linux Kernel Driver và ứng dụng đa luồng (Multithreaded Application).

Hệ thống mô phỏng hoạt động thu thập dữ liệu cảm biến, xử lý dữ liệu, phát hiện các điều kiện bất thường, gửi cảnh báo và lưu trữ thông tin.

Đề tài tập trung vào việc tích hợp giữa Kernel Space và User Space, lập trình đa luồng, đồng bộ hóa dữ liệu, giao tiếp liên tiến trình (IPC), quản lý bộ nhớ, gỡ lỗi và đánh giá hiệu năng thời gian thực.

## 5.2. Kiến trúc hệ thống

Hệ thống gồm một Kernel Driver tùy chỉnh và bốn luồng xử lý chính.

```text
             SENSOR MONITORING SYSTEM
                       |
                       v
             +-------------------+
             |   Kernel Driver   |
             |    sms_sensor     |
             +-------------------+
                       |
             +---------+----------+
             |                    |
             v                    v
      /dev/sms_sensor       /proc/sms_stats
             |
             v
      +----------------+
      | Sensor Thread  |
      +----------------+
             |
             v
      +----------------+
      | Processor      |
      | Thread         |
      +----------------+
          |         |
          v         v
      Circular    Alert
       Buffer     Detection
          |         |
          v         v
       Logger    Alert Thread
       Thread        |
          |          v
          v      POSIX Message
       Log File     Queue
```

## 5.3. Task 1: Xây dựng ứng dụng đa luồng (Multithreaded Application)

### A. Custom Kernel Driver

Xây dựng Linux Kernel Driver mô phỏng cảm biến nhiệt độ và độ ẩm.

Các giao diện được cung cấp:

| Giao diện | Chức năng |
|---|---|
| `/dev/sms_sensor` | Character Device dùng để đọc dữ liệu cảm biến. |
| `/proc/sms_stats` | ProcFS cung cấp các thống kê hoạt động của Driver. |
| `SMS_SET_INTERVAL` | IOCTL dùng để cấu hình chu kỳ lấy mẫu dữ liệu. |

### B. Các luồng xử lý chính

| Luồng | Chức năng |
|---|---|
| Sensor Thread | Định kỳ đọc dữ liệu nhiệt độ và độ ẩm từ Kernel Driver. |
| Processor Thread | Tính toán giá trị trung bình trượt (Rolling Average) và phát hiện dữ liệu bất thường. |
| Alert Thread | Nhận và xử lý cảnh báo thông qua POSIX Message Queue. |
| Logger Thread | Ghi dữ liệu cảm biến và sự kiện hệ thống kèm dấu thời gian vào tệp Log. |

### C. Cơ chế đồng bộ hóa

- POSIX Threads (`pthread`): Quản lý và tạo các luồng xử lý.
- Mutex: Bảo vệ dữ liệu dùng chung.
- Condition Variable: Đồng bộ hoạt động giữa các luồng.
- Circular Buffer: Bộ đệm vòng lưu trữ dữ liệu cảm biến.
- POSIX Message Queue: Trao đổi thông tin cảnh báo giữa các luồng.

## 5.4. Task 2: Quản lý bộ nhớ và tích hợp Driver

Đã hoàn thành kiểm thử tích hợp giữa ứng dụng User Space và Kernel Driver trên môi trường ARM/QEMU.

### Kết quả kiểm thử

| Thông số | Kết quả |
|---|---:|
| Nền tảng kiểm thử | QEMU ARMv7 |
| Thời gian thu thập | 60 giây |
| Chu kỳ lấy mẫu | 500 ms |
| Tổng số mẫu thu thập | 117 |
| Lỗi bộ nhớ Valgrind | 0 |
| Memory Leak trên Heap | Không phát hiện |
| Bộ đếm số lần đọc Driver | Đã xác minh |

Kết quả kiểm thử cho thấy hệ thống đã thực hiện thành công việc giao tiếp giữa ứng dụng User Space và Kernel Driver.

Valgrind được sử dụng để kiểm tra lỗi quản lý bộ nhớ và phát hiện Memory Leak trong quá trình thực thi.

## 5.5. Task 3: Gỡ lỗi và phân tích hiệu năng

Sử dụng các công cụ chuyên dụng để kiểm tra hoạt động của ứng dụng đa luồng và phân tích hiệu năng hệ thống.

| Công cụ | Nội dung thực hiện |
|---|---|
| GDB | Gỡ lỗi ứng dụng đa luồng, phân tích Backtrace và theo dõi hoạt động của các Thread. |
| Valgrind | Phân tích lỗi bộ nhớ và kiểm tra Memory Leak. |
| strace | Theo dõi System Calls và phân tích hoạt động của ứng dụng. |
| perf | Phân tích CPU Hotspots và đánh giá hiệu năng xử lý. |

## 5.6. Task 4: Đánh giá lập lịch thời gian thực (Real-Time Scheduling)

Thực hiện so sánh hiệu năng giữa hai chính sách lập lịch của Linux:

- `SCHED_OTHER`: Chính sách lập lịch thông thường của Linux, sử dụng cơ chế chia sẻ thời gian CPU.
- `SCHED_FIFO`: Chính sách lập lịch thời gian thực theo nguyên tắc First-In, First-Out.

Thí nghiệm được thực hiện với 1.092 mẫu đo Jitter cho mỗi chính sách.

### Kết quả Benchmark

| Chỉ số | SCHED_OTHER | SCHED_FIFO |
|---|---:|---:|
| Priority | 0 | 50 |
| Số mẫu đo | 1.092 | 1.092 |
| Jitter nhỏ nhất (µs) | 359 | 251 |
| Jitter trung bình (µs) | 5.627,29 | 5.497,91 |
| Jitter lớn nhất (µs) | 11.315 | 10.873 |
| P99 Jitter (µs) | 10.680 | 10.495 |
| Số lần trễ Deadline | 109 | 108 |

### Phân tích kết quả

Qua kết quả thực nghiệm, `SCHED_FIFO` cho thấy hiệu năng lập lịch tốt hơn `SCHED_OTHER` trong phạm vi kiểm thử.

Các kết quả đáng chú ý:

- Jitter nhỏ nhất giảm từ 359 µs xuống 251 µs.
- Jitter trung bình giảm từ 5.627,29 µs xuống 5.497,91 µs.
- Jitter lớn nhất giảm từ 11.315 µs xuống 10.873 µs.
- P99 Jitter giảm từ 10.680 µs xuống 10.495 µs.
- Số lần trễ Deadline giảm từ 109 xuống 108.

Nhìn chung, `SCHED_FIFO` giúp cải thiện độ trễ lập lịch và độ ổn định thời gian phản hồi trong thí nghiệm. Tuy nhiên, số lần trễ Deadline gần như không thay đổi đáng kể.

## 5.7. Task 5: Báo cáo kỹ thuật và trình diễn hệ thống

Các nội dung cần hoàn thiện trong giai đoạn cuối:

- Xây dựng tài liệu mô tả kiến trúc hệ thống.
- Phân tích cơ chế đồng bộ hóa và giao tiếp giữa các Thread.
- Hoàn thiện báo cáo kỹ thuật (Technical Report).
- Quay video trình diễn hệ thống từ 3-5 phút.
- Đóng gói mã nguồn hoàn chỉnh.
- Tổng hợp Log và kết quả kiểm thử.

### Trạng thái hoàn thành

| Hạng mục | Trạng thái |
|---|---|
| Sensor Kernel Driver | Hoàn thành |
| ARM/QEMU Driver Integration | Hoàn thành |
| Sensor Monitoring Application | Đang phát triển |
| Memory Management Testing | Hoàn thành |
| Debugging & Profiling | Đã có kết quả kiểm thử |
| Real-Time Scheduling Evaluation | Hoàn thành |
| Technical Report | Chưa hoàn thành |
| Demo Video | Chưa hoàn thành |
| Final Source Package | Chưa hoàn thành |

---

# 6. Tổng hợp tiến độ đã xác minh (Verified Progress)

Bảng dưới đây tổng hợp các chức năng đã được kiểm thử và xác nhận hoạt động thành công.

| Hạng mục | Nội dung xác minh | Trạng thái |
|---|---|---|
| ARMv7 Kernel Module Build | Biên dịch Kernel Module cho ARM | PASS |
| QEMU Module Loading | Nạp Module trên QEMU | PASS |
| CSV Sensor Readings | Đọc dữ liệu cảm biến và xuất CSV | PASS |
| ProcFS Statistics | Kiểm tra `/proc/sms_stats` | PASS |
| IOCTL Sampling Configuration | Cấu hình chu kỳ lấy mẫu bằng `SMS_SET_INTERVAL` | PASS |
| Invalid Interval Handling | Từ chối chu kỳ lấy mẫu không hợp lệ | PASS |
| Sampling Interval Enforcement | Kiểm tra việc thực thi chu kỳ lấy mẫu | PASS |
| ARM/QEMU Integration | Kiểm thử tích hợp trong 60 giây | PASS |
| Valgrind Memory Analysis | Không có lỗi bộ nhớ, không phát hiện Heap Leak | PASS |
| Driver Read Counter | Xác minh bộ đếm số lần đọc Driver | PASS |
| Real-Time Scheduling | 1.092 mẫu đo cho mỗi chế độ | HOÀN THÀNH |

**Lưu ý:** Phần A (Kernel Driver) đã được xây dựng và kiểm thử thành công. Phần B (Multithreaded Application) vẫn đang trong quá trình phát triển. Các nội dung kiến trúc và chức năng dự kiến không đồng nghĩa với việc toàn bộ ứng dụng đã được triển khai và xác minh.

---

# 7. Hướng dẫn biên dịch Sensor Kernel Driver

Di chuyển đến thư mục chứa mã nguồn Driver:

```bash
cd asgn02/driver
```

Thực hiện biên dịch cho kiến trúc ARM:

```bash
make arm
```

**Lưu ý:** Đường dẫn đến thư mục mã nguồn Linux Kernel trong Makefile có thể cần điều chỉnh để phù hợp với môi trường Linux Kernel 5.15 trên máy tính cá nhân.

---

# 8. Công nghệ và kiến thức đã áp dụng

Repository này thể hiện quá trình thực hành và vận dụng các kiến thức:

- Embedded Linux Development.
- Linux Kernel 5.15.
- ARMv7 Cross-Compilation.
- QEMU System Emulation.
- Linux Kernel Module Development.
- Character Device Driver.
- IOCTL, ProcFS và SysFS.
- MTD và JFFS2 Filesystem.
- POSIX Multithreading.
- Mutex và Condition Variables.
- POSIX Message Queue.
- GDB và Valgrind.
- strace và perf.
- Real-Time Linux Scheduling.
- Performance và Latency Benchmarking.

---

# 9. Thông tin Repository

**Môn học:** LOS201 - Embedded Linux Systems

**Nội dung:** Laboratory Exercises và Individual Capstone Assignment.

**Nền tảng thực hiện:** Ubuntu Linux, ARMv7 Cortex-A9 và QEMU vexpress-a9.

Repository được xây dựng nhằm phục vụ mục đích học tập, thực hành lập trình Linux Kernel, phát triển hệ thống nhúng và phân tích hiệu năng hệ điều hành.

---

*LOS201 - Embedded Linux Systems | Kernel Development | Embedded Programming | Real-Time Systems*
