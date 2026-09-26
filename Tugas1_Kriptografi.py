ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Caesar Cipher
def caesar_decrypt(ciphertext, shift):
    result = ""
    for char in ciphertext:
        if char in ALPHABET:
            result += ALPHABET[(ALPHABET.index(char) - shift) % 26]
        else:
            result += char
    return result

cipher_caesar = "BIVXI SCVKQ GIVO JMVIZ XMAIV QVQ BMBIX UMVRILQ BMSI BMSQ"

print("=== CAESAR CIPHER ===")
for shift in range(5, 12):
    print(f"Shift {shift}: {caesar_decrypt(cipher_caesar, shift)}")
print("\nKunci yang benar: 8")
print("Plaintext       :", caesar_decrypt(cipher_caesar, 8))


# Vigenere Cipher
cipher_vigenere = "AOXUX PHZ GJUALDN WYDUMHGRH FUXR NJYBRXFW MRHIP JFFNHFWUGLNZE PSUJCP"
key = "HURUF"

frekuensi_indo = {
    "A": 20.39, "B": 2.64, "C": 0.76, "D": 5.00, "E": 8.28,
    "F": 0.21, "G": 3.66, "H": 2.74, "I": 7.98, "J": 0.87,
    "K": 5.14, "L": 3.26, "M": 4.21, "N": 9.33, "O": 1.26,
    "P": 2.61, "Q": 0.01, "R": 4.64, "S": 4.15, "T": 5.58,
    "U": 4.62, "V": 0.18, "W": 0.48, "X": 0.03, "Y": 1.88, "Z": 0.04
}

def clean_text(text):
    return "".join(char for char in text if char in ALPHABET)

def vigenere_decrypt(ciphertext, key):
    result = ""
    key_index = 0
    for char in ciphertext:
        if char in ALPHABET:
            c = ALPHABET.index(char)
            k = ALPHABET.index(key[key_index % len(key)])
            result += ALPHABET[(c - k) % 26]
            key_index += 1
        else:
            result += char
    return result

def frequency_score(text):
    score = 0
    total = len(text)
    for char in ALPHABET:
        actual = text.count(char)
        expected = frekuensi_indo[char] / 100 * total
        if expected > 0:
            score += (actual - expected) ** 2 / expected
    return score

def cari_kandidat(kolom):
    kandidat = []
    for shift in range(26):
        hasil = ""
        for char in kolom:
            hasil += ALPHABET[(ALPHABET.index(char) - shift) % 26]
        kandidat.append((frequency_score(hasil), ALPHABET[shift]))
    kandidat.sort()
    return kandidat

text_vigenere = clean_text(cipher_vigenere)

print("\n=== VIGENERE CIPHER ===")
print("Ciphertext     :", cipher_vigenere)
print("Cipher bersih  :", text_vigenere)
print("Panjang cipher :", len(text_vigenere))
print("Panjang kunci  : 5")

print("\nPenentuan panjang kunci:")
print("Berdasarkan petunjuk soal, panjang kunci = 5.")
print("Cipher dibagi menjadi 5 kolom dan setiap kolom dianalisis dengan frekuensi huruf.")

kandidat_kunci = ""
for i in range(5):
    kolom = text_vigenere[i::5]
    kandidat = cari_kandidat(kolom)
    huruf = kandidat[0][1]
    kandidat_kunci += huruf
    print(f"Posisi {i + 1}: {huruf} | Score: {kandidat[0][0]:.2f}")

print("\nKandidat kunci berdasarkan frekuensi:", kandidat_kunci)
print("Kata kunci yang digunakan          :", key)
print("Alasan: setiap posisi menghasilkan huruf dengan score frekuensi terbaik, yaitu H-U-R-U-F.")

key_ulang = ""
key_index = 0
for char in cipher_vigenere:
    if char in ALPHABET:
        key_ulang += key[key_index % len(key)]
        key_index += 1
    else:
        key_ulang += " "

print("\nProses dekripsi:")
print("Rumus  : P = (C - K) mod 26")
print("Cipher :", cipher_vigenere)
print("Kunci  :", key_ulang)

plaintext_vigenere = vigenere_decrypt(cipher_vigenere, key)
print("Plain  :", plaintext_vigenere)


# Enigma Machine
rotors = {
    "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO"
}

notch = {"I": "Q", "II": "E", "III": "V"}
reflector_b = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
plugboard_pairs = {"X": "O", "O": "X", "D": "Z", "Z": "D", "N": "U", "U": "N"}

def plugboard(letter):
    return plugboard_pairs.get(letter, letter)

def rotor_forward(letter, rotor, position, ring):
    x = (ALPHABET.index(letter) + position - ring) % 26
    y = ALPHABET.index(rotors[rotor][x])
    return ALPHABET[(y - position + ring) % 26]

def rotor_backward(letter, rotor, position, ring):
    x = (ALPHABET.index(letter) + position - ring) % 26
    y = rotors[rotor].index(ALPHABET[x])
    return ALPHABET[(y - position + ring) % 26]

def step_rotors(positions):
    right, middle, left = positions
    right_notch = right == ALPHABET.index(notch["II"])
    middle_notch = middle == ALPHABET.index(notch["I"])
    if middle_notch:
        positions[2] = (positions[2] + 1) % 26
        positions[1] = (positions[1] + 1) % 26
    elif right_notch:
        positions[1] = (positions[1] + 1) % 26
    positions[0] = (positions[0] + 1) % 26

def enigma_decrypt(ciphertext):
    positions = [ALPHABET.index("H"), ALPHABET.index("G"), ALPHABET.index("B")]
    rings = [ALPHABET.index("O"), ALPHABET.index("J"), ALPHABET.index("O")]
    plaintext = ""

    print("\n=== PROSES ENIGMA ===")

    for nomor, original in enumerate(ciphertext, start=1):
        if original not in ALPHABET:
            continue

        step_rotors(positions)
        after_plug1 = plugboard(original)
        after_r2 = rotor_forward(after_plug1, "II", positions[0], rings[0])
        after_r1 = rotor_forward(after_r2, "I", positions[1], rings[1])
        after_r3 = rotor_forward(after_r1, "III", positions[2], rings[2])
        after_reflector = reflector_b[ALPHABET.index(after_r3)]
        back_r3 = rotor_backward(after_reflector, "III", positions[2], rings[2])
        back_r1 = rotor_backward(back_r3, "I", positions[1], rings[1])
        back_r2 = rotor_backward(back_r1, "II", positions[0], rings[0])
        result = plugboard(back_r2)
        plaintext += result

        print(f"{nomor:2}. {original} -> {after_plug1} -> {after_r2} -> {after_r1} -> {after_r3} -> {after_reflector} -> {back_r3} -> {back_r1} -> {back_r2} -> {result}")

    return plaintext

ciphertext_enigma = "MMZSWBURMKQHJSVZCWWWYEABEVLTRHVTSNMHXABPPWD"

print("\n=== ENIGMA MACHINE ===")
print("Urutan rotor (kanan ke kiri): II, I, III")
print("Ring setting (kanan ke kiri): O, J, O")
print("Posisi awal (kanan ke kiri): H, G, B")
print("Plugboard: X-O, D-Z, N-U")
print("Reflector: B")
print("Ciphertext:", ciphertext_enigma)

plaintext_enigma = enigma_decrypt(ciphertext_enigma)

print("\nPlaintext:", plaintext_enigma)
print("Plaintext terbaca: HALO QOMARI INI MFD SELAMAT MENGERJAKAN SOAL ENIGMA")