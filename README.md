# Araç Bakım Takip Sistemi

Araçların bakım ve servis kayıtlarını yöneten, yaklaşan ve geciken bakımları hatırlatan web uygulaması.

> YZM6443 Modern Yazılım Mühendisliği: Bulut ve DevOps — dönem projesi.
> Projenin asıl amacı Git, otomatik test, CI/CD, Docker ve bulut süreçlerini uçtan uca uygulamaktır.

**Durum:** Geliştirme aşamasında (Hafta 2 — gereksinimler, mimari, veri modeli)

## Temel Fonksiyonlar

| # | Fonksiyon | Açıklama |
|---|---|---|
| F1 | Araç yönetimi (CRUD) | Araç ekleme, listeleme, güncelleme, silme |
| F2 | Bakım kaydı ekleme | Bakım tipi, tarih, kilometre, maliyet, notlar, sonraki bakım tarihi/km |
| F3 | Bakım geçmişi | Araç bazlı geçmiş, tarihe göre sıralama, bakım tipine göre filtreleme |
| F4 | Bakım hatırlatma | 30 gün içinde dolacak bakımlar "yaklaşan", tarihi/km'si geçenler "geciken" |

## Fonksiyonel Gereksinimler

### F1 — Araç yönetimi

- **FR-1.1** Kullanıcı plaka, marka, model, model yılı ve güncel kilometre girerek araç ekleyebilmelidir.
- **FR-1.2** Plaka, marka ve model zorunludur; plaka sistemde benzersiz olmalıdır.
- **FR-1.3** Model yılı ve kilometre negatif olamaz; model yılı gelecek yıldan büyük olamaz.
- **FR-1.4** Kayıtlı araçlar liste halinde görüntülenebilmelidir.
- **FR-1.5** Bir aracın bilgileri güncellenebilmelidir.
- **FR-1.6** Bir araç silindiğinde ona ait tüm bakım kayıtları da silinmelidir.

### F2 — Bakım kaydı ekleme

- **FR-2.1** Kullanıcı bir araca bakım tipi, bakım tarihi, bakım anındaki kilometre, maliyet ve not girerek
  bakım kaydı ekleyebilmelidir.
- **FR-2.2** Bakım tipi ve bakım tarihi zorunludur; kilometre ve maliyet negatif olamaz.
- **FR-2.3** Kayda isteğe bağlı olarak bir sonraki bakım tarihi ve/veya kilometresi girilebilmelidir.
- **FR-2.4** Bir sonraki bakım tarihi, bakım tarihinden önce olamaz.

### F3 — Bakım geçmişi

- **FR-3.1** Araç detay sayfasında o araca ait tüm bakım kayıtları listelenmelidir.
- **FR-3.2** Liste bakım tarihine göre (varsayılan: en yeni önce) sıralanabilmelidir.
- **FR-3.3** Liste bakım tipine göre filtrelenebilmelidir.

### F4 — Bakım hatırlatma

- **FR-4.1** Bir sonraki bakım tarihi bugünden itibaren 30 gün içinde olan kayıtlar **yaklaşan** olarak listelenmelidir.
- **FR-4.2** Bir sonraki bakım tarihi geçmiş **veya** aracın güncel kilometresi bir sonraki bakım kilometresine
  ulaşmış kayıtlar **geciken** olarak listelenmelidir.
- **FR-4.3** Geciken bir kayıt aynı anda yaklaşan listesinde gösterilmez.
- **FR-4.4** Yalnızca her aracın her bakım tipindeki **en son** kaydı hatırlatmaya dahil edilir; yeni bir bakım
  girildiğinde eski hatırlatma kendiliğinden düşer.
- **FR-4.5** Ana sayfa (dashboard) yaklaşan ve geciken bakımları ayrı bölümlerde göstermelidir.

### Fonksiyonel olmayan gereksinimler

- **NFR-1** Uygulama `GET /health` ile durumunu JSON olarak bildirmelidir.
- **NFR-2** Veritabanı bağlantısı ve diğer ayarlar yalnızca ortam değişkenlerinden okunmalıdır.
- **NFR-3** Aynı kod yerelde SQLite, bulutta PostgreSQL ile çalışmalıdır.
- **NFR-4** Arayüz ve hata mesajları Türkçe olmalıdır.

### Kapsam dışı

Kullanıcı yönetimi ve giriş, bildirim/e-posta gönderimi, ödeme, PWA/mobil uygulama ve çoklu dil desteği
bu projenin kapsamında değildir.

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
| Kanban Board | https://github.com/users/emirhangnr/projects/1 |
| CI/CD Pipeline | _eklenecek_ |
| Bulut Uygulaması | _eklenecek_ |

## Gizlilik

Uygulama kişisel veri toplamaz. Örnek verilerin tamamı uydurmadır; gerçek plaka veya isim içermez.
Bağlantı bilgileri ve diğer sırlar yalnızca ortam değişkenlerinden okunur, repoda tutulmaz.
