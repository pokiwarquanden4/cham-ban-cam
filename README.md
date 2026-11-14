# CHẠM BẢN CẨM — trang giới thiệu

Trang tĩnh. Không cần máy chủ, không cần cài gì để xem. Có một công cụ nhỏ bằng Python
để tạo lại các trang sản phẩm (xem mục 4).

---

## 1. Xem thử trên máy

Mở `index.html` bằng trình duyệt là xem được ngay. Nếu video không chạy (một số trình duyệt chặn
file mở trực tiếp từ ổ đĩa), chạy lệnh này trong thư mục trang rồi vào `http://127.0.0.1:8000`:

```
python -m http.server 8000
```

---

## 2. Đưa lên GitHub Pages

1. Tạo một repo mới trên GitHub, để **Public** (repo private cần tài khoản trả phí mới bật được Pages).
2. Đẩy **toàn bộ thư mục trang** lên nhánh `main`. Nhớ giữ cả file `.nojekyll` — thiếu nó GitHub
   có thể bỏ qua một số file.
3. Vào **Settings → Pages**, phần *Build and deployment*: chọn **Deploy from a branch**,
   nhánh `main`, thư mục `/ (root)`. Bấm Save.
4. Đợi 1–2 phút. Trang sẽ ở `https://<tên-tài-khoản>.github.io/<tên-repo>/`.

---

## 3. Trang có những gì

Trang chủ `index.html` chia sáu phần theo tài liệu "cấu trúc website" của nhóm. Menu kiểu
Trúc Lâm: logo ở giữa, ba mục mỗi bên. **Mỗi lần chỉ hiện một phần**; bấm mục nào thì con thoi
chạy ngang rồi phần đó lộ ra. Trang không ghi số "Phần 0X" — số trong bảng dưới chỉ để tiện nói với nhau.

| Phần | Đường dẫn | Nội dung |
|---|---|---|
| 01 Giới thiệu | `#gioi-thieu` | ảnh lớn đầu trang, thông tin doanh nghiệp, về Chạm Bản Cẩm, tầm nhìn – sứ mệnh – giá trị cốt lõi, liên hệ |
| 02 Câu chuyện thổ cẩm | `#cau-chuyen` | Lùng Tám và HTX, bà Vàng Thị Mai, 9 bước làm vải, giá trị thổ cẩm Lùng Tám, ý nghĩa hoa văn |
| 03 Sản phẩm bán lẻ | `#san-pham` | 25 sản phẩm bán lẻ, không có tiêu đề — vào thẳng lưới sản phẩm |
| 04 Hộp quà trải nghiệm | `#hop-qua` | 4 box, không có tiêu đề — vào thẳng lưới box |
| 05 Trải nghiệm văn hóa | `#trai-nghiem` | văn hóa Hà Giang, năm cộng đồng, chợ phiên, video (2 phim) |
| 06 Về chúng tôi | `#ve-chung-toi` | giới thiệu dự án, thành viên, đối tác cung ứng, nguồn tư liệu |

- Gắn thẳng đường dẫn tới một mục bên trong cũng được, ví dụ `#hoa-van`, `#quy-trinh`, `#nam-soi`.
- Đường dẫn cũ `#phan-1`, `#phan-2`, `#phan-3` (đã gửi đi trước đây) vẫn mở đúng nội dung:
  `#phan-1` → phần 05, `#phan-2` → phần 02, `#phan-3` → mục hoa văn trong phần 02.
- Không có JavaScript thì cả sáu phần hiện nối tiếp nhau — không ai bị mất nội dung.

Phần 02 và 06 không có tiêu đề lớn, mở đầu bằng hàng mục lục chữ to. Phần 06 không đánh số mục.
Mọi đoạn văn **căn lề hai đầu** (CSS `text-align:justify`, danh sách lớp ở cuối mục chữ trong
`index.html` và ở `chung.css`) — thêm kiểu đoạn văn mới thì nhớ thêm vào danh sách đó.

**Chữ:** tiếng Việt lấy nguyên văn tài liệu; riêng mục *Ý nghĩa hoa văn* giữ như web cũ
theo ghi chú của nhóm. Nếu tài liệu sửa thì phải sửa lại trang, hai bên không tự đồng bộ.

---

## 4. Sửa sản phẩm

Danh sách box và sản phẩm bán lẻ nằm trong **`cong-cu/san-pham.json`**. Lưới thẻ ở phần 03 (sản phẩm bán lẻ),
phần 04 (box) và 29 trang trong thư mục `san-pham/` đều được tạo từ tệp này. Sửa xong thì chạy:

```
python cong-cu/tao-trang.py
```

Công cụ sẽ:
- tạo lại mọi trang `san-pham/<mã>.html` (và xoá trang của sản phẩm đã bỏ khỏi danh sách),
- thay lưới thẻ trong `index.html` — chỉ thay đoạn nằm giữa các dấu `<!-- @nhom-box -->`
  (trong phần 04) và `<!-- @nhom-ban-le -->` (trong phần 03),
- chép menu (`cong-cu/dau-trang.html`) và chân trang (`cong-cu/chan-trang.html`) vào
  `index.html` và mọi trang sản phẩm. **Muốn đổi số điện thoại, email, mạng xã hội thì sửa hai tệp
  này rồi chạy công cụ**, đừng sửa tay từng trang.

Đừng sửa tay các tệp trong `san-pham/` — lần chạy công cụ sau sẽ ghi đè.

Mỗi sản phẩm trong tệp JSON có chữ tiếng Việt và tiếng Anh. Ảnh ghi bằng tên tệp trong
`assets/img/`, không có đuôi. Thêm mô tả cho sản phẩm bán lẻ thì thêm hai trường
`"mo_ta"` và `"mo_ta_en"` vào sản phẩm đó — có mô tả rồi thì ô chờ tự biến mất.

Mỗi ảnh sản phẩm có 4 bản: `<tên>.webp` (ảnh lớn), `<tên>-the.webp` (640px, dùng cho thẻ và dãy
ảnh nhỏ), `<tên>.jpg` (ảnh xem trước khi chia sẻ link), `<tên>-tiny.webp` (nền mờ lúc chờ tải).
Có ảnh mới thì một lệnh tạo đủ cả bốn bản:

```
python cong-cu/tao-anh.py "D:/anh/Túi tote đỏ.jpg" tui-tote-do
```

**Ảnh gốc của nhiều sản phẩm bán lẻ trong tài liệu rất nhỏ** (lót ly, kẹp nơ, balo đỏ, balo trắng kem,
túi tote, túi đeo chéo mã 1 và 3… chỉ 160–500px), nên lên trang hơi nhoè. Có ảnh chụp gốc thì chạy
lệnh trên với đúng tên cũ để thay.

Có Pillow (`pip install pillow`) thì công cụ tự đọc kích thước ảnh để ghi vào trang; không có
cũng chạy được.

---

## 5. Những ô còn chờ điền

Tìm chữ `Chủ dự án điền` là thấy, đang hiện bằng khung viền đứt:

- **Mô tả Vòng tay và Túi đựng bút** — tài liệu chưa có; thêm `"mo_ta"`, `"mo_ta_en"` vào
  `cong-cu/san-pham.json` (mục 4).
- **Ảnh Móc khóa logo** — chưa có ảnh riêng. Tạo ảnh bằng `python cong-cu/tao-anh.py <ảnh> moc-khoa-logo`
  rồi sửa `"anh": null` thành `"anh": "moc-khoa-logo"` trong JSON và chạy lại công cụ.

Ảnh bìa phần 01 là `assets/img/anh-bia` (ảnh dọc, hiện trọn ảnh, hai bên là nền trang). Thay ảnh thì
sửa `src`, `alt`, `data-alt-en`, `width`, `height` của thẻ ảnh trong khối `gt-anh-dau` ở `index.html`.

Trang không hiện giá — liên hệ mua qua nút "Liên hệ qua Facebook để mua hàng"
(`https://www.facebook.com/ChamBanCam`).

---

## 6. Hai ngôn ngữ

Cờ Việt Nam / Anh ở góc trên bên phải. Trang nhớ lựa chọn của người xem cho lần sau
và cho mọi trang khác.

Mỗi đoạn chữ có hai bản đứng cạnh nhau, `lang="vi"` và `lang="en"`; CSS chỉ cho hiện một bản.
Chữ nằm trong thuộc tính (chữ thay thế của ảnh, nhãn đọc màn hình) thì để bản tiếng Anh ở
`data-alt-en` / `data-aria-en`. **Thêm đoạn mới thì nhớ thêm cả bản tiếng Anh.**

Bản tiếng Anh của phần 01, 02, 05 lấy từ tài liệu. **Bản tiếng Anh của phần 03 Sản phẩm bán lẻ (kể cả mô tả), 04 Hộp quà trải nghiệm (4 box),
06 Về chúng tôi, menu, nút bấm và vài tiêu đề nhỏ do người làm web dịch** — nhóm nên đọc lại.

---

## 7. Hiệu ứng — chỉ ở phần 05

Năm sợi ở mép phải (dưới đáy trên điện thoại), đổi màu theo cộng đồng và ảnh nền đứng yên khi
cuộn **chỉ bật ở phần 05 Trải nghiệm văn hóa**, nơi có năm cộng đồng. Các phần khác giữ gọn
kiểu Trúc Lâm / Miên Studio. Con thoi vẫn chạy mỗi khi người xem đổi phần.

- Bấm một sợi hoặc một cột người thì con thoi chạy và cả khu đổi màu theo trang phục cộng đồng đó.
- **Máy yếu, mạng chậm, hoặc người dùng bật giảm chuyển động** thì trang tự hạ bậc: bỏ con thoi,
  ảnh nền đứng yên thành ảnh thường. Nội dung vẫn đủ.
- **Màu chữ và màu mảng là hai biến tách riêng** (`--chu`, `--khoi`). Ba trong năm màu cộng đồng
  không đủ tương phản để làm chữ nhỏ, nên mỗi cộng đồng có một màu riêng cho chữ. Sửa màu thì giữ
  quy tắc này.
- **Hoa văn vẽ bằng mũi thêu chữ X**, không phải ô vuông đặc. Mỗi mũi lệch nhẹ theo vị trí nhưng
  có quy luật, nên vẽ lại bao nhiêu lần cũng ra đúng một hình.
- Ảnh nền phần 05 là `hg-ban-lang`, độ phủ 0.78 — sửa ở hàm `datAnhNen` cuối `index.html`.
  Làm nhạt ảnh thì dùng `filter`, **đừng dùng `opacity`** — `opacity` làm cả khối trong suốt nên
  ảnh nền phía sau lọt qua, nhìn nhoè nhoẹt.

---

## 8. Phim

Hai phim nằm cạnh nhau ở mục 04 Video của phần 05, chỉ tải khi người xem bấm nút; phim này chạy
thì phim kia tự dừng.

- **`story.mp4` ("Quy trình tạo ra thổ cẩm", 2 phút 22)** — phim nhóm tự quay tại Lùng Tám. Bản gốc
  trên Drive là `Story Telling.mp4` (107 MB, mã H.265): quá giới hạn 100 MB mỗi tệp của GitHub và
  Chrome/Firefox không phát được, nên trang dùng bản đã chuyển sang H.264 (26 MB) — cùng phim,
  cùng thời lượng.
- **`van-hoa.mp4` ("Văn hoá Hà Giang", 53 giây)** — phim do nhóm dựng nhưng ghép từ tư liệu của bên thứ ba: giây 15–25 có logo
**AMAZING HÀ GIANG — KỲ VĨ HÀ GIANG**, giây 26 có dòng ghi công **The Lover Lo Lo Chai — Jerry Tran**.
Hai thứ này vẫn nằm nguyên trong hình. Khối ghi nguồn đặt cạnh phim ở web cũ đã bỏ theo quyết định
của nhóm (11/2026). Nếu trang dùng cho mục đích thương mại thật sự, nên xin phép chủ tư liệu bằng
văn bản, hoặc thay bằng phim tự quay.

Video dùng mã H.264. Chrome và Firefox không phát được H.265 — thay video mới thì nhớ chuyển mã trước.

---

## 9. Ảnh xem trước khi gửi link

- Trang chủ dùng `assets/img/share.jpg` (1200×630).
- Mỗi trang sản phẩm dùng ảnh chính của sản phẩm đó. Ảnh nhỏ hơn 200px thì Facebook và Zalo bỏ qua,
  nên công cụ tự dùng `share.jpg` thay.

**Lưu ý nếu đổi tên miền:** các thẻ `og:url`, `og:image`, `twitter:image` phải là **đường dẫn tuyệt
đối** — để tương đối là ảnh xem trước không hiện. Ở trang chủ thì sửa trong `index.html`; ở trang
sản phẩm thì sửa `"dia_chi_web"` trong `cong-cu/san-pham.json` rồi chạy lại công cụ.

Facebook và Zalo giữ ảnh xem trước khá lâu. Sau khi đổi, dán link vào
`developers.facebook.com/tools/debug/` rồi bấm *Scrape Again*.

---

## 10. Cấu trúc thư mục

```
index.html                trang chủ: sáu phần, CSS và JavaScript riêng của trang chủ
san-pham/                 29 trang sản phẩm — DO CÔNG CỤ TẠO, đừng sửa tay
cong-cu/
  san-pham.json           danh sách box và sản phẩm bán lẻ
  dau-trang.html          thanh trên cùng + menu, dùng chung
  chan-trang.html         chân trang, dùng chung
  tao-trang.py            công cụ tạo trang (mục 4)
  tao-anh.py              chuyển một ảnh gốc thành đủ các bản trang cần (mục 4)
assets/
  css/chung.css           màu, chữ, menu, chân trang, thẻ và trang sản phẩm — dùng cho mọi trang
  js/chung.js             chuyển ngôn ngữ, menu điện thoại, ảnh hiện dần, bộ ảnh sản phẩm
  img/                    ảnh
  video/                  video H.264
.nojekyll                 báo GitHub đừng xử lý lại file
```

Mọi đường dẫn đều là đường dẫn tương đối, không có dấu gạch chéo ở đầu — nhờ vậy trang chạy được
cả khi nằm trong thư mục con của GitHub Pages.

**Tệp không còn trang nào dùng** (để lại, chưa xoá — khoảng 14 MB):
phim `hero-loop.mp4`, `vung-cao-loop.mp4`, `soi-loop.mp4`, và các ảnh
`anh-nhom`, `b1-thu-hoach`, `b3-noi-soi`, `cd-nung`, `cho-phien-moi`, `hat-then-dan-tinh`, `hg-dong-van`,
`hg-duong-deo`, `hg-lung-cu`, `hg-nho-que`, `hg-nui-doi`, `hg-ruong-bac-thang`, `hg-tham-ma`, `khung-cui`,
`le-cap-sac`, `lo-lo-ban-lang`, `lo-lo-mua`, `nha-san-tay`, `nha-trinh-tuong`, `nhom-cham-ban-cam`,
`phu-nu-dao`, `phu-nu-mong`, `poster-nhuom`, `poster-san-pham`, `poster-the-end`,
`poster-thung-lung`, `tay-dien-xuong`, `thung-lung-ban-lang`, `trai-nghiem` (mỗi ảnh gồm các bản
`.webp`, `.jpg`, `-tiny.webp`). Xoá đi thì repo nhẹ hơn; GitHub không tính băng thông cho tệp không ai mở.

---

## 11. Dung lượng và băng thông

GitHub cho mỗi repo tối đa 1 GB và khoảng 100 GB băng thông mỗi tháng, nên bình thường thì thoải mái.
Phim `story.mp4` (26 MB) và `van-hoa.mp4` (11 MB) chỉ tải khi người xem bấm nút (`preload="none"`), ảnh chỉ tải khi cuộn tới.

Nếu trang được chia sẻ rộng (vài nghìn lượt bấm xem phim) mà chạm trần băng thông, đưa phim lên
YouTube ở chế độ *không công khai* rồi thay khối phim bằng đường dẫn YouTube.
