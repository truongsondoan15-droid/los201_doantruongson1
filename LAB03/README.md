# LAB-03: Embedded Linux Debugging and Real-Time Performance

## 1. Introduction

This lab focuses on debugging, memory analysis, system call tracing, and real-time performance evaluation in an Embedded Linux environment.

The main purpose is to understand common application errors, analyze Linux system calls, measure application performance, and compare scheduling latency between Standard Linux and PREEMPT_RT kernels.

## 2. Objectives

- Set up an ARM debugging environment using QEMU.
- Analyze memory errors using Valgrind.
- Trace system calls using strace.
- Measure application performance using perf.
- Evaluate real-time performance using cyclictest.
- Compare Standard Linux kernel and PREEMPT_RT kernel.

## 3. Environment and Tools

| Component | Description |
|---|---|
| Host OS | Ubuntu Linux |
| Host Architecture | x86_64 |
| ARM Architecture | ARM Cortex-A9 |
| Emulator | QEMU |
| ARM Compiler | arm-linux-gnueabihf-gcc |
| Host Compiler | GCC |
| Memory Analysis | Valgrind |
| System Call Tracing | strace |
| Performance Analysis | perf |
| Real-time Testing | cyclictest |
| PREEMPT_RT Kernel | 7.0.0-38-realtime |

## 4. Repository Structure

```text
Lab3/
│
├── app/
│   ├── buggy_app.c
│   ├── buggy_app
│   ├── buggy_app_host
│   └── strace_log.txt
│
├── logs/
│   ├── strace_log.txt
│   ├── perf_stat.txt
│   ├── cyclictest_standard.txt
│   └── cyclictest_realtime.txt
│
├── output/
│   └── initramfs_lab3.cpio.gz
│
├── report/
│   └── Lab3_Report.pdf
│
└── README.md
```

## 5. Lab Implementation

### A. ARM Remote Debugging

- Prepared the ARM debugging environment.
- Used QEMU to emulate the ARM Cortex-A9 platform.
- Prepared the ARM application for debugging.

**Note:** Section A.2 (GDB Remote Debugging) was skipped.

### B. Memory Error Detection with Valgrind

Valgrind was used to analyze memory-related errors in `buggy_app_host`.

The application contains the following issues:

1. Out-of-bounds read in `process_data()`.
2. Use-after-free in `create_message()`.
3. Signed integer overflow in `calculate()`.

Valgrind reported:
- 47 errors from 8 contexts.
- Invalid and uninitialized memory accesses.
- No outstanding heap blocks at program exit.

### C. System Performance Analysis

#### C.1 System Call Tracing with strace

Used strace to monitor system calls made by the application.

The trace includes:
- `execve()`
- `openat()`
- `read()`
- `write()`
- `mmap()`
- `munmap()`
- `close()`
- `exit_group()`

Log file: `logs/strace_log.txt`

#### C.2 Performance Measurement with perf

Used perf to collect performance statistics.

Results:

| Metric | Result |
|---|---:|
| Task Clock | 0.54 ms |
| Context Switches | 0 |
| CPU Migrations | 0 |
| Page Faults | 62 |
| Elapsed Time | 1.69 ms |

Log file: `logs/perf_stat.txt`

### D. Real-Time Performance Testing

Used cyclictest to evaluate scheduling latency.

Both tests used:
- FIFO scheduling policy.
- Priority: 80.
- Interval: 1000 µs.
- Number of loops: 10,000.

#### D.1 Standard Linux Kernel

Results:

| Metric | Value |
|---|---:|
| Minimum Latency | 2 µs |
| Average Latency | 3 µs |
| Maximum Latency | 117 µs |

Log file: `logs/cyclictest_standard.txt`

#### D.2 PREEMPT_RT Kernel

Installed and booted the PREEMPT_RT kernel.

Kernel version:

```text
7.0.0-38-realtime
```

Verified configuration:

```text
CONFIG_PREEMPT_RT=y
```

Results:

| Metric | Value |
|---|---:|
| Minimum Latency | 2 µs |
| Average Latency | 3 µs |
| Maximum Latency | 93 µs |

Log file: `logs/cyclictest_realtime.txt`

## 6. Performance Comparison

| Metric | Standard Kernel | PREEMPT_RT Kernel |
|---|---:|---:|
| Minimum Latency | 2 µs | 2 µs |
| Average Latency | 3 µs | 3 µs |
| Maximum Latency | 117 µs | 93 µs |

### Analysis

The PREEMPT_RT kernel achieved a lower maximum latency than the Standard Linux kernel.

- Maximum latency decreased from 117 µs to 93 µs.
- Improvement: approximately 20.5%.
- Minimum latency remained unchanged.
- Average latency remained unchanged.

These results are based on individual test runs and may vary depending on system load and hardware conditions.

## 7. Conclusion

This lab provided practical experience with Embedded Linux debugging and performance analysis.

The experiments demonstrated how to:
- Identify memory errors using Valgrind.
- Monitor system calls using strace.
- Measure application performance using perf.
- Evaluate scheduling latency using cyclictest.
- Compare Standard Linux and PREEMPT_RT kernel behavior.

The experimental results showed that PREEMPT_RT achieved a lower maximum scheduling latency in the recorded test.

## 8. Notes

- Section A.2 was intentionally skipped.
- The perf measurement was performed on the Ubuntu host.
- The cyclictest measurements were performed on the Ubuntu host using Standard and PREEMPT_RT kernels.
- The application source code and experimental logs are included in this repository.
