"""
Collatz Cipher - Collatz PRNG Tabanlı Şifreleme Modülü
Bilgi Sistemleri Güvenliği - Ödev Projesi

Bu modül Collatz PRNG'yi kullanarak stream cipher (akış şifresi) uygular.
Şifreleme: plaintext XOR keystream
Çözme: ciphertext XOR keystream (aynı seed ile)
"""

from collatz_prng import CollatzPRNG


class CollatzCipher:
    """
    Collatz PRNG tabanlı simetrik şifreleme sınıfı.

    Şifreleme yöntemi: XOR Stream Cipher
    - Aynı anahtar (seed) şifreleme ve çözme için kullanılır
    - Her byte, Collatz PRNG'den üretilen byte ile XOR'lanır
    """

    def __init__(self, key):
        """
        Args:
            key: Şifreleme anahtarı (pozitif tam sayı, seed olarak kullanılır)
        """
        if key <= 1:
            raise ValueError("Anahtar 1'den büyük pozitif tam sayı olmalı!")
        self.key = key

    def _get_prng(self):
        """Yeni bir PRNG instance'ı oluşturur."""
        return CollatzPRNG(self.key)

    def encrypt_bytes(self, plaintext):
        """
        Byte dizisini şifreler.

        Args:
            plaintext: Şifrelenecek byte dizisi

        Returns:
            Şifreli byte dizisi
        """
        prng = self._get_prng()
        ciphertext = bytearray()

        for byte in plaintext:
            key_byte = prng.next_byte()
            encrypted_byte = byte ^ key_byte
            ciphertext.append(encrypted_byte)

        return bytes(ciphertext)

    def decrypt_bytes(self, ciphertext):
        """
        Şifreli byte dizisini çözer.

        Args:
            ciphertext: Çözülecek şifreli byte dizisi

        Returns:
            Çözülmüş byte dizisi
        """
        # XOR şifreleme simetrik olduğu için aynı işlem
        return self.encrypt_bytes(ciphertext)

    def encrypt_text(self, plaintext):
        """
        Metin şifreler.

        Args:
            plaintext: Şifrelenecek metin (string)

        Returns:
            Şifreli metin (hex formatında string)
        """
        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext_bytes = self.encrypt_bytes(plaintext_bytes)
        return ciphertext_bytes.hex()

    def decrypt_text(self, ciphertext_hex):
        """
        Şifreli metni çözer.

        Args:
            ciphertext_hex: Hex formatında şifreli metin

        Returns:
            Çözülmüş metin (string)
        """
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        plaintext_bytes = self.decrypt_bytes(ciphertext_bytes)
        return plaintext_bytes.decode('utf-8')

    def encrypt_file(self, input_path, output_path):
        """
        Dosya şifreler.

        Args:
            input_path: Girdi dosyası yolu
            output_path: Çıktı dosyası yolu
        """
        with open(input_path, 'rb') as f:
            plaintext = f.read()

        ciphertext = self.encrypt_bytes(plaintext)

        with open(output_path, 'wb') as f:
            f.write(ciphertext)

        print(f"Dosya şifrelendi: {input_path} -> {output_path}")

    def decrypt_file(self, input_path, output_path):
        """
        Şifreli dosyayı çözer.

        Args:
            input_path: Şifreli dosya yolu
            output_path: Çıktı dosyası yolu
        """
        # XOR simetrik olduğu için aynı işlem
        self.encrypt_file(input_path, output_path)
        print(f"Dosya çözüldü: {input_path} -> {output_path}")


def visualize_encryption(plaintext, key):
    """
    Şifreleme sürecini adım adım gösterir.

    Args:
        plaintext: Şifrelenecek metin
        key: Şifreleme anahtarı
    """
    cipher = CollatzCipher(key)
    prng = CollatzPRNG(key)

    print(f"\nAnahtar (Seed): {key}")
    print(f"Düz Metin: {plaintext}")
    print("-" * 60)
    print(f"{'Karakter':<10} {'ASCII':<8} {'KeyByte':<10} {'XOR':<10} {'Şifreli':<10}")
    print("-" * 60)

    ciphertext_bytes = []
    for char in plaintext:
        ascii_val = ord(char)
        key_byte = prng.next_byte()
        encrypted = ascii_val ^ key_byte
        ciphertext_bytes.append(encrypted)

        print(f"{char:<10} {ascii_val:<8} {key_byte:<10} {ascii_val} ^ {key_byte} = {encrypted:<10}")

    print("-" * 60)
    ciphertext_hex = bytes(ciphertext_bytes).hex()
    print(f"Şifreli (Hex): {ciphertext_hex}")

    return ciphertext_hex


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("Collatz Cipher Demo")
    print("=" * 60)

    # Örnek 1: Metin şifreleme
    key = 2024
    plaintext = "Merhaba Dunya!"

    cipher = CollatzCipher(key)

    print(f"\n[1] Metin Şifreleme")
    print(f"Anahtar: {key}")
    print(f"Düz metin: {plaintext}")

    encrypted = cipher.encrypt_text(plaintext)
    print(f"Şifreli (hex): {encrypted}")

    decrypted = cipher.decrypt_text(encrypted)
    print(f"Çözülmüş: {decrypted}")

    # Örnek 2: Adım adım görselleştirme
    print("\n" + "=" * 60)
    print("[2] Şifreleme Adımları")
    print("=" * 60)

    visualize_encryption("HELLO", 27)

    # Örnek 3: Farklı anahtarlar
    print("\n" + "=" * 60)
    print("[3] Farklı Anahtarlarla Şifreleme")
    print("=" * 60)

    message = "Gizli Mesaj"
    for k in [7, 42, 123, 2024]:
        c = CollatzCipher(k)
        enc = c.encrypt_text(message)
        print(f"Anahtar {k:4d}: {enc}")

    # Örnek 4: Aynı anahtar = Aynı sonuç (Deterministik)
    print("\n" + "=" * 60)
    print("[4] Deterministik Özellik")
    print("=" * 60)

    c1 = CollatzCipher(999)
    c2 = CollatzCipher(999)

    enc1 = c1.encrypt_text("Test")
    enc2 = c2.encrypt_text("Test")

    print(f"Şifreleme 1: {enc1}")
    print(f"Şifreleme 2: {enc2}")
    print(f"Aynı mı? {enc1 == enc2}")
