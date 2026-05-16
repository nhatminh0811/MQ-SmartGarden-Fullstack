# Dự án cửa hàng cây cảnh

Một ứng dụng web bán cây cảnh được xây dựng trên Django với các chức năng quản lý sản phẩm, đơn hàng, thanh toán, người dùng, và một số tính năng hỗ trợ bền vững.

## Tổng quan

Ứng dụng này cung cấp:

- Quản lý sản phẩm và nội dung cây cảnh
- Thanh toán trực tuyến và đơn hàng
- Quản lý người dùng, tài khoản và hồ sơ
- Tích hợp API cho phần frontend và hệ thống quản lý
- Hỗ trợ chất lượng sản phẩm và đánh giá/kiểm định
- Khả năng mở rộng cho dự án thương mại điện tử nhỏ

## Công nghệ

- Python 3.x
- Django 4.2+
- Django REST Framework
- PostgreSQL (khuyến nghị) hoặc SQLite
- Stripe cho thanh toán
- TensorFlow cho inference kiểm định chất lượng
- Pillow cho xử lý ảnh

## Cài đặt

1. Tạo virtual environment:

```bash
python -m venv .venv
```

2. Kích hoạt môi trường:

- Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

- Windows Command Prompt:

```cmd
.\.venv\Scripts\activate
```

3. Cài đặt dependency:

```bash
pip install -r requirements.txt
```

4. Thiết lập biến môi trường

Tạo file `.env` nếu cần và cấu hình các biến môi trường như:

```env
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
STRIPE_API_KEY=your_stripe_api_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret
```

5. Chạy migrations:

```bash
python manage.py migrate
```

6. Tạo superuser nếu cần:

```bash
python manage.py createsuperuser
```

7. Khởi động server:

```bash
python manage.py runserver
```

## Cấu trúc dự án

- `brfn/` - Cấu hình Django và routing chính
- `products/` - Quản lý sản phẩm, API, views, recommendation, kiểm định chất lượng
- `orders/` - Quản lý đơn hàng, báo cáo, trạng thái giao hàng
- `payments/` - Xử lý thanh toán và tích hợp thanh toán
- `sustainability/` - Tính năng liên quan đến bền vững và báo cáo môi trường
- `users/` - Mô hình người dùng, bảo mật và views liên quan đến tài khoản
- `templates/` - Giao diện HTML cho frontend
- `media/` - Thư mục chứa ảnh và nội dung tải lên

## Chạy thử

Truy cập ứng dụng trên:

```
http://127.0.0.1:8000/
```

Và trang admin trên:

```
http://127.0.0.1:8000/admin/
```

## Ghi chú

- Dự án hiện có thể chạy với SQLite mặc định. Nếu dùng PostgreSQL, cài `psycopg2-binary` và cấu hình `DATABASE_URL` tương ứng.
- TensorFlow được sử dụng cho các module kiểm định chất lượng sản phẩm.

## Mở rộng

- Thêm chức năng tìm kiếm sản phẩm nâng cao
- Tối ưu SEO và trải nghiệm người dùng cho giao diện frontend
- Hoàn thiện quản lý đơn hàng và báo cáo tài chính
- Tích hợp hệ thống đánh giá, sản phẩm yêu thích, và thông báo người dùng

---

Cảm ơn bạn đã sử dụng dự án này! Nếu cần hỗ trợ hoặc phát triển thêm, hãy mở rộng file README và cập nhật các hướng dẫn phù hợp.