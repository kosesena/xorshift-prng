"""
Collatz PRNG - Collatz Varsayımına Dayalı Sözde Rastgele Sayı Üreteci
Bilgi Sistemleri Güvenliği - Ödev Projesi

Collatz Varsayımı (3n+1 Problemi):
- n çift ise: n / 2
- n tek ise: 3n + 1
Her pozitif tam sayı sonunda 1'e ulaşır (varsayım).
"""


class CollatzPRNG:
    """
    Collatz varsayımını kullanarak rastgele bit dizisi üreten sınıf.

    Çalışma prensibi:
    - Çift sayı -> 0 biti üret
    - Tek sayı -> 1 biti üret
    """

    def __init__(self, seed):
        """
        Args:
            seed: Başlangıç değeri (pozitif tam sayı, 1'den büyük olmalı)
        """
        if seed <= 1:
            raise ValueError("Seed 1'den büyük pozitif tam sayı olmalı!")
        self.seed = seed
        self.current = seed
        self.step_count = 0

    def _collatz_step(self, n):
        """Tek bir Collatz adımı uygular."""
        if n % 2 == 0:
            return n // 2
        else:
            return 3 * n + 1

    def next_bit(self):
        """
        Bir sonraki rastgele biti üretir.

        Returns:
            0 veya 1
        """
        # Eğer 1'e ulaştıysak, seed'i yeniden başlat (döngüyü kır)
        if self.current <= 1:
            self.current = self.seed + self.step_count

        # Mevcut sayıya göre bit üret
        bit = self.current % 2  # Tek ise 1, çift ise 0

        # Collatz adımını uygula
        self.current = self._collatz_step(self.current)
        self.step_count += 1

        return bit

    def next_byte(self):
        """
        8 bit üretip bir byte döndürür.

        Returns:
            0-255 arası tam sayı
        """
        byte = 0
        for i in range(8):
            byte = (byte << 1) | self.next_bit()
        return byte

    def next_int(self, bits=32):
        """
        Belirtilen bit sayısında rastgele tam sayı üretir.

        Args:
            bits: Üretilecek bit sayısı (varsayılan 32)

        Returns:
            Rastgele tam sayı
        """
        result = 0
        for i in range(bits):
            result = (result << 1) | self.next_bit()
        return result

    def generate_bits(self, count):
        """
        Belirtilen sayıda bit üretir.

        Args:
            count: Üretilecek bit sayısı

        Returns:
            Bit listesi [0, 1, 1, 0, ...]
        """
        return [self.next_bit() for _ in range(count)]

    def generate_bytes(self, count):
        """
        Belirtilen sayıda byte üretir.

        Args:
            count: Üretilecek byte sayısı

        Returns:
            Byte listesi
        """
        return bytes([self.next_byte() for _ in range(count)])

    def reset(self):
        """PRNG'yi başlangıç durumuna sıfırlar."""
        self.current = self.seed
        self.step_count = 0

    def get_collatz_sequence(self, length=20):
        """
        Collatz dizisini döndürür (görselleştirme için).

        Args:
            length: Dizi uzunluğu

        Returns:
            (sayılar, bitler) tuple'ı
        """
        self.reset()
        numbers = []
        bits = []

        for _ in range(length):
            numbers.append(self.current)
            bits.append(self.current % 2)

            if self.current <= 1:
                self.current = self.seed + len(numbers)
            self.current = self._collatz_step(self.current)

        self.reset()
        return numbers, bits


def collatz_sequence(n, max_steps=100):
    """
    Bir sayının Collatz dizisini döndürür.

    Args:
        n: Başlangıç sayısı
        max_steps: Maksimum adım sayısı

    Returns:
        Collatz dizisi listesi
    """
    sequence = [n]
    while n != 1 and len(sequence) < max_steps:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("Collatz PRNG Demo")
    print("=" * 60)

    seed = 27  # Örnek seed
    prng = CollatzPRNG(seed)

    print(f"\nSeed: {seed}")
    print(f"Collatz dizisi: {collatz_sequence(seed, 15)}")

    # Collatz adımlarını ve üretilen bitleri göster
    numbers, bits = prng.get_collatz_sequence(20)
    print(f"\nİlk 20 adım:")
    print(f"Sayılar: {numbers}")
    print(f"Bitler:  {bits}")
    print(f"Bit dizisi: {''.join(map(str, bits))}")

    # Rastgele sayılar üret
    prng.reset()
    print(f"\nÜretilen 5 byte: {list(prng.generate_bytes(5))}")

    prng.reset()
    print(f"Üretilen 32-bit sayı: {prng.next_int(32)}")

    # Farklı seed'ler
    print("\n" + "=" * 60)
    print("Farklı Seed Değerleri")
    print("=" * 60)

    for s in [7, 27, 97, 123]:
        p = CollatzPRNG(s)
        bits = p.generate_bits(16)
        print(f"Seed {s:3d}: {''.join(map(str, bits))}")
