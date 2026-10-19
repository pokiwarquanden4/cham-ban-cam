# CHẠM BẢN CẨM — trang giới thiệu

Trang tĩnh một file. Không cần máy chủ, không cần cài gì, không có bước dựng.

---

## 1. Xem thử trên máy

Mở `index.html` bằng trình duyệt là xem được ngay. Nếu video không chạy (một số trình duyệt chặn
file mở trực tiếp từ ổ đĩa), chạy lệnh này trong thư mục `site` rồi vào `http://127.0.0.1:8000`:

```
python -m http.server 8000
```

---

## 2. Đưa lên GitHub Pages

1. Tạo một repo mới trên GitHub, để **Public** (repo private cần tài khoản trả phí mới bật được Pages).
2. Đẩy **toàn bộ thư mục `site`** lên nhánh `main`. Nhớ giữ cả file `.nojekyll` — thiếu nó GitHub
   có thể bỏ qua một số file.
3. Vào **Settings → Pages**, phần *Build and deployment*: chọn **Deploy from a branch**,
   nhánh `main`, thư mục `/ (root)`. Bấm Save.
4. Đợi 1–2 phút. Trang sẽ ở `https://<tên-tài-khoản>.github.io/<tên-repo>/`.

Bằng dòng lệnh:

```
cd site
git init
git add -A
git commit -m "Trang gioi thieu CHAM BAN CAM"
git branch -M main
git remote add origin https://github.com/<tên-tài-khoản>/<tên-repo>.git
git push -u origin main
```

---

## 3. Gắn tên miền riêng

1. Mua tên miền ở bất kỳ nhà cung cấp nào.
2. Ở phần quản lý DNS của tên miền, trỏ về GitHub:
   - 4 bản ghi **A** cho tên miền gốc: `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153`
   - 1 bản ghi **CNAME** cho `www` trỏ tới `<tên-tài-khoản>.github.io`
3. Về **Settings → Pages → Custom domain**, điền tên miền, bấm Save.
   GitHub sẽ tự tạo file `CNAME` trong repo.
4. Đợi chứng chỉ bảo mật cấp xong rồi bật **Enforce HTTPS**.

---

## 4. Những ô cần tự điền

Trong `index.html` có bốn chỗ để trống, đang hiện bằng khung viền đứt. Tìm chữ
`Chủ dự án điền` là thấy hết:

- giá bộ và các phiên bản hộp
- tên nghệ nhân / hộ sản xuất / hợp tác xã đối tác
- email · điện thoại · fanpage
- thông tin liên hệ ở chân trang

Chưa điền thì trang vẫn chạy bình thường, chỉ là còn khung trống.

**Lưu ý:** trang không có biểu mẫu đăng ký. GitHub Pages chỉ phục vụ file tĩnh, không có
máy chủ phía sau để hứng dữ liệu người điền. Nếu cần nhận đăng ký, dùng dịch vụ ngoài
như Google Form hoặc Formspree rồi đặt đường dẫn vào ô liên hệ.

---

## 5. Hai điều về bản quyền tư liệu — đọc trước khi chạy quảng cáo

**Phim `story.mp4` ("Lùng Tám", 2 phút 22)** là phim nhóm tự quay. Không dính tư liệu của ai.
Dùng thoải mái.

**Phim `van-hoa.mp4` ("Văn hoá Hà Giang", 53 giây)** do nhóm dựng nhưng **ghép từ tư liệu
của bên thứ ba**:
- giây 15–25 có logo **AMAZING HÀ GIANG — KỲ VĨ HÀ GIANG** đóng chìm trong hình
- giây 26 có dòng ghi công **The Lover Lo Lo Chai — Jerry Tran**

Trang đang giữ nguyên cả hai, không cắt không che, và có hẳn một khối ghi nguồn đặt tên là
*"Chúng tôi ghi nguồn vì đó là nghề."* Đừng gỡ khối đó, cũng đừng xoá logo khỏi phim —
xoá logo là gỡ mất phần ghi công, còn rủi ro hơn giữ lại.

Nếu sau này trang dùng cho mục đích thương mại thật sự, nên xin phép chủ tư liệu bằng văn bản,
hoặc thay bằng phim tự quay.

Ảnh trong năm chương lấy từ tài liệu dự án của nhóm. Nếu biết tác giả gốc của từng ảnh thì
nên bổ sung tên vào phần chú thích dưới mỗi ảnh.

---

## 6. Dung lượng và băng thông

Tổng thư mục khoảng **48 MB**, trong đó video chiếm 40 MB. GitHub cho mỗi repo tối đa 1 GB
và khoảng 100 GB băng thông mỗi tháng, nên bình thường thì thoải mái.

Chỗ cần để ý: `story.mp4` nặng 25,8 MB. Trang đã đặt phim ở chế độ **chỉ tải khi người xem
bấm nút** (`preload="none"`, không tự phát), nên người chỉ lướt qua không tốn gì.

Nhưng nếu trang được chia sẻ rộng — chẳng hạn một buổi thuyết trình đông người, hay một bài
đăng lan truyền — thì khoảng vài nghìn lượt bấm xem là chạm trần băng thông, GitHub sẽ gửi
cảnh báo và có thể tạm ngắt trang.

**Cách xử lý khi đó:** đưa `story.mp4` và `van-hoa.mp4` lên YouTube ở chế độ *không công khai*
rồi thay khối phim bằng đường dẫn YouTube. Chỉ sửa khoảng mười dòng, không phải dựng lại trang.

---

## 7. Cấu trúc thư mục

```
site/
  index.html              toàn bộ trang: HTML + CSS + JavaScript trong một file
  .nojekyll               báo GitHub đừng xử lý lại file
  .gitignore
  assets/
    img/    23 ảnh, mỗi ảnh có 3 bản: .webp, .jpg dự phòng, -tiny.webp làm nền chờ
    video/  5 video H.264
```

Video dùng mã H.264 chứ không phải H.265 như file gốc. Chrome và Firefox không phát được
H.265 — nếu sau này thay video mới, nhớ chuyển mã trước.

---

## 8. Vài điều về cách trang hoạt động

- **Năm sợi ở mép phải màn hình** (dưới đáy trên điện thoại) là năm cộng đồng. Bấm vào một sợi
  thì con thoi chạy ngang và cả trang đổi màu theo bộ trang phục của cộng đồng đó. Khi cuộn
  qua từng chương thì màu cũng đổi, nhưng đổi lặng lẽ không chạy con thoi — để cảm giác
  "mình vừa bấm ra điều đó" không bị trang tự làm hộ.
- **Máy yếu, mạng chậm, hoặc người dùng bật chế độ giảm chuyển động** thì trang tự hạ bậc:
  bỏ con thoi, bỏ video nền, chỉ còn ảnh tĩnh. Nội dung vẫn đủ.
- **Trang dùng nền sáng.** Nền là sắc vải lanh mộc `#F6F2E9`. Màu chàm không mất đi — nó chuyển
  từ vai nền sang vai mực và vai điểm nhấn, đúng như trên tấm vải thật.
  Chỉ ba khối dùng nền tối: phần mở đầu, khung phim và khối ghi nguồn. Xem phim thì tắt đèn,
  đó là lý do của ba khối đó, không phải sở thích. Khối nào cần nền tối thì thêm `class="tam-toi"`,
  mọi token bên trong sẽ tự đổi vai.
- **Hoa văn vẽ bằng mũi thêu chữ X**, không phải ô vuông đặc — thổ cẩm được làm từ mũi thêu,
  vẽ bằng ô vuông sẽ ra hình pixel. Mỗi mũi lệch nhẹ theo vị trí, nhưng lệch có quy luật nên
  vẽ lại bao nhiêu lần cũng ra đúng một hình.
- **Màu chữ và màu mảng là hai biến tách riêng.** Ba trong năm màu cộng đồng không đủ tương
  phản để làm chữ nhỏ trên nền chàm, nên mỗi cộng đồng có một màu riêng dành cho chữ. Nếu sửa
  màu, giữ nguyên quy tắc này, không thì có chương sẽ không đọc được.
- **Mọi đường dẫn đều là đường dẫn tương đối**, không có dấu gạch chéo ở đầu — nhờ vậy trang
  chạy được cả khi nằm trong thư mục con của GitHub Pages.

---

## 9. Trang chia làm ba phần

Trang giữ đúng cách chia ba thẻ trong tài liệu của nhóm:

1. **Văn hoá Hà Giang** — năm cộng đồng, mốc UNESCO 2019, chợ phiên
2. **Nguồn gốc và quy trình** — Lùng Tám, hợp tác xã 2001, chín bước làm vải, phim của nhóm
3. **Ý nghĩa hoa văn thổ cẩm** — bốn họ họa tiết, sắc màu, vì sao cần gìn giữ

Mỗi lần chỉ hiện một phần. Bấm thẻ nào thì con thoi chạy ngang rồi phần đó lộ ra.
Gắn thẳng đường dẫn tới từng phần được: thêm `#phan-1`, `#phan-2` hoặc `#phan-3` vào cuối địa chỉ.

Nội dung ba phần lấy từ tài liệu Google Docs của nhóm. Nếu tài liệu đó sửa thì phải sửa lại trang,
hai bên không tự đồng bộ.
