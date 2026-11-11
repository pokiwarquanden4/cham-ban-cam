/* ===========================================================
   CHẠM BẢN CẨM — JavaScript dùng chung cho MỌI trang
   1. Chuyển ngôn ngữ VI / EN (nhớ lựa chọn của người xem)
   2. Menu trên điện thoại
   3. Thanh menu thu gọn khi cuộn
   4. Ảnh hiện dần khi tải xong
   5. Bộ ảnh của trang sản phẩm
   Không có tệp này trang vẫn đọc được: tiếng Việt, ảnh hiện thẳng.
   =========================================================== */
(function(){
'use strict';
var R = document.documentElement;
var KHOA = 'cbc-ngon-ngu';
var tieuDeVi = document.title;
var meTieuDeEn = document.querySelector('meta[name="cbc-tieu-de-en"]');

/* ---------- 1. NGÔN NGỮ ---------- */
function ngonNgu(){ return R.dataset.nn === 'en' ? 'en' : 'vi'; }

function doiThuocTinh(nn){
  /* chữ nằm trong thuộc tính (alt, aria-label) không ẩn hiện bằng CSS được */
  document.querySelectorAll('[data-alt-en]').forEach(function(el){
    if (el.dataset.altVi == null) el.dataset.altVi = el.getAttribute('alt') || '';
    el.setAttribute('alt', nn === 'en' ? el.dataset.altEn : el.dataset.altVi);
  });
  document.querySelectorAll('[data-aria-en]').forEach(function(el){
    if (el.dataset.ariaVi == null) el.dataset.ariaVi = el.getAttribute('aria-label') || '';
    el.setAttribute('aria-label', nn === 'en' ? el.dataset.ariaEn : el.dataset.ariaVi);
  });
}

function datNgonNgu(nn, luu){
  nn = (nn === 'en') ? 'en' : 'vi';
  if (nn === 'en') R.dataset.nn = 'en'; else R.removeAttribute('data-nn');
  R.lang = nn;
  document.querySelectorAll('[data-dat-nn]').forEach(function(b){
    b.setAttribute('aria-pressed', String(b.dataset.datNn === nn));
  });
  doiThuocTinh(nn);
  document.title = (nn === 'en' && meTieuDeEn) ? meTieuDeEn.content : tieuDeVi;
  if (luu){ try { localStorage.setItem(KHOA, nn); } catch(e){} }
  document.dispatchEvent(new CustomEvent('doi-ngon-ngu', {detail:{nn:nn}}));
}

document.querySelectorAll('[data-dat-nn]').forEach(function(b){
  b.addEventListener('click', function(){ datNgonNgu(b.dataset.datNn, true); });
});
datNgonNgu(ngonNgu(), false);   /* đồng bộ với lựa chọn đã đặt sẵn trong <head> */

/* ---------- 2. MENU TRÊN ĐIỆN THOẠI ---------- */
var nutMenu = document.getElementById('nut-menu');
var menuDong = document.getElementById('menu-dong');
function dongMenu(){
  if (!nutMenu || !menuDong) return;
  nutMenu.setAttribute('aria-expanded', 'false');
  menuDong.hidden = true;
}
if (nutMenu && menuDong){
  nutMenu.addEventListener('click', function(){
    var mo = nutMenu.getAttribute('aria-expanded') !== 'true';
    nutMenu.setAttribute('aria-expanded', String(mo));
    menuDong.hidden = !mo;
  });
  menuDong.addEventListener('click', function(e){ if (e.target.closest('a')) dongMenu(); });
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && !menuDong.hidden){ dongMenu(); nutMenu.focus(); }
  });
}

/* ---------- 3. THANH MENU THU GỌN KHI CUỘN ---------- */
var dau = document.getElementById('dau-trang');
if (dau){
  var choVe = false;
  /* Thu gọn làm cả trang dịch lên ~47px; trình duyệt có thể bù bằng cách kéo vị trí cuộn lùi lại.
     Dùng hai ngưỡng cách xa nhau (120 / 40) để cú dịch đó không đảo được trạng thái,
     nếu không menu sẽ thu–nở liên tục quanh ngưỡng. */
  var xet = function(){
    choVe = false;
    var y = window.scrollY;
    if (y > 120) dau.classList.add('gon');
    else if (y < 40) dau.classList.remove('gon');
  };
  addEventListener('scroll', function(){ if (!choVe){ choVe = true; requestAnimationFrame(xet); } }, {passive:true});
  xet();
}

/* ---------- 4. ẢNH HIỆN DẦN ---------- */
function choHien(im){
  if (im.complete && im.naturalWidth){ im.classList.add('xong'); return; }
  im.addEventListener('load', function(){ im.classList.add('xong'); }, {once:true});
  /* ảnh lỗi vẫn phải hiện ra để người xem đọc được chữ thay thế */
  im.addEventListener('error', function(){ im.classList.add('xong'); }, {once:true});
}
document.querySelectorAll('img.mo-dan').forEach(choHien);

/* ---------- 5. BỘ ẢNH TRANG SẢN PHẨM ---------- */
var anhLon = document.getElementById('anh-lon');
if (anhLon){
  document.querySelectorAll('.sp-anh-nho button').forEach(function(nut){
    nut.addEventListener('click', function(){
      if (nut.getAttribute('aria-pressed') === 'true') return;
      document.querySelectorAll('.sp-anh-nho button').forEach(function(n){
        n.setAttribute('aria-pressed', String(n === nut));
      });
      anhLon.classList.remove('xong');
      anhLon.dataset.altVi = nut.dataset.altVi;
      anhLon.dataset.altEn = nut.dataset.altEn;
      anhLon.setAttribute('alt', ngonNgu() === 'en' ? nut.dataset.altEn : nut.dataset.altVi);
      if (nut.dataset.rong){
        var r = +nut.dataset.rong, c = +nut.dataset.cao, khung = anhLon.parentElement;
        anhLon.width = r; anhLon.height = c;
        /* ảnh gốc nhỏ (dưới 600px) chỉ được phóng tối đa gấp đôi — cùng quy tắc với công cụ tạo trang */
        var nho = Math.max(r, c) < 600;
        khung.classList.toggle('nho', nho);
        if (nho){ khung.style.setProperty('--w', r); khung.style.setProperty('--h', c); }
      }
      anhLon.src = nut.dataset.lon;
      choHien(anhLon);
    });
  });
}

window.CBC = { ngonNgu: ngonNgu, datNgonNgu: datNgonNgu, dongMenu: dongMenu };
})();
