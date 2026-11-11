"""Chuyển một ảnh gốc thành đủ các bản trang cần, đặt vào assets/img/.

Chạy ở thư mục gốc của trang (cần Pillow: pip install pillow):
    python cong-cu/tao-anh.py <đường-dẫn-ảnh-gốc> <tên-không-dấu>

Ví dụ:
    python cong-cu/tao-anh.py "D:/anh/Chạm Hoa.png" box-cham-hoa

Ra bốn tệp:
    <tên>.webp       ảnh lớn, cạnh dài tối đa 1600px (không bao giờ phóng to ảnh nhỏ)
    <tên>-the.webp   640px, cho thẻ sản phẩm và dãy ảnh nhỏ
    <tên>.jpg        ảnh xem trước khi chia sẻ link (Facebook, Zalo)
    <tên>-tiny.webp  24px, nền mờ lúc chờ tải
Ghi đè nếu tên đã có.
"""
import os
import re
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit('Cần Pillow: chạy  pip install pillow  rồi thử lại.')

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RA = os.path.join(GOC, 'assets', 'img')
NEN = (246, 242, 233)   # nền vải lanh của trang, lót dưới ảnh có phần trong suốt


def main():
    for luong in (sys.stdout, sys.stderr):
        try:
            luong.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    nguon, ten = sys.argv[1], sys.argv[2]
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', ten):
        sys.exit('Tên chỉ gồm chữ thường không dấu, số và dấu gạch ngang, ví dụ: tui-tote-do')
    im = ImageOps.exif_transpose(Image.open(nguon))      # ảnh chụp điện thoại có thể bị xoay
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        lot = Image.new('RGB', im.size, NEN)
        lot.paste(im, mask=im.split()[-1])
        im = lot
    im = im.convert('RGB')

    lon = im.copy()
    lon.thumbnail((1600, 1600), Image.LANCZOS)
    lon.save(os.path.join(RA, ten + '.webp'), 'WEBP', quality=82, method=6)
    lon.save(os.path.join(RA, ten + '.jpg'), 'JPEG', quality=84, optimize=True, progressive=True)
    the = im.copy()
    the.thumbnail((640, 640), Image.LANCZOS)
    the.save(os.path.join(RA, ten + '-the.webp'), 'WEBP', quality=78, method=6)
    nho = im.copy()
    nho.thumbnail((24, 24))
    nho.save(os.path.join(RA, ten + '-tiny.webp'), 'WEBP', quality=40)
    print('xong: assets/img/%s.webp (%dx%d) và các bản -the, .jpg, -tiny' % ((ten,) + lon.size))
    if max(im.size) < 600:
        print('lưu ý: ảnh gốc chỉ %dx%d — lên trang sẽ hơi nhoè, có ảnh gốc lớn hơn thì tốt hơn' % im.size)


if __name__ == '__main__':
    main()
