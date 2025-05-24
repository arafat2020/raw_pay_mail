# 📧 cPanel Python Email Sender via WSGI

This is a lightweight Python email API built specifically for **cPanel Python environments**. It listens for **HTTP POST requests** and sends HTML-formatted emails using `aiosmtplib` via your SMTP server.

## ✅ Features

- Compatible with **WSGI Python apps on cPanel**
- Uses **`aiosmtplib`** for async email delivery
- Clean, responsive **HTML email template**
- Sends from your SMTP server (e.g., GoDaddy, Zoho, Gmail)
- No third-party services required (like SendGrid or Mailgun)
- Validates required fields from the incoming JSON

---

## 🚀 Getting Started

### 1. Upload Your Files

Upload all Python files to a directory in your cPanel **Python app root** (e.g., `/home/user/email_sender/`).

Ensure `aiosmtplib` is installed in the Python environment you created in cPanel.

```bash
pip install aiosmtplib
