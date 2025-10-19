#!/usr/bin/env python
"""
COMPLETE REMAINING TASKS - Khusus untuk file kredivo_preprocessed_20251011_172307.csv
Menyelesaikan: Normalisasi, Remove Duplikat, Bi-gram, Tri-gram, WordCloud
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

print("""
========================================================================
        MENYELESAIKAN TUGAS CPMK 2 - REMAINING TASKS
========================================================================
""")

# ============================================
# LOAD YOUR SPECIFIC FILE
# ============================================
print("📁 Loading your preprocessed file...")
filename = 'kredivo_preprocessed_20251011_172307.csv'

try:
    df = pd.read_csv(filename, encoding='utf-8')
    print(f"✅ Successfully loaded: {filename}")
    print(f"   Total reviews: {len(df)}")
    print(f"   Columns: {', '.join(df.columns.tolist())}")
except:
    print(f"❌ File {filename} tidak ditemukan!")
    print("   Pastikan file ada di folder yang sama dengan script ini")
    exit(1)

# ============================================
# STEP 1: NORMALISASI KATA
# ============================================
print("\n" + "="*70)
print("STEP 1: NORMALISASI KATA BAHASA INDONESIA")
print("="*70)

# Comprehensive Indonesian slang dictionary
SLANG_DICT = {
    # Common abbreviations
    'gak': 'tidak', 'ga': 'tidak', 'g': 'tidak', 'ngga': 'tidak', 'nggak': 'tidak',
    'gk': 'tidak', 'kagak': 'tidak', 'kaga': 'tidak', 'ndak': 'tidak',
    'udah': 'sudah', 'uda': 'sudah', 'dah': 'sudah', 'udh': 'sudah', 'sdh': 'sudah',
    'gimana': 'bagaimana', 'gmn': 'bagaimana', 'gmana': 'bagaimana', 'bgmn': 'bagaimana',
    'aja': 'saja', 'aj': 'saja', 'ajah': 'saja', 'doang': 'saja', 'doank': 'saja',
    'bgt': 'sangat', 'bngt': 'sangat', 'bngtt': 'sangat', 'banget': 'sangat',
    'knp': 'kenapa', 'knapa': 'kenapa', 'napa': 'kenapa', 'ngapa': 'kenapa',
    'yg': 'yang', 'yng': 'yang', 'yhg': 'yang',
    'dgn': 'dengan', 'dg': 'dengan', 'dgn': 'dengan',
    'utk': 'untuk', 'u/': 'untuk', 'untk': 'untuk', 'buat': 'untuk',
    'krn': 'karena', 'karna': 'karena', 'krna': 'karena',
    'skrg': 'sekarang', 'skrng': 'sekarang', 'skg': 'sekarang',
    'trs': 'terus', 'trz': 'terus', 'trus': 'terus', 'teross': 'terus',
    'bs': 'bisa', 'bsa': 'bisa', 'isa': 'bisa',
    'jg': 'juga', 'jga': 'juga', 'jugak': 'juga',
    'lg': 'lagi', 'lgi': 'lagi', 'lagee': 'lagi',
    'sm': 'sama', 'sma': 'sama', 'ama': 'sama',
    'dl': 'dulu', 'dlu': 'dulu', 'doloe': 'dulu',
    'dr': 'dari', 'dri': 'dari', 'darii': 'dari',
    'tp': 'tapi', 'tpi': 'tapi', 'tetapi': 'tapi',
    'jd': 'jadi', 'jdi': 'jadi', 'jadii': 'jadi',
    'hrs': 'harus', 'hrus': 'harus', 'kudu': 'harus', 'musti': 'harus',
    'cb': 'coba', 'coba2': 'coba', 'nyoba': 'coba',
    'br': 'baru', 'bru': 'baru', 'barusan': 'baru',
    'blm': 'belum', 'blom': 'belum', 'belon': 'belum',
    'msh': 'masih', 'masi': 'masih', 'masih': 'masih',
    'sll': 'selalu', 'slalu': 'selalu', 'sellu': 'selalu',
    
    # Pronouns
    'sy': 'saya', 'sya': 'saya', 'aku': 'saya', 'ak': 'saya',
    'gw': 'saya', 'gwe': 'saya', 'gua': 'saya', 'gue': 'saya', 'ane': 'saya',
    'km': 'kamu', 'kmu': 'kamu', 'lu': 'kamu', 'lo': 'kamu', 'elu': 'kamu',
    'ente': 'kamu', 'loe': 'kamu',
    'kt': 'kita', 'qta': 'kita', 'kite': 'kita',
    'mrk': 'mereka', 'merka': 'mereka', 'mrka': 'mereka',
    'dy': 'dia', 'doi': 'dia', 'dya': 'dia',
    
    # Financial/App specific
    'app': 'aplikasi', 'apk': 'aplikasi', 'apps': 'aplikasi', 'apl': 'aplikasi',
    'pinjam': 'pinjam', 'pinjeman': 'pinjaman', 'pinjem': 'pinjam', 'pnjm': 'pinjam',
    'bayar': 'bayar', 'byr': 'bayar', 'byar': 'bayar', 'bayr': 'bayar',
    'lunas': 'lunas', 'lns': 'lunas', 'lunasi': 'lunas',
    'limit': 'limit', 'plafon': 'plafon',
    'cc': 'kartu kredit', 'creditcard': 'kartu kredit',
    'tf': 'transfer', 'trf': 'transfer',
    'wd': 'withdraw', 'tarik': 'withdraw',
    'topup': 'top up', 'top-up': 'top up',
    'tagihan': 'tagihan', 'tgihan': 'tagihan', 'bill': 'tagihan',
    'cicilan': 'cicilan', 'cicil': 'cicilan', 'angsur': 'cicilan',
    'bunga': 'bunga', 'bnga': 'bunga', 'interest': 'bunga',
    'denda': 'denda', 'pinalti': 'denda', 'penalty': 'denda',
    
    # Adjectives
    'bgus': 'bagus', 'bgs': 'bagus', 'baguss': 'bagus', 'mantap': 'bagus',
    'jelek': 'buruk', 'jlek': 'buruk', 'ancur': 'buruk', 'parah': 'buruk',
    'gampang': 'mudah', 'gmpang': 'mudah', 'ez': 'mudah',
    'susah': 'sulit', 'ssh': 'sulit', 'ribet': 'sulit', 'ruwet': 'sulit',
    'cpt': 'cepat', 'cepet': 'cepat', 'cpat': 'cepat',
    'lmbt': 'lambat', 'lemot': 'lambat', 'lama': 'lambat', 'lelet': 'lambat',
    'oke': 'baik', 'okay': 'baik', 'okey': 'baik', 'ok': 'baik',
    'sip': 'baik', 'siip': 'baik', 'mantul': 'baik', 'keren': 'baik',
    
    # Expressions to remove
    'hehe': '', 'haha': '', 'wkwk': '', 'xixi': '', 'hihi': '',
    'hmm': '', 'hmmm': '', 'huhu': '', 'huft': '',
    'wew': '', 'wow': '', 'eh': '', 'ah': '', 'oh': '',
}

def normalize_text(text):
    """Normalize Indonesian slang words"""
    if pd.isna(text) or text == "":
        return ""
    
    words = str(text).split()
    normalized = []
    
    for word in words:
        # Check slang dictionary
        normalized_word = SLANG_DICT.get(word.lower(), word)
        if normalized_word:  # Skip empty strings
            normalized.append(normalized_word)
    
    return ' '.join(normalized)

# Apply normalization
print("  Normalizing text...")
df['normalized_text'] = df['final_text'].apply(normalize_text)

# Count changes
changes = sum(1 for i in range(len(df)) 
              if str(df.iloc[i]['final_text']) != str(df.iloc[i]['normalized_text']))
print(f"✅ Normalisasi selesai! ({changes} reviews normalized)")

# Show examples
print("\n  Contoh normalisasi:")
print("  " + "-"*50)
count_examples = 0
for i in range(min(100, len(df))):
    if str(df.iloc[i]['final_text']) != str(df.iloc[i]['normalized_text']):
        print(f"  Before: {str(df.iloc[i]['final_text'])[:60]}...")
        print(f"  After:  {str(df.iloc[i]['normalized_text'])[:60]}...")
        print("  " + "-"*50)
        count_examples += 1
        if count_examples >= 2:
            break

# ============================================
# STEP 2: REMOVE DUPLIKAT
# ============================================
print("\n" + "="*70)
print("STEP 2: REMOVE DUPLIKAT")
print("="*70)

original_count = len(df)

# Remove exact duplicates
df_clean = df.drop_duplicates(subset=['content'], keep='first')
exact_dupes = original_count - len(df_clean)

# Remove normalized duplicates
df_clean = df_clean.drop_duplicates(subset=['normalized_text'], keep='first')
norm_dupes = original_count - exact_dupes - len(df_clean)

# Remove empty
df_clean = df_clean[df_clean['normalized_text'].str.strip() != '']
df_clean = df_clean.dropna(subset=['normalized_text'])

final_count = len(df_clean)

print(f"  Original reviews   : {original_count}")
print(f"  Exact duplicates   : {exact_dupes}")
print(f"  Similar duplicates : {norm_dupes}")
print(f"  Empty removed      : {original_count - exact_dupes - norm_dupes - final_count}")
print(f"  Final unique       : {final_count}")
print(f"✅ Remove duplikat selesai! ({original_count - final_count} removed)")

df = df_clean  # Use clean dataframe

# ============================================
# STEP 3: BI-GRAM ANALYSIS
# ============================================
print("\n" + "="*70)
print("STEP 3: BI-GRAM ANALYSIS")
print("="*70)

# Collect bigrams
bigrams = []
for text in df['normalized_text']:
    if pd.notna(text) and text:
        words = str(text).split()
        for i in range(len(words)-1):
            bigrams.append(f"{words[i]} {words[i+1]}")

# Count and get top bigrams
bigram_freq = Counter(bigrams)
top_bigrams = bigram_freq.most_common(30)

print("\n  Top 15 Bi-grams:")
print("  " + "-"*50)
for i, (bigram, freq) in enumerate(top_bigrams[:15], 1):
    bar = "█" * min(30, int(freq/5))
    print(f"  {i:2d}. {bigram:30s} : {freq:4d} {bar}")

# Visualize
plt.figure(figsize=(12, 7))
bg_words, bg_counts = zip(*top_bigrams[:15])
colors = plt.cm.viridis([i/15 for i in range(15)])
bars = plt.barh(range(len(bg_words)), bg_counts, color=colors)

plt.yticks(range(len(bg_words)), bg_words, fontsize=10)
plt.xlabel('Frequency', fontsize=11, fontweight='bold')
plt.title('Top 15 Bi-grams dalam Review Kredivo', fontsize=13, fontweight='bold')

# Add value labels
for bar, count in zip(bars, bg_counts):
    plt.text(count + 0.5, bar.get_y() + bar.get_height()/2, 
             str(count), va='center', fontsize=9)

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('bigram_analysis.png', dpi=200, bbox_inches='tight')
plt.close()
print("\n💾 Saved: bigram_analysis.png")

# ============================================
# STEP 4: TRI-GRAM ANALYSIS
# ============================================
print("\n" + "="*70)
print("STEP 4: TRI-GRAM ANALYSIS")
print("="*70)

# Collect trigrams
trigrams = []
for text in df['normalized_text']:
    if pd.notna(text) and text:
        words = str(text).split()
        for i in range(len(words)-2):
            trigrams.append(f"{words[i]} {words[i+1]} {words[i+2]}")

# Count and get top trigrams
trigram_freq = Counter(trigrams)
top_trigrams = trigram_freq.most_common(30)

print("\n  Top 15 Tri-grams:")
print("  " + "-"*50)
for i, (trigram, freq) in enumerate(top_trigrams[:15], 1):
    bar = "█" * min(30, int(freq/5))
    print(f"  {i:2d}. {trigram:40s} : {freq:4d} {bar}")

# Visualize
plt.figure(figsize=(12, 7))
tg_words, tg_counts = zip(*top_trigrams[:15])
colors = plt.cm.plasma([i/15 for i in range(15)])
bars = plt.barh(range(len(tg_words)), tg_counts, color=colors)

plt.yticks(range(len(tg_words)), tg_words, fontsize=10)
plt.xlabel('Frequency', fontsize=11, fontweight='bold')
plt.title('Top 15 Tri-grams dalam Review Kredivo', fontsize=13, fontweight='bold')

# Add value labels
for bar, count in zip(bars, tg_counts):
    plt.text(count + 0.5, bar.get_y() + bar.get_height()/2,
             str(count), va='center', fontsize=9)

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('trigram_analysis.png', dpi=200, bbox_inches='tight')
plt.close()
print("\n💾 Saved: trigram_analysis.png")

# ============================================
# STEP 5: WORDCLOUD GENERATION
# ============================================
print("\n" + "="*70)
print("STEP 5: WORDCLOUD GENERATION")
print("="*70)

# Prepare text
all_text = ' '.join(df['normalized_text'].dropna())

if not all_text.strip():
    print("⚠️ No text for wordcloud!")
else:
    # Main wordcloud
    print("  Generating wordclouds...")
    wc_main = WordCloud(
        width=1600, height=800,
        background_color='white',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5,
        min_font_size=10
    ).generate(all_text)
    
    # Create 4-panel figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Overall
    axes[0,0].imshow(wc_main, interpolation='bilinear')
    axes[0,0].set_title('WordCloud Keseluruhan', fontsize=14, fontweight='bold')
    axes[0,0].axis('off')
    
    # Positive (rating 4-5)
    positive_df = df[df['score'] >= 4]
    positive_text = ' '.join(positive_df['normalized_text'].dropna())
    if positive_text:
        wc_pos = WordCloud(width=800, height=600, background_color='white',
                          colormap='Greens', max_words=50).generate(positive_text)
        axes[0,1].imshow(wc_pos, interpolation='bilinear')
    axes[0,1].set_title(f'Positive Reviews (Rating 4-5)\n{len(positive_df)} reviews', 
                       fontsize=14, fontweight='bold')
    axes[0,1].axis('off')
    
    # Negative (rating 1-2)
    negative_df = df[df['score'] <= 2]
    negative_text = ' '.join(negative_df['normalized_text'].dropna())
    if negative_text:
        wc_neg = WordCloud(width=800, height=600, background_color='white',
                          colormap='Reds', max_words=50).generate(negative_text)
        axes[1,0].imshow(wc_neg, interpolation='bilinear')
    axes[1,0].set_title(f'Negative Reviews (Rating 1-2)\n{len(negative_df)} reviews',
                       fontsize=14, fontweight='bold')
    axes[1,0].axis('off')
    
    # Neutral (rating 3)
    neutral_df = df[df['score'] == 3]
    neutral_text = ' '.join(neutral_df['normalized_text'].dropna())
    if neutral_text:
        wc_neu = WordCloud(width=800, height=600, background_color='white',
                          colormap='Blues', max_words=50).generate(neutral_text)
        axes[1,1].imshow(wc_neu, interpolation='bilinear')
    axes[1,1].set_title(f'Neutral Reviews (Rating 3)\n{len(neutral_df)} reviews',
                       fontsize=14, fontweight='bold')
    axes[1,1].axis('off')
    
    plt.suptitle('WordCloud Analysis - Kredivo Reviews', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('wordcloud_analysis.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("💾 Saved: wordcloud_analysis.png")

# ============================================
# STEP 6: CREATE FOLDER STRUCTURE
# ============================================
print("\n" + "="*70)
print("STEP 6: MEMBUAT STRUKTUR FOLDER CPMK 2")
print("="*70)

# Create folders
folders = ['CPMK 2', 'CPMK 2/data', 'CPMK 2/visualizations', 'CPMK 2/scripts']
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"📁 Created/Verified: {folder}")

# Save final data with normalization
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'CPMK 2/data/kredivo_final_normalized_{timestamp}.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n💾 Final data saved: {output_file}")

# Copy/Move files
import shutil
import glob

# Move visualizations
vis_files = ['bigram_analysis.png', 'trigram_analysis.png', 'wordcloud_analysis.png']
for file in vis_files:
    if os.path.exists(file):
        dest = f'CPMK 2/visualizations/{file}'
        shutil.move(file, dest)
        print(f"  Moved: {file} → visualizations/")

# Copy original preprocessed file
if os.path.exists(filename):
    shutil.copy2(filename, f'CPMK 2/data/{filename}')
    print(f"  Copied: {filename} → data/")

# Copy Python scripts
py_files = glob.glob('*.py')
for file in py_files:
    dest = f'CPMK 2/scripts/{os.path.basename(file)}'
    if os.path.exists(file) and not os.path.exists(dest):
        shutil.copy2(file, dest)
        print(f"  Copied: {file} → scripts/")

# ============================================
# FINAL REPORT & SUMMARY
# ============================================
print("\n" + "="*70)
print("                 ✨ SEMUA TUGAS SELESAI! ✨")
print("="*70)

print("\n📋 CHECKLIST TUGAS CPMK 2:")
print("  ✅ 1. Scraping (sudah ada)")
print("  ✅ 2. Preprocessing (sudah ada)")
print("  ✅ 3. Normalisasi Kata")
print("  ✅ 4. Remove Duplikat")
print("  ✅ 5. Bi-gram Analysis")
print("  ✅ 6. Tri-gram Analysis")
print("  ✅ 7. WordCloud Generation")

print("\n📊 STATISTIK AKHIR:")
print(f"  • Total unique reviews : {len(df)}")
print(f"  • Rata-rata rating    : {df['score'].mean():.2f}/5.0")
print(f"  • Positive (4-5★)     : {len(df[df['score'] >= 4])} reviews")
print(f"  • Negative (1-2★)     : {len(df[df['score'] <= 2])} reviews")
print(f"  • Neutral (3★)        : {len(df[df['score'] == 3])} reviews")

if top_bigrams:
    print(f"\n  • Top bi-gram  : '{top_bigrams[0][0]}' ({top_bigrams[0][1]} times)")
if top_trigrams:
    print(f"  • Top tri-gram : '{top_trigrams[0][0]}' ({top_trigrams[0][1]} times)")

print("\n📁 FOLDER STRUKTUR:")
print("  CPMK 2/")
print("  ├── data/")
print("  │   ├── kredivo_preprocessed_20251011_172307.csv")
print("  │   └── kredivo_final_normalized_*.csv")
print("  ├── visualizations/")
print("  │   ├── bigram_analysis.png")
print("  │   ├── trigram_analysis.png")
print("  │   └── wordcloud_analysis.png")
print("  └── scripts/")
print("      └── [Python files]")

print("\n🎯 READY TO SUBMIT!")
print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n📦 Upload folder 'CPMK 2' ke GitHub/platform pengumpulan")
print("="*70)