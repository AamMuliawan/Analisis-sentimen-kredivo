import pandas as pd
import re
import string
from datetime import datetime
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

print("Memuat data...")
df = pd.read_csv('kredivo_reviews_20251009_070032.csv')
print(f"Total review: {len(df)}\n")

# ===== 1. CASEFOLDING =====
print("[1/6] Casefolding...")
df['casefolding'] = df['content'].str.lower()

# ===== 2. TOKENISASI =====
print("[2/6] Tokenisasi...")
df['tokenisasi'] = df['casefolding'].apply(lambda x: x.split() if pd.notna(x) else [])
df['tokenisasi_text'] = df['tokenisasi'].apply(lambda x: ' '.join(x))

# ===== 3. PENGHAPUSAN STOPWORDS =====
print("[3/6] Penghapusan Stopwords...")
factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()

df['stopword_removal'] = df['tokenisasi_text'].apply(lambda x: stopword_remover.remove(x) if x else "")

# ===== 4. PENGHAPUSAN TANDA BACA =====
print("[4/6] Penghapusan Tanda Baca...")

def remove_punctuation(text):
    if pd.isna(text) or text == "":
        return ""
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['punctuation_removal'] = df['stopword_removal'].apply(remove_punctuation)

# ===== 5. STEMMING =====
print("[5/6] Stemming...")
stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()

df['stemming'] = df['punctuation_removal'].apply(lambda x: stemmer.stem(x) if x else "")

# ===== 6. PENGHAPUSAN URL DAN MENTION =====
print("[6/6] Penghapusan URL dan Mention...")

def remove_url_mention(text):
    if pd.isna(text) or text == "":
        return ""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['final_text'] = df['stemming'].apply(remove_url_mention)

# ===== SIMPAN HASIL =====
print("\nMenyimpan hasil...")
output_cols = ['userName', 'score', 'at', 'content', 
               'casefolding', 'tokenisasi_text', 'stopword_removal', 
               'punctuation_removal', 'stemming', 'final_text']
df_output = df[output_cols]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'kredivo_preprocessed_{timestamp}.csv'
df_output.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"✅ Tersimpan: {output_file}")

# ===== CONTOH HASIL =====
print("\n" + "="*70)
print("CONTOH 3 HASIL PREPROCESSING")
print("="*70)

for i in range(min(3, len(df))):
    row = df.iloc[i]
    print(f"\nReview #{i+1} | Rating: {row['score']}⭐")
    print(f"1. Original          : {row['content'][:70]}...")
    print(f"2. Casefolding       : {row['casefolding'][:70]}...")
    print(f"3. Tokenisasi        : {row['tokenisasi_text'][:70]}...")
    print(f"4. Stopword Removal  : {row['stopword_removal'][:70]}...")
    print(f"5. Punctuation Remove: {row['punctuation_removal'][:70]}...")
    print(f"6. Stemming          : {row['stemming'][:70]}...")
    print(f"7. Final (URL/Mention): {row['final_text'][:70]}...")
    print("-"*70)

print(f"\n🎯 Selesai! Total: {len(df)} reviews diproses")
print(f"📊 Rata-rata rating: {df['score'].mean():.2f}/5.0")