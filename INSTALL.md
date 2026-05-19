# PhotoMax Windows Kurulum

Bu rehber, PhotoMax'i baska bir Windows bilgisayarda tek tikla calistirmak icindir.

## 1. Gerekli Kurulumlar

Once bunlari kur:

- Python 3.12 veya daha yeni
- Git
- Ekran karti suruculeri guncel olmalidir

Python kurarken su secenegi isaretle:

```text
Add python.exe to PATH
```

## 2. Projeyi Indir

PowerShell veya CMD ac:

```powershell
git clone https://github.com/AnkaGamestd/photomax.git
cd photomax
```

## 3. Tek Tikla Calistir

Dosya Gezgini'nde proje klasorunu ac ve bunu cift tikla:

```text
start_photomax.bat
```

Ilk calistirmada:

- Python sanal ortam kurulur
- Gerekli paketler indirilir
- Real-ESRGAN engine indirilir
- Tarayici otomatik acilir

Adres:

```text
http://127.0.0.1:8000
```

## Notlar

- Uygulamayi kullanirken acilan siyah terminal penceresini kapatma.
- PC uyku moduna girerse islem durur.
- Engine indirildikten sonra sonraki acilislar daha hizli olur.
- Internet sadece ilk kurulum ve engine indirme icin gerekir.

## Python PATH Sorunu

Python kurulu ama bulunamiyorsa, Python yolunu elle verebilirsin:

```powershell
$env:PHOTOMAX_PYTHON="C:\Users\KULLANICI\AppData\Local\Programs\Python\Python314\python.exe"
.\start_photomax.bat
```
