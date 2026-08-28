# QA Builder

Tool xây dựng dataset Q&A từ tài liệu Markdown (`.md`).

## 1. Yêu cầu

* Python 3.10+
* Git
* Gemini API Key

## 2. Clone project

```bash
git clone https://github.com/Tuakkiek/qa-builder.git
cd qa-builder
```

## 3. Tạo môi trường ảo `.venv`

### Windows

```bash
python -m venv .venv
```

### Kích hoạt `.venv`

**Windows CMD:**

```cmd
.venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Git Bash:**

```bash
source .venv/Scripts/activate
```

Sau khi kích hoạt thành công, terminal sẽ có dạng:

```text
(.venv) C:\...\qa-builder>
```

## 4. Cài thư viện

```bash
pip install -r requirements.txt
```

Nếu project chưa có `requirements.txt`, có thể cài thủ công:

```bash
pip install sentence-transformers tqdm google-genai
```

## 5. Kiểm tra môi trường

```bash
python -c "import sentence_transformers, tqdm, google.genai; print('Environment OK')"
```

Nếu terminal hiển thị:

```text
Environment OK
```

thì môi trường đã được cài đặt thành công.

## 6. Cấu hình Gemini API Key

Tạo file `.env` ở thư mục gốc project:

```text
GEMINI_API_KEY=your_api_key_here
```

**Không commit file `.env` lên Git.**

Thêm vào `.gitignore`:

```text
.venv/
.env
__pycache__/
logs/
output/
```

## 7. Chuẩn bị dữ liệu

Project hiện tại **chỉ nhận file Markdown (`.md`)**.

Đặt các file Markdown vào:

```text
data/
├── document1.md
├── document2.md
└── document3.md
```

Không xử lý:

```text
.pdf
.docx
.txt
```
