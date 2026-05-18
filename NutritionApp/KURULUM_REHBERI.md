# Akıllı Yemek Planlama Sistemi - Kurulum Rehberi

## 🚨 ÖNEMLİ: Başka Bir Bilgisayarda Çalıştırmak İçin Yapılması Gerekenler

### 1. SQL Server Bağlantı Bilgilerini Değiştirme

**`app.py` dosyasının 108. satırını değiştirmeniz GEREKİYOR:**

```python
self.db = Database(
    server=r"DESKTOP-JTV1ES3\SQLEXPRESS",  # ← BURAYI DEĞİŞTİRİN
    database="NutritionApp",
    trusted_connection=True,
)
```

#### Bilgisayar Adını Öğrenme:
1. **Windows tuşu + R** tuşlarına basın
2. `cmd` yazıp Enter'a basın
3. Komut satırına `hostname` yazın ve Enter'a basın
4. Çıkan bilgisayar adını not edin

#### SQL Server Instance Adını Öğrenme:
1. SQL Server Management Studio (SSMS) açın
2. Bağlantı penceresinde "Server name" kısmına bakın
3. Genellikle şu formatta olur: `BILGISAYAR_ADI\SQLEXPRESS` veya `BILGISAYAR_ADI\MSSQLSERVER`
4. Eğer varsayılan instance kullanıyorsanız sadece bilgisayar adı yeterli olabilir

#### Örnek:
Eğer bilgisayar adınız `MYPC` ve SQL Server instance adınız `SQLEXPRESS` ise:
```python
server=r"MYPC\SQLEXPRESS"
```

Eğer varsayılan instance kullanıyorsanız:
```python
server=r"MYPC"
```

---

### 2. SQL Server Kurulumu ve Veritabanı Oluşturma

#### Gereksinimler:
- **SQL Server Express** veya **SQL Server** kurulu olmalı
- SQL Server servisinin çalışıyor olması gerekiyor

#### Veritabanını Oluşturma:
1. SQL Server Management Studio (SSMS) açın
2. Kendi bilgisayarınıza bağlanın
3. `NutritionApp.sql` dosyasını açın
4. Tüm içeriği seçip çalıştırın (F5)
5. Veritabanı ve tablolar oluşturulacak

**NOT:** `NutritionApp.sql` dosyasındaki dosya yolları farklı bir bilgisayarda çalışmayabilir. Eğer hata alırsanız, dosya yollarını kendi SQL Server kurulumunuza göre düzenleyin.

---

### 3. Python Paketlerini Yükleme

#### Gereksinimler:
- **Python 3.7 veya üzeri** kurulu olmalı

#### Adımlar:
1. Terminal/Command Prompt açın
2. Proje klasörüne gidin
3. Şu komutu çalıştırın:
```bash
pip install -r requirements.txt
```

Bu komut şu paketleri yükleyecek:
- `customtkinter>=5.2.0` (Modern GUI için)
- `pyodbc>=5.0.0` (SQL Server bağlantısı için)

---

### 4. ODBC Driver Kontrolü

**`database.py` dosyasında varsayılan driver:**
```python
driver: str = "{ODBC Driver 17 for SQL Server}"
```

Eğer bağlantı hatası alırsanız:

1. Yüklü ODBC driver'ları kontrol edin:
   - Windows: `ODBC Data Sources (64-bit)` uygulamasını açın
   - "Drivers" sekmesine bakın

2. Yaygın driver isimleri:
   - `{ODBC Driver 17 for SQL Server}`
   - `{ODBC Driver 18 for SQL Server}`
   - `{SQL Server Native Client 11.0}`
   - `{SQL Server}`

3. Eğer farklı bir driver kullanıyorsanız, `database.py` dosyasının 16. satırını değiştirin:
```python
driver: str = "{YUKLU_DRIVER_ADI}"
```

---

### 5. Uygulamayı Çalıştırma

1. Terminal/Command Prompt açın
2. Proje klasörüne gidin
3. Şu komutu çalıştırın:
```bash
python app.py
```

veya

```bash
python main.py
```

---

## ❌ YAPILMAMASI GEREKENLER

1. **`app.py` dosyasındaki server adını değiştirmeden çalıştırmayın** - Bağlantı hatası alırsınız
2. **Veritabanını oluşturmadan çalıştırmayın** - Tablo bulunamadı hatası alırsınız
3. **Python paketlerini yüklemeden çalıştırmayın** - Import hatası alırsınız
4. **SQL Server servisinin kapalı olduğu durumda çalıştırmayın** - Bağlantı hatası alırsınız

---

## 🔧 Sorun Giderme

### "Veritabanına bağlanılamadı" Hatası:
- SQL Server servisinin çalıştığından emin olun
- Server adının doğru olduğundan emin olun
- Windows Authentication'ın aktif olduğundan emin olun
- Firewall ayarlarını kontrol edin

### "ODBC Driver bulunamadı" Hatası:
- Microsoft ODBC Driver for SQL Server'ı yükleyin
- Driver adının doğru olduğundan emin olun

### "Tablo bulunamadı" Hatası:
- `NutritionApp.sql` dosyasını çalıştırdığınızdan emin olun
- Veritabanı adının doğru olduğundan emin olun

### "ModuleNotFoundError" Hatası:
- `pip install -r requirements.txt` komutunu çalıştırdığınızdan emin olun
- Python sürümünüzün 3.7 veya üzeri olduğundan emin olun

---

## 📝 Özet Checklist

- [ ] SQL Server kurulu ve çalışıyor
- [ ] `NutritionApp.sql` dosyası çalıştırıldı ve veritabanı oluşturuldu
- [ ] `app.py` dosyasındaki server adı değiştirildi
- [ ] Python 3.7+ kurulu
- [ ] `pip install -r requirements.txt` komutu çalıştırıldı
- [ ] ODBC Driver yüklü ve doğru driver adı kullanılıyor
- [ ] Uygulama başarıyla çalışıyor

---

## 💡 İpucu

Eğer birden fazla bilgisayarda çalıştıracaksanız, `app.py` dosyasındaki server adını bir config dosyasına taşıyabilirsiniz. Bu şekilde her bilgisayarda sadece config dosyasını değiştirmeniz yeterli olur.

