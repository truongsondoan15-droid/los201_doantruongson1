# -*- coding: utf-8 -*-

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, Preformatted
)

OUTPUT = "LAB02/bao_cao/SE200908_Lab02_BaoCao.pdf"

os.makedirs("LAB02/bao_cao", exist_ok=True)

# Font tieng Viet
pdfmetrics.registerFont(TTFont(
    "VN", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
))
pdfmetrics.registerFont(TTFont(
    "VN-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
))

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="Cover",
    fontName="VN-Bold",
    fontSize=21,
    leading=30,
    alignment=1,
    textColor=colors.darkblue,
    spaceAfter=15
))

styles.add(ParagraphStyle(
    name="H1",
    fontName="VN-Bold",
    fontSize=14,
    leading=20,
    textColor=colors.darkblue,
    spaceBefore=14,
    spaceAfter=8
))

styles.add(ParagraphStyle(
    name="H2",
    fontName="VN-Bold",
    fontSize=10,
    leading=15,
    spaceBefore=8,
    spaceAfter=5
))

styles.add(ParagraphStyle(
    name="Body",
    fontName="VN",
    fontSize=9,
    leading=14,
    spaceAfter=7
))

styles.add(ParagraphStyle(
    name="CodeVN",
    fontName="Courier",
    fontSize=7,
    leading=10,
    backColor=colors.whitesmoke,
    borderPadding=7
))

story = []

def p(text):
    story.append(Paragraph(text, styles["Body"]))

def h1(text):
    story.append(Paragraph(text, styles["H1"]))

def h2(text):
    story.append(Paragraph(text, styles["H2"]))

def code(text):
    story.append(Preformatted(text.strip(), styles["CodeVN"]))
    story.append(Spacer(1, 8))

def make_table(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "VN-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "VN"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

# ==================================================
# TRANG BIA
# ==================================================

story.append(Spacer(1, 3*cm))

story.append(Paragraph("BÁO CÁO THỰC HÀNH", styles["Cover"]))
story.append(Paragraph("LOS201 - EMBEDDED LINUX", styles["Cover"]))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("LAB 02", styles["Cover"]))

p("<b>Chủ đề:</b> Character Device Driver, PROCFS, SYSFS và JFFS2")

make_table([
    ["Thông tin", "Nội dung"],
    ["Họ và tên", "Doan Truong Son"],
    ["Mã sinh viên", "SE200908"],
    ["Kernel", "Linux 5.15.0"],
    ["Kiến trúc", "ARMv7 - ARM EABI5"],
    ["Compiler", "arm-linux-gnueabihf-gcc 15.2.0"],
    ["Driver", "lab2_driver.ko"],
], [5*cm, 10*cm])

p("Năm học: ................................................")

story.append(PageBreak())

# ==================================================
# 1. MUC TIEU
# ==================================================

h1("1. MỤC TIÊU BÀI THỰC HÀNH")

p("Bài thực hành LAB02 giúp sinh viên tìm hiểu quy trình xây dựng "
  "Character Device Driver trong Linux Kernel.")

p("Các mục tiêu chính:")
p("- Xây dựng và biên dịch Linux Kernel Module.<br/>"
  "- Đăng ký Character Device Driver.<br/>"
  "- Trao đổi dữ liệu giữa Kernel Space và User Space.<br/>"
  "- Sử dụng PROCFS và SYSFS.<br/>"
  "- Tìm hiểu MTD và hệ thống tập tin JFFS2.<br/>"
  "- Tích hợp driver vào Root Filesystem.")

# ==================================================
# 2. MOI TRUONG
# ==================================================

h1("2. MÔI TRƯỜNG THỰC HIỆN")

make_table([
    ["Thành phần", "Thông tin"],
    ["Kernel", "Linux 5.15.0"],
    ["Architecture", "ARMv7"],
    ["ABI", "EABI5"],
    ["Compiler", "arm-linux-gnueabihf-gcc 15.2.0"],
    ["Module", "lab2_driver.ko"],
    ["Root filesystem", "initramfs"],
    ["Filesystem", "JFFS2"],
    ["vermagic", "5.15.0 SMP mod_unload ARMv7 p2v8"],
], [5*cm, 10*cm])

# ==================================================
# 3. KIEN TRUC DRIVER
# ==================================================

h1("3. KIẾN TRÚC CHARACTER DEVICE DRIVER")

code("""
       USER APPLICATION
        read() / write()
              |
              v
       VIRTUAL FILE SYSTEM
              |
              v
       CHARACTER DEVICE
             DRIVER
              |
              v
         KERNEL BUFFER
              |
        +-----+------+
        |            |
      PROCFS       SYSFS
""")

p("Ứng dụng User Space giao tiếp với driver thông qua device node. "
  "VFS chuyển yêu cầu đến các hàm callback được đăng ký trong "
  "cấu trúc file_operations.")

p("Các hàm thường gặp gồm open(), read(), write() và release(). "
  "Driver xử lý yêu cầu, kiểm tra dữ liệu và thực hiện trao đổi "
  "với vùng nhớ trong Kernel Space.")

h2("3.1. Trao đổi dữ liệu")

p("copy_from_user() sao chép dữ liệu từ User Space vào Kernel Space. "
  "copy_to_user() sao chép dữ liệu từ Kernel Space về User Space.")

p("Không sử dụng memcpy() trực tiếp với con trỏ User Space vì kernel "
  "không thể mặc định truy cập an toàn vùng nhớ của tiến trình. "
  "Các hàm copy_from_user() và copy_to_user() hỗ trợ kiểm tra lỗi "
  "trong quá trình sao chép.")

h2("3.2. Đồng bộ dữ liệu")

p("DEFINE_MUTEX(lab2_mutex) khai báo mutex để bảo vệ vùng dữ liệu "
  "dùng chung. Mutex giúp tránh Race Condition khi nhiều tiến trình "
  "truy cập driver đồng thời.")

# ==================================================
# 4. PROCFS VA SYSFS
# ==================================================

h1("4. PROCFS VÀ SYSFS")

p("<b>PROCFS:</b> Hệ thống tập tin ảo dùng để cung cấp thông tin "
  "trạng thái hệ thống và kernel.")

p("<b>SYSFS:</b> Giao diện thể hiện các đối tượng thiết bị, driver "
  "và thuộc tính của chúng.")

h2("4.1. Kiểm tra PROCFS")

code("""
cat /proc/lab2_info
""")

p("[BỔ SUNG LOG PROCFS THỰC TẾ VÀO ĐÂY]")

h2("4.2. Kiểm tra SYSFS")

code("""
find /sys -iname '*lab2*' 2>/dev/null
""")

p("[BỔ SUNG ĐƯỜNG DẪN VÀ LOG SYSFS THỰC TẾ VÀO ĐÂY]")

# ==================================================
# 5. KIEM TRA DRIVER
# ==================================================

h1("5. KIỂM TRA CHARACTER DEVICE DRIVER")

code("""
modinfo lab2_driver.ko
insmod lab2_driver.ko
lsmod | grep lab2
ls -l /dev/lab2
dmesg | grep -i lab2
/usr/bin/test_driver.sh
""")

p("Các lệnh trên dùng để kiểm tra thông tin module, nạp driver, "
  "xác nhận module đã được nạp và kiểm tra thông báo kernel.")

p("[BỔ SUNG LOG CHẠY DRIVER THỰC TẾ VÀO ĐÂY]")

# ==================================================
# 6. MTD VA JFFS2
# ==================================================

h1("6. HỆ THỐNG TẬP TIN MTD VÀ JFFS2")

p("MTD là lớp con của Linux Kernel cung cấp giao diện quản lý "
  "các thiết bị nhớ flash.")

p("JFFS2 là hệ thống tập tin được thiết kế cho thiết bị flash "
  "dạng raw NAND/NOR.")

h2("6.1. Kiểm tra MTD")

code("""
cat /proc/mtd
mtdinfo <THIET_BI_MTD>
""")

p("[BỔ SUNG LOG MTD THỰC TẾ VÀO ĐÂY]")

h2("6.2. Thao tác JFFS2")

p("Các thao tác dưới đây được thực hiện trên HOST Ubuntu. "
  "Phải xác định đúng thiết bị MTD trước khi xóa hoặc ghi dữ liệu.")

code("""
# Xac dinh thiet bi MTD
cat /proc/mtd

# Thay <THIET_BI_MTD> bang thiet bi dung
flash_erase <THIET_BI_MTD> 0 0
nandwrite <THIET_BI_MTD> jffs2.img

mkdir -p /mnt/jffs2
mount -t jffs2 <THIET_BI_MTD> /mnt/jffs2

ls -lah /mnt/jffs2
cat /mnt/jffs2/hello.txt

umount /mnt/jffs2
""")

p("[BỔ SUNG LOG FLASH_ERASE, NANDWRITE, MOUNT, ĐỌC FILE, "
  "REMOUNT VÀ NANDDUMP THỰC TẾ VÀO ĐÂY]")

# ==================================================
# 7. SO SANH FILESYSTEM
# ==================================================

h1("7. SO SÁNH CÁC HỆ THỐNG TẬP TIN")

make_table([
    ["Filesystem", "Đặc điểm", "Ưu điểm", "Hạn chế"],
    ["ext4", "Block device", "Ổn định, phổ biến", "Không chuyên cho raw NAND"],
    ["JFFS2", "Raw flash", "Phù hợp flash dung lượng nhỏ", "Mount có thể chậm khi nhiều node"],
    ["UBIFS", "Raw NAND qua UBI", "Quản lý NAND tốt", "Cấu hình phức tạp hơn"],
    ["SquashFS", "Read-only", "Nén tốt, tiết kiệm dung lượng", "Không ghi trực tiếp"],
    ["cramfs", "Read-only", "Đơn giản, nhỏ gọn", "Ít linh hoạt"],
], [2.3*cm, 3.1*cm, 4.6*cm, 5*cm])

h2("7.1. Đề xuất cho thiết bị IoT có NAND 32 MB")

p("Đối với thiết bị IoT có NAND 32 MB, có thể sử dụng SquashFS "
  "cho Root Filesystem chỉ đọc nhằm tiết kiệm dung lượng.")

p("Một phân vùng JFFS2 hoặc UBI/UBIFS có thể được sử dụng cho "
  "dữ liệu cần ghi thay đổi thường xuyên. Lựa chọn cuối cùng "
  "phụ thuộc vào dung lượng thực tế, erase block, RAM, kernel "
  "và bootloader.")

# ==================================================
# 8. CAU HOI PHAN TICH
# ==================================================

h1("8. CÂU HỎI PHÂN TÍCH")

h2("Câu 1. Vì sao không dùng memcpy() giữa kernel và user buffer?")

p("Vùng nhớ User Space không được kernel truy cập trực tiếp tùy ý. "
  "copy_from_user() và copy_to_user() cung cấp cơ chế truy cập "
  "an toàn hơn và xử lý lỗi khi sao chép dữ liệu.")

h2("Câu 2. Vì sao sử dụng DEFINE_MUTEX(lab2_mutex)?")

p("Mutex bảo vệ tài nguyên dùng chung khi nhiều tiến trình truy cập "
  "driver đồng thời. Điều này giúp tránh Race Condition và đảm bảo "
  "tính nhất quán của dữ liệu.")

h2("Câu 3. So sánh PROCFS và SYSFS.")

p("PROCFS thường cung cấp thông tin trạng thái hệ thống và kernel. "
  "SYSFS thể hiện các đối tượng thiết bị, driver và thuộc tính "
  "của chúng. SYSFS có cấu trúc rõ ràng cho mô hình thiết bị.")

h2("Câu 4. Vì sao JFFS2 cần erase trước khi ghi?")

p("NAND Flash không cho phép ghi đè tùy ý lên dữ liệu cũ. Muốn "
  "tái sử dụng erase block cần xóa block theo quy tắc phần cứng. "
  "Trong khi đó ext4 hoạt động trên block device và ghi theo "
  "giao diện block/sector.")

h2("Câu 5. Nếu insmod trong rcS thất bại, boot có tiếp tục không?")

p("Điều này phụ thuộc cách viết rcS và shell. Nếu script không "
  "dừng ngay khi lệnh lỗi và không gọi exit, các lệnh tiếp theo "
  "có thể vẫn chạy. Tuy nhiên driver sẽ không hoạt động. "
  "Cần kiểm tra mã trả về và xử lý lỗi phù hợp.")

# ==================================================
# 9. KHO KHAN
# ==================================================

h1("9. KHÓ KHĂN VÀ CÁCH KHẮC PHỤC")

p("Điền ít nhất hai khó khăn thực tế đã gặp trong quá trình "
  "thực hiện bài lab. Không sử dụng nội dung minh họa thay "
  "cho trải nghiệm thực tế.")

make_table([
    ["Khó khăn", "Nguyên nhân", "Cách khắc phục"],
    ["[Khó khăn thực tế 1]", "[Mô tả lỗi]", "[Cách xử lý và kết quả]"],
    ["[Khó khăn thực tế 2]", "[Mô tả lỗi]", "[Cách xử lý và kết quả]"],
], [4.5*cm, 5*cm, 5.5*cm])

# ==================================================
# 10. CAU TRUC THU MUC
# ==================================================

h1("10. CẤU TRÚC THƯ MỤC")

code("""
LAB02/
|-- README.md
|-- driver/
|   |-- lab2_driver.c
|   |-- Makefile
|   |-- lab2_driver.ko
|   |-- sms_assignment/
|   `-- task2_misc/
|-- configs/
|-- logs/
|-- mtd/
|   |-- jffs2.img
|   |-- nand_dump.bin
|   `-- jffs2_data/
|-- output/
|   `-- initramfs_lab2.cpio.gz
|-- rootfs/
|   `-- initramfs/
|       |-- etc/init.d/rcS
|       |-- lib/modules/5.15.0/
|       `-- usr/bin/
`-- bao_cao/
    `-- SE200908_Lab02_BaoCao.pdf
""")

# ==================================================
# 11. KET LUAN
# ==================================================

h1("11. KẾT LUẬN")

p("Thông qua bài thực hành LAB02, sinh viên tìm hiểu được "
  "quy trình xây dựng Linux Character Device Driver, trao đổi "
  "dữ liệu giữa Kernel Space và User Space, sử dụng PROCFS, "
  "SYSFS và hệ thống tập tin JFFS2.")

p("Kết quả thực nghiệm và log chạy thực tế cần được bổ sung "
  "đầy đủ để chứng minh các chức năng đã được kiểm tra.")

# ==================================================
# TAO PDF
# ==================================================

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("VN", 8)
    canvas.drawString(
        2*cm, 1*cm,
        "LOS201 - LAB02 | Doan Truong Son | SE200908"
    )
    canvas.drawRightString(
        19*cm, 1*cm,
        f"Trang {doc.page}"
    )
    canvas.restoreState()

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=1.8*cm,
    leftMargin=1.8*cm,
    topMargin=1.8*cm,
    bottomMargin=1.8*cm,
    title="Bao cao LAB02 - Doan Truong Son",
    author="Doan Truong Son"
)

doc.build(
    story,
    onFirstPage=footer,
    onLaterPages=footer
)

print("\n======================================")
print("TAO BAO CAO LAB02 THANH CONG!")
print("File:", OUTPUT)
print("======================================\n")
