"""
Collatz Cipher - Ana Çalıştırma Dosyası
Bilgi Sistemleri Güvenliği - Ödev Projesi

Bu dosya projenin tüm özelliklerini demonstre eder:
1. Collatz PRNG ile rastgele sayı üretimi
2. Collatz Cipher ile metin şifreleme/çözme
3. Görselleştirmeler
"""

from collatz_prng import CollatzPRNG, collatz_sequence
from cipher import CollatzCipher, visualize_encryption
from visualize import (
    plot_collatz_sequence,
    plot_bit_distribution,
    plot_histogram,
    plot_all
)


def demo_collatz_sequence():
    """Collatz dizisini gösterir."""
    print("\n" + "=" * 60)
    print("1. COLLATZ DİZİSİ")
    print("=" * 60)

    seeds = [7, 27, 97]
    for seed in seeds:
        seq = collatz_sequence(seed, max_steps=30)
        print(f"\nSeed {seed}:")
        print(f"  Dizi: {seq}")
        print(f"  Uzunluk: {len(seq)} adımda 1'e ulaştı")


def demo_prng():
    """PRNG özelliklerini gösterir."""
    print("\n" + "=" * 60)
    print("2. COLLATZ PRNG")
    print("=" * 60)

    seed = 27
    prng = CollatzPRNG(seed)

    print(f"\nSeed: {seed}")

    # Collatz adımları ve bitler
    numbers, bits = prng.get_collatz_sequence(20)
    print(f"\nCollatz Adımları:")
    print(f"  Sayılar: {numbers[:10]}...")
    print(f"  Bitler:  {bits[:10]}...")

    # Bit dizisi
    prng.reset()
    bit_string = ''.join(map(str, prng.generate_bits(32)))
    print(f"\n32-bit üretim: {bit_string}")

    # Byte'lar
    prng.reset()
    bytes_list = list(prng.generate_bytes(8))
    print(f"8 byte üretim: {bytes_list}")

    # Farklı seed'ler
    print(f"\nFarklı seed değerleri (16-bit):")
    for s in [7, 27, 97, 123]:
        p = CollatzPRNG(s)
        bits = ''.join(map(str, p.generate_bits(16)))
        print(f"  Seed {s:3d}: {bits}")


def demo_cipher():
    """Şifreleme özelliklerini gösterir."""
    print("\n" + "=" * 60)
    print("3. COLLATZ CIPHER (ŞİFRELEME)")
    print("=" * 60)

    key = 2024
    plaintext = "Bilgi Sistemleri Guvenligi"

    cipher = CollatzCipher(key)

    print(f"\nAnahtar: {key}")
    print(f"Düz Metin: {plaintext}")

    # Şifreleme
    encrypted = cipher.encrypt_text(plaintext)
    print(f"Şifreli (Hex): {encrypted}")

    # Çözme
    decrypted = cipher.decrypt_text(encrypted)
    print(f"Çözülmüş: {decrypted}")

    # Doğrulama
    print(f"\nDoğrulama: {plaintext == decrypted}")


def demo_step_by_step():
    """Şifrelemeyi adım adım gösterir."""
    print("\n" + "=" * 60)
    print("4. ADIM ADIM ŞİFRELEME")
    print("=" * 60)

    visualize_encryption("SENA", 27)


def demo_security():
    """Güvenlik özelliklerini gösterir."""
    print("\n" + "=" * 60)
    print("5. GÜVENLİK ÖZELLİKLERİ")
    print("=" * 60)

    message = "Gizli"

    # Farklı anahtarlar = Farklı şifreli metinler
    print("\nAynı mesaj, farklı anahtarlar:")
    for key in [100, 200, 300]:
        c = CollatzCipher(key)
        enc = c.encrypt_text(message)
        print(f"  Anahtar {key}: {enc}")

    # Yanlış anahtar ile çözme
    print("\nYanlış anahtar ile çözme denemesi:")
    correct_key = 2024
    wrong_key = 1234

    cipher1 = CollatzCipher(correct_key)
    encrypted = cipher1.encrypt_text("Dogru Mesaj")
    print(f"  Şifreli: {encrypted}")

    cipher2 = CollatzCipher(wrong_key)
    try:
        wrong_decrypt = cipher2.decrypt_text(encrypted)
        print(f"  Yanlış anahtar ({wrong_key}) ile: {wrong_decrypt}")
    except:
        print(f"  Yanlış anahtar ile çözülemedi!")

    cipher3 = CollatzCipher(correct_key)
    correct_decrypt = cipher3.decrypt_text(encrypted)
    print(f"  Doğru anahtar ({correct_key}) ile: {correct_decrypt}")


def main():
    """Ana fonksiyon."""
    print("=" * 60)
    print("   COLLATZ CIPHER")
    print("   Collatz Varsayımı Tabanlı Şifreleme Sistemi")
    print("   Bilgi Sistemleri Güvenliği - 2025")
    print("=" * 60)

    # Demo'ları çalıştır
    demo_collatz_sequence()
    demo_prng()
    demo_cipher()
    demo_step_by_step()
    demo_security()

    # Grafikleri oluştur
    print("\n" + "=" * 60)
    print("6. GRAFİKLER OLUŞTURULUYOR...")
    print("=" * 60)

    try:
        plot_all(seed=27, output_dir="output")
        print("\nGrafikler 'output/' klasörüne kaydedildi.")
    except Exception as e:
        print(f"Grafik oluşturma hatası: {e}")

    print("\n" + "=" * 60)
    print("Demo tamamlandı!")
    print("=" * 60)


if __name__ == "__main__":
    main()
