"""Tạo lại các trang sản phẩm và những đoạn dùng chung trong index.html.

Chạy ở thư mục gốc của trang:
    python cong-cu/tao-trang.py

Công cụ đọc:
    cong-cu/san-pham.json    danh sách box và sản phẩm bán lẻ (chữ VI + EN, ảnh)
    cong-cu/dau-trang.html   thanh trên cùng + menu, dùng cho mọi trang
    cong-cu/chan-trang.html  chân trang, dùng cho mọi trang
và ghi ra:
    san-pham/<mã>.html       mỗi sản phẩm một trang (xoá trang của sản phẩm đã bỏ khỏi danh sách)
    index.html               chỉ thay phần nằm giữa các cặp dấu <!-- @tên --> ... <!-- /@tên -->

Không cần cài gì thêm ngoài Python 3. Có Pillow thì công cụ tự đọc kích thước ảnh
để ghi width/height (trang đỡ giật khi tải); không có cũng không sao.
"""
import html
import json
import os
import re
import sys

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONG_CU = os.path.join(GOC, 'cong-cu')
THU_MUC_SP = os.path.join(GOC, 'san-pham')
THU_MUC_ANH = os.path.join(GOC, 'assets', 'img')

try:
    from PIL import Image
except ImportError:          # không có Pillow: bỏ width/height
    Image = None

e = html.escape


def doc(ten):
    with open(os.path.join(CONG_CU, ten), encoding='utf-8') as f:
        return f.read()


def kich_thuoc(tep):
    """(rộng, cao) của assets/img/<tep>.webp, hoặc None."""
    if Image is None:
        return None
    p = os.path.join(THU_MUC_ANH, tep + '.webp')
    if not os.path.exists(p):
        sys.exit('THIẾU ẢNH: assets/img/%s.webp' % tep)
    with Image.open(p) as im:
        return im.size


def wh(tep):
    k = kich_thuoc(tep)
    return ' width="%d" height="%d"' % k if k else ''


def hai_ngu(vi, en):
    """Một cặp chữ VI/EN; chỉ một bản hiện, theo nút chuyển ngôn ngữ."""
    if not en or en == vi:
        return e(vi)
    return '<span lang="vi">%s</span><span lang="en">%s</span>' % (e(vi), e(en))


def dien(mau, goc, trang_chu):
    return mau.replace('{{goc}}', goc).replace('{{trang-chu}}', trang_chu)


def ten_sp(sp, en=False):
    if en:
        return sp['loai_en'] + (' – ' + sp['bien_the_en'] if sp['bien_the_en'] else '')
    return sp['loai'] + (' – ' + sp['bien_the'] if sp['bien_the'] else '')


MUI_TEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
           'stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M9 7h8v8"/></svg>')
ICON_FB = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.6 21v-7.9h2.7l.4-3.2h-3.1v-2'
           'c0-.9.3-1.5 1.6-1.5h1.6V3.5a22 22 0 0 0-2.4-.1c-2.4 0-4 1.5-4 4.1v2.4H7.7v3.2h2.7V21z"/></svg>')


# ---------------------------------------------------------------- lưới thẻ ở trang chủ
def the_box(b):
    anh = b['anh'][0]['tep']
    return (
        '<a class="the-sp" href="san-pham/%(ma)s.html">'
        '<span class="the-anh" style="background-image:url(assets/img/%(anh)s-tiny.webp)">'
        '<img class="mo-dan" src="assets/img/%(anh)s-the.webp" alt=""%(wh)s loading="lazy" decoding="async">'
        '<span class="mui-ten" aria-hidden="true">%(mt)s</span></span>'
        '<span class="the-nhan">%(nhan)s</span>'
        '<span class="the-ten">%(ten)s</span>'
        '<span class="the-mo-ta">%(kh)s</span>'
        '<span class="the-chan"><span class="the-kham-pha">%(kp)s</span></span>'
        '</a>' % {
            'ma': b['ma'], 'anh': anh, 'wh': wh(anh + '-the'), 'mt': MUI_TEN,
            'nhan': hai_ngu('Chạm Bản Cẩm · Box', 'Chạm Bản Cẩm · Gift box'),
            'ten': e(b['ten']), 'kh': hai_ngu(b['khau_hieu'], b['khau_hieu_en']),
            'kp': hai_ngu('Khám phá box', 'Explore box'),
        })


def cac_anh_le(sp):
    """Ảnh của một sản phẩm lẻ dưới dạng danh sách {tep, vi, en}.
    Trong JSON, "anh" có thể là một tên ảnh, một danh sách, hoặc null (chưa có ảnh)."""
    a = sp.get('anh')
    if not a:
        return []
    if isinstance(a, list):
        return a
    return [{'tep': a, 'vi': ten_sp(sp), 'en': ten_sp(sp, True)}]


CHO_ANH = hai_ngu('[ Chờ ảnh ]', '[ Photo coming soon ]')


def the_ban_le(sp):
    ds = cac_anh_le(sp)
    if ds:
        anh = ('<span class="the-anh"><img class="mo-dan" src="assets/img/%s-the.webp" alt=""%s '
               'loading="lazy" decoding="async">' % (ds[0]['tep'], wh(ds[0]['tep'] + '-the')))
    else:
        anh = '<span class="the-anh cho-anh"><span class="chu-cho">%s</span>' % CHO_ANH
    return (
        '<a class="the-sp vua" href="san-pham/%(ma)s.html">%(anh)s'
        '<span class="mui-ten" aria-hidden="true">%(mt)s</span></span>'
        '<span class="the-nhan">%(nhan)s</span>'
        '<span class="the-ten">%(ten)s</span>'
        '<span class="the-chan"><span class="the-kham-pha">%(kp)s</span></span>'
        '</a>' % {
            'ma': sp['ma'], 'anh': anh, 'mt': MUI_TEN,
            'nhan': hai_ngu('Chạm Bản Cẩm · Bán lẻ', 'Chạm Bản Cẩm · Retail'),
            'ten': hai_ngu(ten_sp(sp), ten_sp(sp, True)),
            'kp': hai_ngu('Xem sản phẩm', 'View product'),
        })


def nhom(tieu_de_vi, tieu_de_en, dem_vi, dem_en, cac_the):
    """Lưới thẻ, có thể kèm dòng đầu nhóm (tiêu đề + số đếm).
    Bỏ tiêu đề thì chỉ hiện số đếm; bỏ cả số đếm thì chỉ còn lưới."""
    if dem_vi:
        dem = '<span class="dem">%s</span>' % hai_ngu(dem_vi, dem_en)
        if tieu_de_vi:
            dau = '<div class="dau-nhom"><h3>%s</h3>%s</div>\n' % (hai_ngu(tieu_de_vi, tieu_de_en), dem)
        else:
            dau = '<div class="dau-nhom chi-dem">%s</div>\n' % dem
    else:
        dau = ''
    return '\n%s<div class="luoi-sp">\n%s\n</div>\n' % (dau, '\n'.join(cac_the))


# ---------------------------------------------------------------- trang sản phẩm
MAU_TRANG = '''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(tieu_de)s</title>
<meta name="cbc-tieu-de-en" content="%(tieu_de_en)s">
<meta name="description" content="%(mo_ta)s">
<meta name="theme-color" content="#F6F2E9">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%%3E%%3Crect width='32' height='32' fill='%%230D141B'/%%3E%%3Cg fill='%%23E6DFCE'%%3E%%3Crect x='5' y='3' width='2' height='26'/%%3E%%3Crect x='11' y='3' width='2' height='26'/%%3E%%3Crect x='17' y='3' width='2' height='26'/%%3E%%3Crect x='23' y='3' width='2' height='26'/%%3E%%3C/g%%3E%%3Crect x='2' y='14' width='28' height='4' fill='%%23D8321C'/%%3E%%3C/svg%%3E">
<meta property="og:type" content="product">
<meta property="og:url" content="%(url)s">
<meta property="og:site_name" content="Chạm Bản Cẩm">
<meta property="og:locale" content="vi_VN">
<meta property="og:title" content="%(tieu_de)s">
<meta property="og:description" content="%(mo_ta)s">
<meta property="og:image" content="%(og_anh)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="%(og_anh)s">
<!-- TRANG NÀY DO cong-cu/tao-trang.py TẠO RA. Sửa cong-cu/san-pham.json rồi chạy lại công cụ, đừng sửa tay. -->
<script>(function(d){d.className+=' js';try{if(localStorage.getItem('cbc-ngon-ngu')==='en'){d.setAttribute('data-nn','en');d.lang='en'}}catch(e){}})(document.documentElement)</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wdth,wght@75..100,300..800&family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Literata:ital,wght@0,400;1,400&display=swap">
<link rel="stylesheet" href="../assets/css/chung.css">
</head>
<body>
%(dau)s
<main class="trang-sp">
  <div class="boc">
    <a class="lien-ket-ve ve" href="../index.html#%(phan_ve)s"><span aria-hidden="true">←</span> %(ve)s</a>
    <div class="sp-luoi">
      <div class="sp-anh">
%(anh)s
      </div>
      <div class="sp-thong-tin">
%(sp_dau)s        <h1 class="sp-ten">%(ten)s</h1>
%(than)s
        <div class="sp-mua">
          <a class="nut-fb" href="%(fb)s" target="_blank" rel="noopener">%(icon_fb)s<span>%(nut)s</span></a>
        </div>
      </div>
    </div>
  </div>
</main>
%(chan)s
<script src="../assets/js/chung.js" defer></script>
</body>
</html>
'''


def khung_anh_lon(tep, alt_vi, alt_en):
    k = kich_thuoc(tep)
    lop, kieu = 'sp-anh-chinh', ''
    if k and max(k) < 600:
        # ảnh gốc trong tài liệu rất nhỏ: chỉ phóng tối đa gấp đôi, phóng hơn sẽ nhoè
        lop += ' nho'
        kieu = ' style="--w:%d;--h:%d"' % k
    return ('        <div class="%s"%s><img class="mo-dan" id="anh-lon" src="../assets/img/%s.webp" '
            'alt="%s" data-alt-en="%s"%s decoding="async"></div>' % (
                lop, kieu, tep, e(alt_vi), e(alt_en), wh(tep)))


def bo_anh(ds):
    """Ảnh lớn + dãy ảnh nhỏ (nếu có từ 2 ảnh). ds rỗng thì hiện khung chờ ảnh."""
    if not ds:
        return ('        <div class="sp-anh-chinh cho-anh"><div class="o-cho-dien">%s</div></div>' % hai_ngu(
            '[ Chủ dự án điền: ảnh sản phẩm ]', '[ Owner to fill in: product photo ]'))
    a0 = ds[0]
    anh = khung_anh_lon(a0['tep'], a0['vi'], a0['en'])
    if len(ds) < 2:
        return anh
    nho = []
    for i, a in enumerate(ds):
        k = kich_thuoc(a['tep'])
        co = ' data-rong="%d" data-cao="%d"' % k if k else ''
        nho.append(
            '          <button type="button" aria-pressed="%s" data-lon="../assets/img/%s.webp"%s '
            'data-alt-vi="%s" data-alt-en="%s" aria-label="Ảnh %d" data-aria-en="Photo %d">'
            '<img src="../assets/img/%s-the.webp" alt="" loading="lazy" decoding="async"></button>' % (
                'true' if i == 0 else 'false', a['tep'], co, e(a['vi']), e(a['en']), i + 1, i + 1, a['tep']))
    return (anh + '\n        <div class="sp-anh-nho" role="group" aria-label="Ảnh sản phẩm" data-aria-en="Product photos">\n' +
            '\n'.join(nho) + '\n        </div>')


def trang_box(b, d, dau, chan):
    a0 = b['anh'][0]
    anh = bo_anh(b['anh'])

    dong = '\n'.join(
        '            <li><span class="bt" aria-hidden="true">%s</span><p>%s</p></li>' % (e(c['bt']), hai_ngu(c['vi'], c['en']))
        for c in b['co_gi'])
    bt_co_gi = (e(b['bieu_tuong_co_gi']) + ' ') if b['bieu_tuong_co_gi'] else ''
    than = (
        '        <p class="sp-khau-hieu">%s</p>\n'
        '        <div class="sp-ke"></div>\n'
        '        <section class="sp-co-gi" aria-labelledby="h-co-gi">\n'
        '          <h2 id="h-co-gi">%s%s</h2>\n'
        '          <ul>\n%s\n          </ul>\n'
        '        </section>' % (
            hai_ngu(b['khau_hieu'], b['khau_hieu_en']),
            bt_co_gi, hai_ngu(b['ten'] + ' có gì?', "What's inside " + b['ten'] + '?'),
            dong))

    tieu_de = '%s — %s | CHẠM BẢN CẨM' % (b['ten'], b['khau_hieu'])
    tieu_de_en = '%s — %s | CHẠM BẢN CẨM' % (b['ten'], b['khau_hieu_en'])
    return MAU_TRANG % {
        'tieu_de': e(tieu_de), 'tieu_de_en': e(tieu_de_en),
        'mo_ta': e('Box quà %s của CHẠM BẢN CẨM: %s.' % (b['ten'], b['khau_hieu'].lower())),
        'url': e(d['dia_chi_web'] + 'san-pham/' + b['ma'] + '.html'),
        'og_anh': e(anh_og(d, a0['tep'])),
        'dau': dau, 'chan': chan, 've': hai_ngu('Quay lại danh sách sản phẩm', 'Back to all products'),
        'phan_ve': 'hop-qua',      # box nằm ở phần 04 Hộp quà trải nghiệm
        'anh': anh,
        # trang box không ghi số thứ tự và nhãn "Box" (theo góp ý của nhóm); giữ biểu tượng nếu tài liệu có
        'sp_dau': ('        <div class="sp-dau"><span class="sp-bieu-tuong" aria-hidden="true">%s</span></div>\n'
                   % e(b['bieu_tuong'])) if b['bieu_tuong'] else '',
        'ten': e(b['ten']), 'than': than,
        'fb': e(d['facebook']), 'icon_fb': ICON_FB,
        'nut': hai_ngu('Liên hệ qua Facebook để mua hàng', 'Contact us on Facebook to order'),
    }


def trang_ban_le(sp, d, dau, chan):
    vi, en = ten_sp(sp), ten_sp(sp, True)
    mo_ta_vi, mo_ta_en = sp.get('mo_ta', ''), sp.get('mo_ta_en', '')
    if mo_ta_vi:
        than = '        <div class="sp-ke"></div>\n        <p class="sp-mo-ta">%s</p>' % hai_ngu(mo_ta_vi, mo_ta_en)
    else:
        than = ('        <div class="sp-ke"></div>\n'
                '        <div class="o-cho-dien">%s</div>' % hai_ngu(
                    '[ Chủ dự án điền: mô tả sản phẩm ]', '[ Owner to fill in: product description ]'))
    return MAU_TRANG % {
        'tieu_de': e(vi + ' | CHẠM BẢN CẨM'), 'tieu_de_en': e(en + ' | CHẠM BẢN CẨM'),
        'mo_ta': e('%s — sản phẩm thổ cẩm của CHẠM BẢN CẨM.' % vi),
        'url': e(d['dia_chi_web'] + 'san-pham/' + sp['ma'] + '.html'),
        'og_anh': e(anh_og(d, (cac_anh_le(sp) or [{'tep': None}])[0]['tep'])),
        'dau': dau, 'chan': chan, 've': hai_ngu('Quay lại danh sách sản phẩm', 'Back to all products'),
        'phan_ve': 'san-pham',     # sản phẩm lẻ nằm ở phần 03 Sản phẩm bán lẻ
        'anh': bo_anh(cac_anh_le(sp)),
        'sp_dau': '        <div class="sp-dau"><span class="sp-nhan">%s</span></div>\n' % hai_ngu(
            'Sản phẩm bán lẻ', 'Retail product'),
        'ten': hai_ngu(vi, en), 'than': than,
        'fb': e(d['facebook']), 'icon_fb': ICON_FB,
        'nut': hai_ngu('Liên hệ qua Facebook để mua hàng', 'Contact us on Facebook to order'),
    }


def anh_og(d, tep):
    """Facebook và Zalo bỏ qua ảnh nhỏ hơn 200px — khi đó (hoặc khi chưa có ảnh)
    dùng ảnh chia sẻ chung của trang."""
    if not tep:
        return d['dia_chi_web'] + 'assets/img/share.jpg'
    k = kich_thuoc(tep)
    if k and min(k) < 200:
        return d['dia_chi_web'] + 'assets/img/share.jpg'
    return d['dia_chi_web'] + 'assets/img/' + tep + '.jpg'


# ---------------------------------------------------------------- ghi vào index.html
def thay_doan(van_ban, ten, noi_dung):
    mau = re.compile(r'(<!-- @%s -->)(.*?)(<!-- /@%s -->)' % (re.escape(ten), re.escape(ten)), re.S)
    if not mau.search(van_ban):
        sys.exit('index.html thiếu cặp dấu <!-- @%s --> ... <!-- /@%s -->' % (ten, ten))
    return mau.sub(lambda m: m.group(1) + '\n' + noi_dung.strip('\n') + '\n' + m.group(3), van_ban, count=1)


def main():
    # cửa sổ dòng lệnh Windows mặc định không in được chữ có dấu
    for luong in (sys.stdout, sys.stderr):
        try:
            luong.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass
    d = json.loads(doc('san-pham.json'))
    dau_mau, chan_mau = doc('dau-trang.html'), doc('chan-trang.html')

    # --- trang sản phẩm
    os.makedirs(THU_MUC_SP, exist_ok=True)
    dau_goc = dien(dau_mau, '../', '../index.html')
    # menu sáng đúng phần chứa sản phẩm: box ở 04 Hộp quà, sản phẩm lẻ ở 03 Sản phẩm bán lẻ
    dau_box = dau_goc.replace('data-phan="hop-qua">', 'data-phan="hop-qua" aria-current="true">')
    dau_le = dau_goc.replace('data-phan="san-pham">', 'data-phan="san-pham" aria-current="true">')
    chan_sp = dien(chan_mau, '../', '../index.html')
    con = set()
    for b in d['box']:
        con.add(b['ma'] + '.html')
        ghi(os.path.join(THU_MUC_SP, b['ma'] + '.html'), trang_box(b, d, dau_box, chan_sp))
    for sp in d['ban_le']:
        con.add(sp['ma'] + '.html')
        ghi(os.path.join(THU_MUC_SP, sp['ma'] + '.html'), trang_ban_le(sp, d, dau_le, chan_sp))
    for f in os.listdir(THU_MUC_SP):
        if f.endswith('.html') and f not in con:
            os.remove(os.path.join(THU_MUC_SP, f))
            print('đã xoá trang cũ: san-pham/' + f)

    # --- index.html
    p = os.path.join(GOC, 'index.html')
    with open(p, encoding='utf-8') as f:
        v = f.read()
    v = thay_doan(v, 'dau-trang', dien(dau_mau, '', ''))
    v = thay_doan(v, 'chan-trang', dien(chan_mau, '', ''))
    n_box, n_le = len(d['box']), len(d['ban_le'])
    # theo góp ý của nhóm: hai lưới không có dòng tiêu đề / số đếm — vào thẳng sản phẩm
    v = thay_doan(v, 'nhom-box', nhom(None, None, None, None, [the_box(b) for b in d['box']]))
    v = thay_doan(v, 'nhom-ban-le', nhom(None, None, None, None, [the_ban_le(sp) for sp in d['ban_le']]))
    ghi(p, v)
    print('xong: %d box, %d sản phẩm bán lẻ, index.html đã cập nhật' % (n_box, n_le))


def ghi(p, noi_dung):
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(noi_dung)


if __name__ == '__main__':
    main()
