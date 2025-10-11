from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime

APP_ID = 'com.finaccel.android'

print("🚀 Mulai scraping reviews Kredivo...")
print("=" * 50)

try:
    result, continuation_token = reviews(
        APP_ID,
        lang='id',
        country='id',
        sort=Sort.NEWEST,
        count=2000
    )
    
    df = pd.DataFrame(result)
    
    print(f"✅ Berhasil scraping {len(df)} reviews!")
    print("\n📊 Kolom yang tersedia:")
    for i, col in enumerate(df.columns.tolist(), 1):
        print(f"   {i}. {col}")
    
    print("\n⭐ Distribusi Rating:")
    rating_dist = df['score'].value_counts().sort_index()
    for rating, count in rating_dist.items():
        bar = "█" * int(count/10)
        print(f"   {rating} bintang: {count:4d} {bar}")
    
    print(f"\n📈 Rata-rata rating: {df['score'].mean():.2f}/5.0")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'kredivo_reviews_{timestamp}.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n💾 Data tersimpan: {filename}")

    print("\n👀 Preview 3 review pertama:")
    print("=" * 50)
    for idx, row in df.head(3).iterrows():
        print(f"\n[{row['userName']}] - Rating: {row['score']}⭐")
        print(f"Tanggal: {row['at']}")
        print(f"Review: {row['content'][:150]}...")
        print("-" * 50)
    
    print("\n✨ Scraping selesai! Silakan cek file CSV-nya.")
    
except Exception as e:
    print(f"❌ Error terjadi: {str(e)}")
    print("Coba periksa koneksi internet atau package name aplikasi.")