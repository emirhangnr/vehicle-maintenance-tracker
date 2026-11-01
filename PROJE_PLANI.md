# Araç Bakım Takip Sistemi — Proje Planı ve Çalışma Kuralları

> Bu dosya projenin tek referans kaynağıdır. Geliştirme sırasında alınan her karar burada yazılıdır;
> yeni bir karar alındığında önce bu dosya güncellenir, sonra kod yazılır.

---

## 1. Proje Künyesi

| Alan | Değer |
|---|---|
| Ders | YZM6443 — Modern Yazılım Mühendisliği: Bulut ve DevOps |
| Dönem | 2026-2027 Güz |
| Öğrenci | 4. sınıf |
| Proje | 9. Araç Bakım Takip Sistemi |
| İş alanı | Otomotiv (Automotive) |
| Kaynak liste | Sample_Project_Topics_List1, sıra 9 |
| Repo adı | `vehicle-maintenance-tracker` |
| Teslim | Aralık 2026 sonu (8 haftalık plan: 2 Kasım – 27 Aralık 2026) |

**Projenin tanımı:** Araçların bakım ve servis kayıtlarını yöneten, yaklaşan ve geciken bakımları
hatırlatan web uygulaması. Ders kapsamında asıl amaç kapsamlı bir uygulama geliştirmek değil;
Git, otomatik test, CI/CD, Docker ve Cloud süreçlerini uçtan uca uygulamaktır.

---

## 2. Kapsam — 4 Temel Fonksiyon

| # | Fonksiyon | Açıklama |
|---|---|---|
| F1 | **Araç yönetimi (CRUD)** | Araç ekleme, listeleme, güncelleme, silme. Plaka, marka, model, yıl, güncel kilometre. |
| F2 | **Bakım kaydı ekleme** | Bir araca bakım kaydı girme: bakım tipi, tarih, kilometre, maliyet, notlar, bir sonraki bakım tarihi/km. |
| F3 | **Bakım geçmişi görüntüleme** | Araç bazlı bakım geçmişi listesi, tarihe göre sıralama ve bakım tipine göre filtreleme. |
| F4 | **Bakım hatırlatma** | Tarih ve kilometre bazlı hesaplama: 30 gün içinde dolacak bakımlar "yaklaşan", tarihi/km'si geçmişler "geciken" olarak ayrı listelenir. |

### Kapsam Dışı (bilinçli kararlar)

Aşağıdakiler ders rubriğinde yer almadığı ve zamanı DevOps tarafından çalacağı için **yapılmayacak**:

- Kullanıcı yönetimi, kayıt/giriş, rol bazlı yetkilendirme
- Ödeme sistemi, bildirim/e-posta gönderimi
- PWA (manifest + service worker), mobil uygulama
- Karmaşık arayüz, SPA framework (React/Vue), tasarım sistemi
- Çoklu dil desteği

---

## 3. Teknoloji Yığını ve Gerekçeleri

| Katman | Seçim | Neden |
|---|---|---|
| Dil | Python 3.12 | Ders örneklerinde öneriliyor, ekosistem olgun |
| Web framework | **FastAPI** | REST endpoint'ler + `/health` doğal, test edilebilirliği yüksek, OpenAPI dokümantasyonu otomatik |
| Arayüz | **Jinja2** (sunucu taraflı HTML) | Tek servis, tek container; ayrı frontend deploy'u gerekmez |
| ORM | **SQLAlchemy** | Veritabanı-bağımsız kod: aynı kod SQLite ve Postgres üzerinde çalışır |
| Veritabanı (yerel + CI) | **SQLite** | Kurulum gerektirmez, testler izole ve hızlı çalışır |
| Veritabanı (bulut) | **Neon Postgres** (Free) | Veri kalıcı; 5 dk sonra uyuyor ama her sorguda otomatik uyanıyor, kart istemiyor |
| Paket yönetimi | **venv + requirements.txt** | Standart kütüphane, ek araç kurulumu yok; Dockerfile ile birebir aynı mantık |
| Test | **pytest + pytest-cov + httpx** | FastAPI TestClient ile entegrasyon ve birim testleri |
| CI/CD | **GitHub Actions** | Repo ile aynı yerde, Kanban ile entegre |
| Konteyner | **Docker** (+ docker-compose, yerel) | Rubrikte zorunlu |
| Bulut | **Render** (Free web service) | Kart istemiyor, otomatik `*.onrender.com` + HTTPS, gerçek konteyner, loglar panelde, Actions'tan deploy hook ile tetiklenebilir |
| Kanban | **GitHub Projects** | Issue/PR otomasyonu, Evidence alanları kendiliğinden dolar, CSV export var |
| Lint/format | **Yok** (karar: sadece pytest + coverage) | Üçüncü taraf araç eklenmedi. İleride gerekirse ayrıca onay alınacak |

### Neden Streamlit değil?

Listede önerilen araç Streamlit'ti ancak ders dokümanı teknolojiyi serbest bırakıyor
("Python (Flask/FastAPI), Node.js veya bildiğiniz başka bir teknoloji"). Streamlit'te
`/health` endpoint'i, test edilebilir servis katmanı ve yapılandırılmış loglama doğal gelmiyor;
rubrikteki Monitoring, Testing ve CI maddelerini FastAPI çok daha temiz karşılıyor.

### Neden Vercel değil?

Vercel artık `Dockerfile.vercel` ile konteyner çalıştırabiliyor, ancak:
ikinci bir Dockerfile gerektiriyor, imajı uzun ömürlü konteyner değil serverless fonksiyon olarak
çalıştırıyor ve CD'yi kendi yapıyor. Rubrikteki "çalışan container kanıtı" ve "CD pipeline" maddeleri
Render'da çok daha doğrudan gösteriliyor.

### Neden Supabase değil?

Supabase Free planında proje **1 hafta hareketsizlikte duraklatılıyor ve panelden elle uyandırmak
gerekiyor** — sunum günü uygulamanın ölü gelmesi riski var. Neon'un scale-to-zero'su her sorguda
otomatik uyanıyor. Ayrıca Supabase'in auth/storage/realtime özelliklerine ihtiyacımız yok.

---

## 4. Mimari ve Veri Modeli

### Katmanlı yapı

```
HTTP isteği
    ↓
Routers (FastAPI)          → HTTP, validasyon, şablon render
    ↓
Services (iş mantığı)      → saf Python, veritabanından bağımsız test edilebilir
    ↓
Repositories / Models      → SQLAlchemy, veritabanı erişimi
    ↓
SQLite (yerel) / Postgres (bulut)
```

**Kural:** İş mantığı `services/` katmanında, HTTP'den ve veritabanından bağımsız olacak.
Unit testlerin çoğu bu katmanı hedefleyecek — hızlı ve kırılgan olmayan testler böyle yazılır.

### Veri modeli (taslak)

**`vehicles`**

| Alan | Tip | Not |
|---|---|---|
| id | int, PK | |
| plate | str, unique, not null | Plaka |
| brand | str, not null | Marka |
| model | str, not null | Model |
| year | int | Model yılı |
| current_km | int, default 0 | Güncel kilometre |
| created_at | datetime | |

**`maintenance_records`**

| Alan | Tip | Not |
|---|---|---|
| id | int, PK | |
| vehicle_id | int, FK → vehicles.id, cascade delete | |
| maintenance_type | str, not null | Yağ değişimi, lastik, fren vb. |
| service_date | date, not null | Bakımın yapıldığı tarih |
| odometer_km | int | Bakım anındaki kilometre |
| cost | decimal | Maliyet (TL) |
| notes | text, nullable | |
| next_due_date | date, nullable | Bir sonraki bakım tarihi |
| next_due_km | int, nullable | Bir sonraki bakım kilometresi |
| created_at | datetime | |

### Endpoint taslağı

| Metot | Yol | İşlev |
|---|---|---|
| GET | `/` | Dashboard: yaklaşan ve geciken bakımlar |
| GET | `/vehicles` | Araç listesi |
| POST | `/vehicles` | Araç ekle |
| GET | `/vehicles/{id}` | Araç detayı + bakım geçmişi |
| POST | `/vehicles/{id}/edit` | Araç güncelle |
| POST | `/vehicles/{id}/delete` | Araç sil |
| POST | `/vehicles/{id}/maintenances` | Bakım kaydı ekle |
| GET | `/reminders` | Hatırlatma listesi |
| GET | `/health` | Sağlık kontrolü (JSON: status, db bağlantısı, versiyon) |
| GET | `/docs` | OpenAPI (FastAPI otomatik) |

---

## 5. Repo Yapısı

```
vehicle-maintenance-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI uygulaması, startup/shutdown
│   ├── config.py               # Ortam değişkenleri (DATABASE_URL vb.)
│   ├── database.py             # SQLAlchemy engine, session
│   ├── logging_config.py       # Yapılandırılmış JSON loglama
│   ├── models/                 # SQLAlchemy modelleri
│   ├── schemas/                # Pydantic şemaları
│   ├── services/               # İş mantığı (test edilen asıl katman)
│   ├── routers/                # HTTP rotaları
│   ├── templates/              # Jinja2 şablonları
│   └── static/                 # CSS
├── tests/
│   ├── conftest.py             # Test fixture'ları, in-memory SQLite
│   ├── test_vehicle_service.py
│   ├── test_maintenance_service.py
│   ├── test_reminder_service.py
│   └── test_api.py
├── docs/
│   ├── architecture.md         # Mimari ve veri modeli (teslim edilecek)
│   └── kanban/                 # Haftalık Kanban ekran görüntüleri
│       ├── hafta-01.png
│       └── ...
├── .github/
│   ├── ISSUE_TEMPLATE/task.md
│   └── workflows/ci.yml
├── scripts/
│   └── make_evidence.sh        # Kanban zip + evidence paketleme
├── .gitignore
├── .dockerignore
├── .env.example                # Yalnızca şablon değerler
├── Dockerfile
├── docker-compose.yml          # Yerel geliştirme
├── requirements.txt
├── requirements-dev.txt
├── PROJE_PLANI.md              # bu dosya
└── README.md
```

---

## 6. Çalışma Kuralları

### 6.1 Dil

| Nerede | Dil |
|---|---|
| Değişken, fonksiyon, sınıf, dosya adları | İngilizce |
| Commit mesajları, branch adları | İngilizce |
| Kod içi yorumlar | İngilizce |
| Kullanıcı arayüzü (şablonlar, hata mesajları) | Türkçe |
| README.md, docs/architecture.md, final rapor | Türkçe |
| Kanban kartları | Türkçe |

### 6.2 Git akışı — GitHub Flow

- `main` dalı **her zaman çalışır durumda** olacak. Doğrudan `main`'e commit atılmayacak.
- Her görev için dal açılacak: `feature/vehicle-crud`, `feature/reminder-service`, `fix/date-parsing`
- Dal → Pull Request → CI geçer → merge. PR açıklamasına `Closes #14` yazılacak.
- Merge sonrası dal silinecek.
- `main` dalına branch protection: CI geçmeden merge edilemez (5. haftadan itibaren).

### 6.3 Commit kuralları

**Conventional Commits** formatı, İngilizce, emir kipi:

```
feat: add vehicle CRUD endpoints
fix: correct overdue calculation for null next_due_date
test: add unit tests for reminder service
ci: add pytest job to GitHub Actions workflow
docs: update architecture diagram
chore: add .dockerignore
refactor: extract maintenance filtering into service layer
```

**Kesin kurallar:**
- Commit mesajlarında **hiçbir AI atfı bulunmayacak**: `Co-Authored-By`, `Generated with`,
  `🤖` benzeri hiçbir ifade yok. Kod yorumlarında ve dokümanlarda da AI referansı geçmeyecek.
- Her commit tek bir mantıksal değişikliği içerecek. "wip", "fix", "update" gibi anlamsız mesajlar yok.
- Commit'ler düzenli aralıklarla atılacak — tek seferde 2000 satırlık commit, Kanban'daki ilerleme
  takibini anlamsız kılar ve değerlendirmede olumsuz görünür.

### 6.4 Üçüncü taraf araç/paket kuralı

**Her yeni paket veya araç kurulumundan önce onay alınacak.** Aşağıdaki liste onaylanmış kabul
edilir; bunların dışındaki her şey ayrıca sorulacak.

**Çalışma zamanı (`requirements.txt`):**
`fastapi`, `uvicorn[standard]`, `jinja2`, `sqlalchemy`, `pydantic`, `pydantic-settings`,
`psycopg[binary]` (Postgres sürücüsü), `python-multipart` (form verisi)

**Geliştirme (`requirements-dev.txt`):**
`pytest`, `pytest-cov`, `httpx`

Tüm paket sürümleri sabitlenecek (`fastapi==0.1xx.x` gibi), böylece yerel ortam, CI ve
Docker imajı aynı sürümleri kullanacak.

---

## 7. Güvenlik ve Gizlilik

> **Repo public olacak.** Aşağıdaki kurallar istisnasız uygulanacak.

### 7.1 Repoya asla girmeyecekler

`.gitignore` ilk commit'te oluşturulacak ve şunları içerecek:

```
.env
.env.local
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/
*.db
*.sqlite
*.sqlite3
*.log
.DS_Store
.idea/
.vscode/
```

### 7.2 Sırların yönetimi

| Sır | Nerede durur | Repoda ne var |
|---|---|---|
| `DATABASE_URL` (Neon bağlantı adresi) | GitHub Secrets + Render Environment Variables | `.env.example` içinde şablon değer |
| Render Deploy Hook URL | GitHub Secrets | — |
| Herhangi bir API anahtarı / token | GitHub Secrets | — |

- **Kodda sabit yazılmış (hardcoded) hiçbir sır bulunmayacak.** Her şey ortam değişkeninden okunacak.
- **Dockerfile'a sır gömülmeyecek.** Değerler çalışma anında ortamdan gelecek.
- **Loglara sır veya kişisel veri yazılmayacak** — bağlantı adresi, parola, token asla loglanmaz.
- `.env.example` yalnızca şablon içerecek:
  ```
  DATABASE_URL=sqlite:///./vehicle_maintenance.db
  LOG_LEVEL=INFO
  APP_ENV=development
  ```

### 7.3 Koruma mekanizmaları

- **GitHub Secret Scanning + Push Protection** repo ayarlarından açılacak (public repolarda ücretsiz).
  Yanlışlıkla bir token push edilmeye kalkılırsa GitHub push'u reddeder.
- **Her push öncesi kontrol alışkanlığı:**
  ```bash
  git status
  git diff --staged
  ```
  Ne gönderildiği görülmeden push atılmayacak.
- İlk commit'ten önce `.gitignore` hazır olacak — sonradan eklemek geç kalmak demektir, çünkü
  dosya bir kez commit edildiyse Git geçmişinde kalır.

### 7.4 Sır sızarsa ne yapılır

Geçmişi temizlemek **tek başına yeterli değildir.** Sıra:

1. İlgili token/parola **derhal iptal edilir ve yenisi oluşturulur** (Neon'da bağlantı dizesi
   yenilenir, Render'da deploy hook yeniden üretilir).
2. Yeni değer GitHub Secrets ve Render'a girilir.
3. Ancak bundan sonra geçmiş temizliği düşünülür.

### 7.5 Veri gizliliği

- Seed/örnek verilerde **gerçek plaka, gerçek isim, gerçek TC kimlik numarası kullanılmayacak.**
  Tamamen uydurma veri (`34 ABC 123`, "Örnek Marka") kullanılacak.
- Ekran görüntülerinde kişisel bilgi, e-posta adresi veya token görünmeyecek — Kanban
  snapshot'ları yüklenmeden önce kontrol edilecek.
- Uygulama kişisel veri toplamıyor; bu durum README'de açıkça belirtilecek.

---

## 8. Kanban Kurulumu (GitHub Projects)

### 8.1 Kurulum adımları (1. hafta)

1. Repo → `Projects` → `New project` → **Board** görünümü
2. Sütunlar: `Todo` / `In Progress` / `Done` (varsayılan geliyor)
3. Proje ve repo **public** yapılacak — hoca aksi halde linki açtığında 404 alır
4. Otomasyonlar açılacak (`Workflows` menüsü):
   - Item added → `Todo`
   - Pull request opened → `In Progress`
   - Issue closed → `Done`
5. Etiketler oluşturulacak: `development`, `git`, `testing`, `ci-cd`, `docker`, `cloud`, `docs`
6. Haftalık milestone'lar oluşturulacak (`Hafta 1` … `Hafta 8`, bitiş tarihi haftanın pazarı);
   her issue kendi haftasının milestone'una bağlanacak
7. Proje URL'si not edilecek — 8 hafta boyunca **aynı link** teslim edilecek

### 8.2 Kart (issue) şablonu

`.github/ISSUE_TEMPLATE/task.md` dosyası ile her yeni issue şu yapıda açılacak:

```markdown
## Task Description
<Yapılacak çalışmayı açıklayan 1-2 cümle>

## Acceptance Criteria
- [ ] <Kriter 1>
- [ ] <Kriter 2>
- [ ] <Kriter 3>

## Evidence
- Commit:
- Pull Request:
- Test / CI / Docker / Cloud çıktısı:
```

**Örnek kart:**

> **#14 — Bakım hatırlatma servisini geliştir** · `development`
>
> **Task Description:** Araçların son bakım tarihi ve kilometre bilgisine göre yaklaşan ve geciken
> bakımları hesaplayan servis katmanı fonksiyonu yazılacak.
>
> **Acceptance Criteria:**
> - [ ] Bakım tarihi 30 gün içinde dolan araçlar "yaklaşan" olarak işaretleniyor
> - [ ] Tarihi geçmiş bakımlar "geciken" olarak ayrı listeleniyor
> - [ ] Fonksiyon için en az 1 unit test yazıldı ve geçiyor
>
> **Evidence:** Commit `a3f91c2` · PR #15 · Actions run #42

### 8.3 Haftalık rutin (her hafta sonu, ~15 dakika)

1. Panonun ekran görüntüsünü al → `docs/kanban/hafta-NN.png` olarak repoya kaydet
2. Biriken tüm görüntüleri zip'le: `scripts/make_evidence.sh`
3. OnlineBeykoz'a yükle: **snapshot (PNG) + geçmiş (ZIP) + pano URL'si**
4. 3-5 dakikalık ilerleme sunumuna hazırlan: Done / In Progress / Issues / To Do / Technical Evidence

> **Önemli:** Ekran görüntüleri o haftanın gerçek durumunu yansıtmalı ve hafta sonunda alınmalı.
> Geriye dönük toplu güncelleme, 8 haftalık ilerleme değerlendirmesinde fark edilir.

---

## 9. 8 Haftalık Plan

### Hafta 1 — 2-8 Kasım 2026 · Kurulum ve iskelet
`git` `development` `docs`

- [ ] GitHub repo oluştur (`vehicle-maintenance-tracker`, public)
- [ ] `.gitignore` oluştur — **ilk commit'te, kod yazmadan önce**
- [ ] Secret Scanning + Push Protection'ı etkinleştir
- [ ] GitHub Projects panosu, etiketler, otomasyonlar, issue template
- [ ] 8 haftalık görevleri `Todo` sütununa ekle (ilk haftalar detaylı, sonrakiler genel)
- [ ] `venv` kur, `requirements.txt` oluştur
- [ ] FastAPI iskeleti: `main.py` + `/health` endpoint'i
- [ ] README taslağı
- **Teslim:** Kanban snapshot + Kanban Board URL

### Hafta 2 — 9-15 Kasım · Gereksinimler, mimari, veri modeli
`development` `docs`

- [ ] Fonksiyonel gereksinimleri yaz (README)
- [ ] `docs/architecture.md`: katmanlı mimari + veri modeli + endpoint listesi
- [ ] SQLAlchemy modelleri: `Vehicle`, `MaintenanceRecord`
- [ ] `database.py`, `config.py` — `DATABASE_URL` ortam değişkeninden
- [ ] Seed verisi (uydurma araçlar)
- [ ] Branch: `feature/data-model` → PR → merge
- **Teslim:** snapshot + zip + URL

### Hafta 3 — 16-22 Kasım · F1 ve F2
`development` `git`

- [ ] **F1:** Araç CRUD — servis katmanı + rotalar + Jinja2 şablonları
- [ ] **F2:** Bakım kaydı ekleme
- [ ] Temel CSS, kullanılabilir arayüz
- [ ] Branch'ler: `feature/vehicle-crud`, `feature/maintenance-records`
- **Teslim:** snapshot + zip + URL

### Hafta 4 — 23-29 Kasım · F3, F4 ve testler
`development` `testing`

- [ ] **F3:** Bakım geçmişi görüntüleme (sıralama + filtreleme)
- [ ] **F4:** Bakım hatırlatma (yaklaşan / geciken hesaplama)
- [ ] Dashboard sayfası
- [ ] **En az 3 unit test** (hedef: 6-8): hatırlatma mantığı, CRUD, validasyon, API endpoint'leri
- [ ] `pytest --cov` ile kapsama raporu
- **Teslim:** snapshot + zip + URL

### Hafta 5 — 30 Kasım - 6 Aralık · CI Pipeline
`ci-cd` `testing`

- [ ] `.github/workflows/ci.yml`: checkout → Python kur → bağımlılıklar → pytest + coverage
- [ ] Her push ve PR'da tetiklenme
- [ ] `main` dalına branch protection: CI geçmeden merge yok
- [ ] README'ye CI rozeti (badge)
- [ ] Başarısız test senaryosunu bilerek dene → pipeline'ın build'i engellediğini kanıtla
- **Teslim:** snapshot + zip + URL

### Hafta 6 — 7-13 Aralık · Docker
`docker`

- [ ] `Dockerfile` — çok aşamalı (multi-stage) build, non-root kullanıcı, slim base image
- [ ] `.dockerignore`
- [ ] `docker-compose.yml` (yerel geliştirme için)
- [ ] `HEALTHCHECK` tanımı
- [ ] CI'a image build adımı ekle
- [ ] Yerel çalıştırma kanıtı: `docker build`, `docker run`, `docker ps` çıktıları
- **Teslim:** snapshot + zip + URL

### Hafta 7 — 14-20 Aralık · Cloud Deployment, CD, Monitoring
`cloud` `ci-cd`

- [ ] Neon projesi oluştur, `DATABASE_URL`'i al
- [ ] Render web service oluştur (Docker), ortam değişkenlerini gir
- [ ] İlk deploy → **Cloud Application URL** elde edilir
- [ ] GitHub Actions'a CD adımı: testler geçerse Render deploy hook'unu tetikle
- [ ] **Monitoring & Logging:**
  - `/health` endpoint'i (uygulama durumu + veritabanı bağlantısı + versiyon)
  - Yapılandırılmış JSON loglama (stdlib `logging`, özel formatter — ek paket yok)
  - Render log panelinden log kanıtları
  - Render Health Check ayarı → `/health`
- **Teslim:** snapshot + zip + URL

### Hafta 8 — 21-27 Aralık · Dokümantasyon, rapor, sunum
`docs`

- [ ] README.md finalize: proje tanımı, 4 temel fonksiyon, fonksiyonel gereksinimler, kurulum,
      çalıştırma, tüm bağlantılar
- [ ] `docs/architecture.md` finalize
- [ ] **Final_Project_Report.pdf** (4-6 sayfa, 7 bölüm — aşağıdaki tabloya göre)
- [ ] **Project_Links.txt**
- [ ] **Project_Evidence.zip**
- [ ] Kanban CSV export (Projects → Export view as CSV)
- [ ] Kaynak kod zip'i
- [ ] Final sunumu + demo provası
- **Teslim:** Tüm final paketi

---

## 10. Teslim Kontrol Listesi

### Final_Project_Report.pdf (4-6 sayfa)

| Bölüm | İçerik |
|---|---|
| 1. Project Overview | Amaç, kapsam, kullanılan teknolojiler |
| 2. Requirements & Architecture | 4 temel fonksiyon, katmanlı mimari, veri modeli |
| 3. Software Implementation | Geliştirilen fonksiyonlar + ekran görüntüleri |
| 4. DevOps Implementation | Git, branching/merging, otomatik test, CI/CD, Docker |
| 5. Cloud Deployment & Monitoring | Render, deployment, logging, health check |
| 6. Agile & Kanban Project Tracking | 8 haftalık ilerleme, karşılaşılan sorunlar ve çözümler |
| 7. Results & Conclusion | Sonuçlar, eksikler, değerlendirme |

### Project_Links.txt

```
Git Repository URL : https://github.com/<kullanici>/vehicle-maintenance-tracker
Kanban Board URL   : https://github.com/users/<kullanici>/projects/<n>
Cloud Application  : https://vehicle-maintenance-tracker.onrender.com
CI/CD Pipeline     : https://github.com/<kullanici>/vehicle-maintenance-tracker/actions
```

### Rubrik eşlemesi

| # | Rubrik maddesi | Nasıl karşılanıyor | Hafta |
|---|---|---|---|
| 1 | Software Implementation | 4 temel fonksiyon, çalışan uygulama, demo | 3-4 |
| 2 | Git & GitHub | Repo, commit geçmişi, ≥2 feature branch, PR kayıtları | 1-8 |
| 3 | Agile & Kanban | GitHub Projects, kart detayları, 8 haftalık geçmiş | 1-8 |
| 4 | Automated Testing | ≥3 unit test (hedef 6-8), pytest, coverage raporu | 4 |
| 5 | CI Pipeline | GitHub Actions `ci.yml`, başarılı run kayıtları | 5 |
| 6 | Docker | Dockerfile, image build, çalışan container kanıtı | 6 |
| 7 | Cloud Deployment | Render üzerinde çalışan uygulama URL'si | 7 |
| 8 | CD | Actions'tan tetiklenen otomatik deployment | 7 |
| 9 | Monitoring & Logging | `/health`, JSON loglar, Render log paneli | 7 |
| 10 | Documentation | README, architecture.md, Final Report PDF | 2, 8 |
| 11 | Final Presentation | Canlı demo: uygulama, Git, CI/CD, Docker, Cloud | 8 |

**Bonus (7-8. haftada değerlendirilecek):** Kubernetes, Terraform veya Ansible.
Şu an kapsam dışı — önce zorunlu maddelerin hepsi sağlam bitecek.

---

## 11. Riskler ve Önlemler

| Risk | Etki | Önlem |
|---|---|---|
| Render free servisi 15 dk sonra uyuyor, ilk istek ~1 dk sürüyor | Demo sırasında uygulama geç açılır | Sunumdan 5 dk önce URL'yi açıp uyandır |
| Neon 5 dk sonra uyku moduna geçiyor | İlk sorgu birkaç yüz ms gecikir | Pratikte sorun değil; aynı ısıtma adımı yeterli |
| Render free: 750 saat/ay, 500 build dakikası | Kota dolarsa servis askıya alınır | Tek servis kullanılacak; gereksiz deploy'dan kaçınılacak |
| Yanlışlıkla sır commit'lemek | Güvenlik açığı | `.gitignore` ilk commit'te + Push Protection + her push öncesi `git diff --staged` |
| Haftalık snapshot'ı unutmak | İlerleme kanıtı eksik kalır | Hafta sonu rutini takvime hatırlatıcı olarak kurulacak |
| Toplu/geç commit atma | Kanban ilerlemesi gerçekçi görünmez | Küçük ve sık commit; her görev kendi dalında |
| Son haftaya iş bırakmak | Rapor ve evidence yetişmez | README ve architecture.md 2. haftada başlar, her hafta güncellenir |

---

## 12. Karar Kaydı

| Tarih | Karar | Gerekçe |
|---|---|---|
| 2026-10-31 | FastAPI + Jinja2, tek servis | Test edilebilirlik ve `/health` kolaylığı |
| 2026-10-31 | Render (bulut) | Kart istemiyor, gerçek konteyner, otomatik domain |
| 2026-10-31 | SQLite (yerel/CI) + Neon Postgres (bulut) | Kalıcı veri + hızlı testler |
| 2026-10-31 | GitHub Projects (Kanban) | Issue/PR otomasyonu, CSV export |
| 2026-10-31 | 4 temel fonksiyon | Listeyi tam karşılar, zamanında biter |
| 2026-10-31 | Kod İngilizce / arayüz + doküman Türkçe | Sektör standardı + hocanın okunabilirliği |
| 2026-10-31 | GitHub Flow (main + feature/* + PR) | Tek kişilik projeye uygun ölçek, PR kanıtı üretir |
| 2026-10-31 | venv + requirements.txt | Standart kütüphane, ek araç kurulumu yok |
| 2026-10-31 | Lint aracı yok (sadece pytest + coverage) | Üçüncü taraf araç eklenmedi |
| 2026-10-31 | PWA kapsam dışı | Rubrikte yok, puan getirmiyor |
| 2026-10-31 | Bonus teknolojiler ertelendi | Önce zorunlu maddeler |
| 2026-11-01 | Haftalık GitHub milestone'ları | Haftalık sunum ve snapshot'larda ilerlemeyi gruplar, CSV export'ta hafta bilgisi kalır |
