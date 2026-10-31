# Araç Bakım Takip Sistemi

Araçların bakım ve servis kayıtlarını yöneten, yaklaşan ve geciken bakımları hatırlatan web uygulaması.

> YZM6443 Modern Yazılım Mühendisliği: Bulut ve DevOps — dönem projesi.
> Projenin asıl amacı Git, otomatik test, CI/CD, Docker ve bulut süreçlerini uçtan uca uygulamaktır.

**Durum:** Geliştirme aşamasında (Hafta 1 — kurulum ve iskelet)

## Temel Fonksiyonlar

| # | Fonksiyon | Açıklama |
|---|---|---|
| F1 | Araç yönetimi (CRUD) | Araç ekleme, listeleme, güncelleme, silme |
| F2 | Bakım kaydı ekleme | Bakım tipi, tarih, kilometre, maliyet, notlar, sonraki bakım tarihi/km |
| F3 | Bakım geçmişi | Araç bazlı geçmiş, tarihe göre sıralama, bakım tipine göre filtreleme |
| F4 | Bakım hatırlatma | 30 gün içinde dolacak bakımlar "yaklaşan", tarihi/km'si geçenler "geciken" |

## Teknolojiler

- Python 3.12, FastAPI, Jinja2, SQLAlchemy
- SQLite (yerel ve CI), Neon Postgres (bulut)
- pytest, pytest-cov
- GitHub Actions (CI/CD), Docker, Render

## Kurulum

> Uygulama kodu henüz eklenmedi; aşağıdaki adımlar sonraki haftalarda geçerli olacaktır.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

## Çalıştırma

```bash
uvicorn app.main:app --reload
```

## Test

```bash
pytest
pytest --cov=app --cov-report=term-missing
```

## Bağlantılar

| | |
|---|---|
| Kanban Board | _eklenecek_ |
| CI/CD Pipeline | _eklenecek_ |
| Bulut Uygulaması | _eklenecek_ |

## Gizlilik

Uygulama kişisel veri toplamaz. Örnek verilerin tamamı uydurmadır; gerçek plaka veya isim içermez.
Bağlantı bilgileri ve diğer sırlar yalnızca ortam değişkenlerinden okunur, repoda tutulmaz.
