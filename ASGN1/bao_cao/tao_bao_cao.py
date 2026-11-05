#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted, KeepTogether
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT = os.path.join(
    os.path.dirname(__file__),
    "SE200908_ASGN1_BaoCao.pdf"
)

# Font hỗ trợ tiếng Việt
font_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

if os.path.exists(font_regular):
    pdfmetrics.registerFont(TTFont("DejaVu", font_regular))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", font_bold))
    FONT = "DejaVu"
    FONT_BOLD = "DejaVu-Bold"
else:
    FONT = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="TitleVN", fontName=FONT_BOLD, fontSize=20,
    leading=28, alignment=TA_CENTER, spaceAfter=20
))
styles.add(ParagraphStyle(
    name="HeadingVN", fontName=FONT_BOLD, fontSize=14,
    leading=20, spaceBefore=14, spaceAfter=8,
    textColor=colors.HexColor("#17365D")
))
styles.add(ParagraphStyle(
    name="SubHeadingVN", fontName=FONT_BOLD, fontSize=11,
    leading=16, spaceBefore=8, spaceAfter=5
))
styles.add(ParagraphStyle(
    name="BodyVN", fontName=FONT, fontSize=9.5,
    leading=15, alignment=TA_LEFT, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="SmallVN", fontName=FONT, fontSize=8,
    leading=12, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="CodeVN", fontName="Courier", fontSize=7,
    leading=9, leftIndent=8, spaceAfter=8
))

story = []

def add_title(text):
    story.append(Paragraph(text, styles["TitleVN"]))

def add_heading(text):
    story.append(Paragraph(text, styles["HeadingVN"]))

def add_subheading(text):
    story.append(Paragraph(text, styles["SubHeadingVN"]))

def add_body(text):
    story.append(Paragraph(text, styles["BodyVN"]))

def add_code(text):
    story.append(Preformatted(text, styles["CodeVN"]))

def add_bullet(text):
    story.append(Paragraph("• " + text, styles["BodyVN"]))

def get_files(folder):
    result = []
    if os.path.isdir(folder):
        for current, dirs, files in os.walk(folder):
            dirs.sort()
            for filename in sorted(files):
                path = os.path.join(current, filename)
                relative = os.path.relpath(path, ROOT)
                result.append((relative, os.path.getsize(path)))
    return result

def read_logs():
    log_dir = os.path.join(ROOT, "logs")
    collected = []
    if os.path.isdir(log_dir):
        for current, dirs, files in os.walk(log_dir):
            dirs.sort()
            for filename in sorted(files):
                path = os.path.join(current, filename)
                try:
                    with open(path, "r", errors="replace") as f:
                        content = f.read(5000).strip()
                    if content:
                        collected.append((os.path.relpath(path, ROOT), content))
                except Exception:
                    pass
    return collected

# Trang bìa
story.append(Spacer(1, 2.5 * cm))
add_title("BÁO CÁO BÀI TẬP LỚN ASGN1")
story.append(Spacer(1, 0.8 * cm))
story.append(Paragraph(
    "MÔN HỌC: EMBEDDED LINUX - LOS201",
    ParagraphStyle(
        "Course", fontName=FONT_BOLD, fontSize=13,
        alignment=TA_CENTER, leading=20
    )
))
story.append(Spacer(1, 2 * cm))

info = [
    ["Thông tin", "Nội dung"],
    ["Họ và tên", "Doan Truong Son"],
    ["Mã sinh viên", "SE200908"],
    ["Môn học", "LOS201 - Embedded Linux"],
    ["Bài thực hiện", "ASGN1"],
    ["Ngày tạo báo cáo", datetime.now().strftime("%d/%m/%Y")],
]
table = Table(info, colWidths=[5 * cm, 10 * cm])
table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), FONT),
    ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
]))
story.append(table)
story.append(Spacer(1, 2 * cm))
story.append(Paragraph(
    "BÁO CÁO PHỤC VỤ HỌC TẬP",
    ParagraphStyle("FooterCover", fontName=FONT, fontSize=10,
                   alignment=TA_CENTER)
))
story.append(PageBreak())

# 1. Giới thiệu
add_heading("1. GIỚI THIỆU")
add_body(
    "Bài tập ASGN1 nhằm củng cố kiến thức về lập trình Linux Kernel, "
    "xây dựng và kiểm thử device driver trong môi trường Embedded Linux. "
    "Bài làm được tổ chức thành hai phần chính: Task 1 sử dụng giao diện "
    "ioctl và Task 2 sử dụng miscellaneous device."
)
add_body(
    "Mục tiêu là hiểu cách một ứng dụng ở user space giao tiếp với kernel "
    "thông qua device file, cách đăng ký driver, xử lý yêu cầu từ chương "
    "trình người dùng và kiểm tra kết quả hoạt động."
)

# 2. Môi trường
add_heading("2. MÔI TRƯỜNG THỰC HIỆN")
env = [
    ["Thành phần", "Thông tin"],
    ["Hệ điều hành máy phát triển", "Ubuntu Linux"],
    ["Kiến trúc mục tiêu", "ARM Linux (kiểm tra theo file build thực tế)"],
    ["Trình biên dịch", "arm-linux-gnueabihf-gcc (nếu dùng cross compiler)"],
    ["Ngôn ngữ", "C"],
    ["Nền tảng", "Linux Kernel / Embedded Linux"],
]
t = Table(env, colWidths=[6 * cm, 9 * cm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), FONT),
    ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(t)
add_body(
    "Lưu ý: cần cập nhật phiên bản kernel, compiler và môi trường chạy "
    "theo kết quả thực tế của máy dùng để thực hiện bài."
)

# 3. Cấu trúc
add_heading("3. CẤU TRÚC THƯ MỤC")
add_code(
"""ASGN1/
├── logs/       - Nhật ký chạy và kết quả kiểm thử
├── output/     - File đầu ra sau khi build
├── task1/      - Mã nguồn và chương trình kiểm thử Task 1
├── task2/      - Mã nguồn và chương trình kiểm thử Task 2
├── bao_cao/    - Báo cáo PDF và script tạo báo cáo
└── README.md   - Hướng dẫn tổng quan"""
)
add_body("Các tệp hiện có trong từng thư mục được thống kê tự động bên dưới.")

for folder in ["task1", "task2", "logs", "output"]:
    add_subheading("3.%s. Nội dung %s/" % (
        ["task1", "task2", "logs", "output"].index(folder) + 1, folder
    ))
    files = get_files(os.path.join(ROOT, folder))
    if files:
        for name, size in files:
            add_bullet("%s (%d bytes)" % (name, size))
    else:
        add_body("Chưa tìm thấy tệp trong thư mục này tại thời điểm tạo báo cáo.")

# 4. Task 1
add_heading("4. TASK 1 - CHARACTER DEVICE VÀ IOCTL")
add_body(
    "Task 1 tập trung vào xây dựng character device driver và cung cấp "
    "giao diện ioctl để ứng dụng user space gửi các lệnh điều khiển đến kernel."
)
add_subheading("4.1. Nguyên lý hoạt động")
add_code(
"""User application
       |
       | open() / ioctl() / close()
       v
Device file (/dev/...)
       |
       v
Character device driver
       |
       v
Kernel xử lý lệnh và trả kết quả
       |
       v
User application nhận kết quả"""
)
add_subheading("4.2. Các thành phần cần trình bày")
add_bullet("Hàm đăng ký và hủy đăng ký character device.")
add_bullet("Các hàm file operation như open, release và unlocked_ioctl.")
add_bullet("Các mã lệnh ioctl và cấu trúc dữ liệu trao đổi giữa user space và kernel.")
add_bullet("Chương trình user space mở device file và gửi lệnh kiểm thử.")
add_subheading("4.3. Kết quả kiểm thử")
add_body(
    "[BỔ SUNG] Dán kết quả chạy chương trình Task 1, thông báo nạp driver, "
    "tạo device node và kết quả từng lệnh ioctl tại đây. Chỉ ghi PASS khi "
    "đã thực sự chạy và xác nhận kết quả."
)

# 5. Task 2
add_heading("5. TASK 2 - MISCELLANEOUS DEVICE DRIVER")
add_body(
    "Task 2 sử dụng cơ chế miscellaneous device của Linux để đăng ký "
    "một thiết bị đơn giản. Cơ chế này giúp giảm phần mã đăng ký major/minor "
    "so với cách triển khai character device truyền thống."
)
add_subheading("5.1. Nguyên lý hoạt động")
add_code(
"""User application
       |
       | open() / read() / write() / ioctl()
       v
Misc device file (/dev/...)
       |
       v
Miscellaneous device driver
       |
       v
Các hàm xử lý được driver cung cấp"""
)
add_subheading("5.2. Các thành phần cần trình bày")
add_bullet("Khai báo cấu trúc miscdevice.")
add_bullet("Đăng ký thiết bị bằng misc_register().")
add_bullet("Hủy đăng ký bằng misc_deregister().")
add_bullet("Khai báo và triển khai các file operation cần thiết.")
add_bullet("Chương trình user space dùng device file để kiểm tra driver.")
add_subheading("5.3. Kết quả kiểm thử")
add_body(
    "[BỔ SUNG] Dán log build, nạp driver, kiểm tra device file và kết quả "
    "chương trình kiểm thử Task 2. Ghi rõ lệnh đã chạy và kết quả thực tế."
)

# 6. Logs
add_heading("6. NHẬT KÝ VÀ KẾT QUẢ THỰC NGHIỆM")
logs = read_logs()
if logs:
    for name, content in logs:
        add_subheading("Log: " + name)
        add_code(content[:3500])
        if len(content) > 3500:
            add_body("[Log đã được rút gọn khi đưa vào báo cáo.]")
else:
    add_body(
        "Chưa tìm thấy nội dung log trong thư mục logs/. "
        "Cần lưu kết quả thực tế vào ASGN1/logs/ rồi chạy lại script."
    )

# 7. Phân tích
add_heading("7. PHÂN TÍCH VÀ CÂU HỎI")
add_subheading("7.1. Vì sao không nên truy cập trực tiếp con trỏ user space?")
add_body(
    "Kernel và user space hoạt động trong hai không gian địa chỉ khác nhau. "
    "Con trỏ do ứng dụng cung cấp không thể được kernel sử dụng như con trỏ "
    "kernel thông thường. Driver cần dùng các hàm an toàn như copy_to_user() "
    "và copy_from_user() để kiểm tra và sao chép dữ liệu giữa hai không gian."
)
add_subheading("7.2. Vai trò của mutex trong device driver")
add_body(
    "Mutex dùng để bảo vệ vùng dữ liệu hoặc thao tác dùng chung khi nhiều "
    "tiến trình có thể truy cập đồng thời. Việc khóa và mở khóa đúng cách "
    "giúp tránh race condition và bảo đảm tính nhất quán của dữ liệu."
)
add_subheading("7.3. Character device và miscellaneous device")
add_body(
    "Character device truyền thống cho phép driver quản lý việc đăng ký "
    "major/minor và tạo device node. Miscellaneous device là một cơ chế "
    "đơn giản hóa cho các thiết bị ký tự nhỏ, thường dùng chung major "
    "được hệ thống dành cho misc device."
)
add_subheading("7.4. Ý nghĩa của file operation")
add_body(
    "Các hàm open, read, write, release và ioctl là giao diện để ứng dụng "
    "user space tương tác với driver. Khi ứng dụng gọi system call trên "
    "device file, kernel chuyển yêu cầu đến hàm tương ứng mà driver đăng ký."
)
add_subheading("7.5. Xử lý lỗi khi nạp driver")
add_body(
    "Nếu thao tác nạp module thất bại, cần kiểm tra mã trả về và log kernel "
    "bằng dmesg. Trong script khởi động, việc hệ thống có tiếp tục boot hay "
    "không phụ thuộc cách script xử lý lỗi và cấu hình init; không thể kết "
    "luận chỉ từ việc insmod thất bại."
)

# 8. Khó khăn
add_heading("8. KHÓ KHĂN VÀ CÁCH KHẮC PHỤC")
add_body(
    "[BỔ SUNG KHÓ KHĂN THỰC TẾ SỐ 1] Mô tả lỗi đã gặp, nguyên nhân xác định "
    "được, cách xử lý và kết quả sau khi sửa."
)
add_body(
    "[BỔ SUNG KHÓ KHĂN THỰC TẾ SỐ 2] Mô tả lỗi thứ hai, các bước kiểm tra, "
    "cách khắc phục và kết quả."
)
add_body(
    "Không nên giữ nguyên hai dòng hướng dẫn này khi nộp bài. Hãy thay bằng "
    "các vấn đề thực tế trong quá trình build hoặc kiểm thử."
)

# 9. Kết luận
add_heading("9. KẾT LUẬN")
add_body(
    "Thông qua ASGN1, sinh viên có cơ hội thực hành xây dựng Linux device "
    "driver và tìm hiểu cơ chế giao tiếp giữa user space và kernel space. "
    "Hai cách tiếp cận character device và miscellaneous device cho thấy "
    "các lựa chọn khác nhau khi triển khai thiết bị trong Linux."
)
add_body(
    "Báo cáo cần được hoàn thiện bằng log thực tế, kết quả kiểm thử và "
    "các khó khăn đã gặp trước khi nộp."
)

# Footer và số trang
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.drawString(2 * cm, 1.2 * cm, "ASGN1 - Doan Truong Son - SE200908")
    canvas.drawRightString(19 * cm, 1.2 * cm, "Trang %d" % doc.page)
    canvas.restoreState()

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2 * cm,
    bottomMargin=2 * cm
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)

print("TAO BAO CAO ASGN1 THANH CONG!")
print("File:", OUTPUT)
print("Kich thuoc: %.1f KB" % (os.path.getsize(OUTPUT) / 1024))
print("Luu y: Hay bo sung log va kho khan thuc te truoc khi nop.")
