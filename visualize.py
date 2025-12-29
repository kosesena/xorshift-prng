"""
Collatz Cipher - Görselleştirme Modülü
Bilgi Sistemleri Güvenliği - Ödev Projesi

Bu modül Collatz PRNG için çeşitli grafikler oluşturur.
"""

import matplotlib.pyplot as plt
from collatz_prng import CollatzPRNG, collatz_sequence


def plot_collatz_sequence(seed, max_steps=50, save_path=None):
    """
    Collatz dizisini grafik olarak çizer.

    Args:
        seed: Başlangıç değeri
        max_steps: Maksimum adım sayısı
        save_path: Kayıt yolu (None ise gösterir)
    """
    sequence = collatz_sequence(seed, max_steps)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(sequence, 'b-o', markersize=4, linewidth=1)
    ax.set_xlabel('Adım', fontsize=12)
    ax.set_ylabel('Değer', fontsize=12)
    ax.set_title(f'Collatz Dizisi (Seed: {seed})', fontsize=14)
    ax.grid(True, alpha=0.3)

    # Çift/tek noktaları renklendir
    for i, val in enumerate(sequence):
        color = 'green' if val % 2 == 0 else 'red'
        ax.scatter(i, val, c=color, s=30, zorder=5)

    ax.legend(['Dizi', 'Çift (0)', 'Tek (1)'], loc='upper right')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_bit_distribution(seed, num_bits=1000, save_path=None):
    """
    Üretilen bitlerin dağılımını gösterir.

    Args:
        seed: PRNG seed değeri
        num_bits: Üretilecek bit sayısı
        save_path: Kayıt yolu
    """
    prng = CollatzPRNG(seed)
    bits = prng.generate_bits(num_bits)

    zeros = bits.count(0)
    ones = bits.count(1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Bar chart
    bars = ax1.bar(['0', '1'], [zeros, ones], color=['#3498db', '#e74c3c'])
    ax1.set_xlabel('Bit Değeri', fontsize=12)
    ax1.set_ylabel('Frekans', fontsize=12)
    ax1.set_title(f'Bit Dağılımı (n={num_bits})', fontsize=14)

    # Yüzdeleri göster
    for bar, val in zip(bars, [zeros, ones]):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val} (%{100*val/num_bits:.1f})',
                ha='center', va='bottom', fontsize=11)

    # Pie chart
    ax2.pie([zeros, ones], labels=['0', '1'], autopct='%1.1f%%',
            colors=['#3498db', '#e74c3c'], startangle=90)
    ax2.set_title(f'Bit Oranları (Seed: {seed})', fontsize=14)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_histogram(seed, num_bytes=10000, save_path=None):
    """
    Üretilen byte'ların histogramını çizer.

    Args:
        seed: PRNG seed değeri
        num_bytes: Üretilecek byte sayısı
        save_path: Kayıt yolu
    """
    prng = CollatzPRNG(seed)
    bytes_data = list(prng.generate_bytes(num_bytes))

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.hist(bytes_data, bins=64, color='#9b59b6', edgecolor='white', alpha=0.8)
    ax.set_xlabel('Byte Değeri (0-255)', fontsize=12)
    ax.set_ylabel('Frekans', fontsize=12)
    ax.set_title(f'Byte Dağılımı Histogramı (n={num_bytes}, Seed: {seed})', fontsize=14)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_scatter_2d(seed, num_points=5000, save_path=None):
    """
    Ardışık byte çiftlerini 2D scatter plot olarak çizer.

    Args:
        seed: PRNG seed değeri
        num_points: Nokta sayısı
        save_path: Kayıt yolu
    """
    prng = CollatzPRNG(seed)
    bytes_data = list(prng.generate_bytes(num_points + 1))

    x = bytes_data[:-1]
    y = bytes_data[1:]

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.scatter(x, y, c='#2ecc71', alpha=0.3, s=1)
    ax.set_xlabel('Byte n', fontsize=12)
    ax.set_ylabel('Byte n+1', fontsize=12)
    ax.set_title(f'Ardışık Byte Korelasyonu (Seed: {seed})', fontsize=14)
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_encryption_process(plaintext, key, save_path=None):
    """
    Şifreleme sürecini görselleştirir.

    Args:
        plaintext: Şifrelenecek metin
        key: Şifreleme anahtarı
        save_path: Kayıt yolu
    """
    prng = CollatzPRNG(key)

    plain_bytes = [ord(c) for c in plaintext]
    key_bytes = [prng.next_byte() for _ in plaintext]
    cipher_bytes = [p ^ k for p, k in zip(plain_bytes, key_bytes)]

    x = range(len(plaintext))

    fig, ax = plt.subplots(figsize=(12, 6))

    width = 0.25
    ax.bar([i - width for i in x], plain_bytes, width, label='Düz Metin (ASCII)', color='#3498db')
    ax.bar([i for i in x], key_bytes, width, label='Anahtar Byte', color='#e74c3c')
    ax.bar([i + width for i in x], cipher_bytes, width, label='Şifreli (XOR)', color='#2ecc71')

    ax.set_xlabel('Karakter İndeksi', fontsize=12)
    ax.set_ylabel('Byte Değeri', fontsize=12)
    ax.set_title(f'Şifreleme Süreci: "{plaintext}" (Anahtar: {key})', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(list(plaintext))
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_all(seed=27, output_dir="output"):
    """
    Tüm grafikleri oluşturur ve kaydeder.

    Args:
        seed: PRNG seed değeri
        output_dir: Çıktı klasörü
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    print("  Collatz dizisi grafiği...")
    plot_collatz_sequence(seed, save_path=f"{output_dir}/collatz_sequence.png")

    print("  Bit dağılımı grafiği...")
    plot_bit_distribution(seed, save_path=f"{output_dir}/bit_distribution.png")

    print("  Histogram grafiği...")
    plot_histogram(seed, save_path=f"{output_dir}/histogram.png")

    print("  2D Scatter grafiği...")
    plot_scatter_2d(seed, save_path=f"{output_dir}/scatter2d.png")

    print("  Şifreleme süreci grafiği...")
    plot_encryption_process("COLLATZ", seed, save_path=f"{output_dir}/encryption_process.png")

    print("  Tüm grafikler oluşturuldu!")


if __name__ == "__main__":
    plot_all(seed=27)
