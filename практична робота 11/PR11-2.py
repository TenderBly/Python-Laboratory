import nltk
from nltk.corpus import gutenberg
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
import string

# Завантаження необхідних ресурсів NLTK
print("Завантаження ресурсів NLTK...")
nltk.download('gutenberg', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Завантаження тексту "Alice in Wonderland"
print("\nЗавантаження тексту 'Alice in Wonderland'...")
alice_text = gutenberg.words('carroll-alice.txt')

# 1. Визначення кількості слів у тексті
total_words = len(alice_text)
print(f"\n1. Загальна кількість слів у тексті: {total_words}")

# 2. Визначення 10 найбільш вживаних слів (без обробки)
print("\n2. 10 найбільш вживаних слів (без обробки):")
word_freq = Counter(alice_text)
top_10_raw = word_freq.most_common(10)

for word, freq in top_10_raw:
    print(f"   '{word}': {freq}")

# Побудова діаграми для необроблених даних
words_raw = [word for word, freq in top_10_raw]
freqs_raw = [freq for word, freq in top_10_raw]

plt.figure(figsize=(12, 6))
plt.bar(words_raw, freqs_raw, color='skyblue', edgecolor='navy')
plt.xlabel('Слова', fontsize=12)
plt.ylabel('Частота', fontsize=12)
plt.title('10 найбільш вживаних слів (без обробки)', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_10_raw_words.png', dpi=300, bbox_inches='tight')
print("\n   Діаграму збережено як 'top_10_raw_words.png'")
plt.show()

# 3. Видалення стоп-слів та пунктуації
print("\n3. Обробка тексту (видалення стоп-слів та пунктуації)...")

# Отримання стоп-слів англійської мови
stop_words = set(stopwords.words('english'))

# Фільтрація: видалення пунктуації та стоп-слів, приведення до нижнього регістру
filtered_words = [
    word.lower() for word in alice_text 
    if word.isalpha() and word.lower() not in stop_words
]

print(f"   Кількість слів після обробки: {len(filtered_words)}")

# 4. Визначення 10 найбільш вживаних слів після обробки
print("\n4. 10 найбільш вживаних слів (після обробки):")
filtered_freq = Counter(filtered_words)
top_10_filtered = filtered_freq.most_common(10)

for word, freq in top_10_filtered:
    print(f"   '{word}': {freq}")

# Побудова діаграми для оброблених даних
words_filtered = [word for word, freq in top_10_filtered]
freqs_filtered = [freq for word, freq in top_10_filtered]

plt.figure(figsize=(12, 6))
plt.bar(words_filtered, freqs_filtered, color='lightcoral', edgecolor='darkred')
plt.xlabel('Слова', fontsize=12)
plt.ylabel('Частота', fontsize=12)
plt.title('10 найбільш вживаних слів (після видалення стоп-слів та пунктуації)', 
          fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_10_filtered_words.png', dpi=300, bbox_inches='tight')
print("\n   Діаграму збережено як 'top_10_filtered_words.png'")
plt.show()

# Додаткова статистика
print("\n" + "="*60)
print("ПІДСУМКОВА СТАТИСТИКА:")
print("="*60)
print(f"Загальна кількість слів: {total_words}")
print(f"Кількість унікальних слів (до обробки): {len(word_freq)}")
print(f"Кількість слів після обробки: {len(filtered_words)}")
print(f"Кількість унікальних слів (після обробки): {len(filtered_freq)}")
print(f"Видалено слів: {total_words - len(filtered_words)}")
print("="*60)