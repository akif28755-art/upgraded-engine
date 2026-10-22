# TJK FormLab — Bulut dağıtım paketi

## GitHub + Render (ücretsiz plan) kurulum
1. ZIP'i çıkarın.
2. GitHub'da yeni bir **Private** veya **Public** depo oluşturun.
3. Bu klasörün **içindeki dosyaları** deponun köküne yükleyin (index.html, assets/, cloud_server.py, render.yaml vb.).
4. Render'a girin: https://render.com/
5. New + → Blueprint seçin ve GitHub deposunu bağlayın.
6. Render `render.yaml` dosyasını algılar; servisi oluşturun.
7. Dağıtım bittikten sonra Render'ın verdiği `https://...onrender.com` adresini açın.
8. Sağlık testi: `https://SİTE-ADRESİNİZ/api/health` → `{"ok": true, ...}` dönmeli.

## API key
Harici API key gerekmiyor. Sunucu Python standart kütüphanesini kullanır.

## ÖNEMLİ SINIRLAMA
Bu paket web arayüzünü ve bulut uyumlu API iskeletini yayımlar. **Canlı TJK veri çekme işlemi bu pakette henüz bulut sunucusuna taşınmış değildir.** `/api/refresh` bu yüzden açıkça `live_source_not_configured` bildirir ve sahte yarış verisi üretmez. Önce web uygulamasının yayınlandığını doğrulayın; ardından Windows PowerShell tabanlı TJK veri toplayıcısının mantığı Python/bulut uyumlu hâle getirilmelidir. Bu adım tamamlanmadan canlı yarış verilerinin çalıştığı varsayılmamalıdır.

## Ücretsiz barındırma
Render ücretsiz servisleri boşta kaldığında uyuyabilir ve kullanım/çalışma limitleri vardır; kesintisiz 7/24 çalışma garantisi yoktur.

## Yerel kontrol
`python cloud_server.py` komutu ile başlatılabilir. Windows'ta Python 3 yüklü olmalıdır. Varsayılan port 10000.
