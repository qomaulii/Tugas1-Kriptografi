ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Caesar Cipher

def caesar_decrypt(ciphertext, shift):
    result = ""

    for char in ciphertext:
        if char in ALPHABET:
            index = ALPHABET.index(char)
            result += ALPHABET[(index - shift) % 26]
        else:
            result += char

    return result


cipher_caesar = "BIVXI SCVKQ GIVO JMVIZ XMAIV QVQ BMBIX UMVRILQ BMSI BMSQ"

print("=== CAESAR CIPHER ===")

for shift in range(5, 12):
    plaintext = caesar_decrypt(cipher_caesar, shift)
    print(f"Shift {shift}: {plaintext}")

print("\nKunci yang benar: 8")
print("Plaintext       :", caesar_decrypt(cipher_caesar, 8))


# Vigenere Cipher

cipher_vigenere = (
    "AOXUX PHZ GJUALDN WYDUMHGRH FUXR "
    "NJYBRXFW MRHIP JFFNHFWUGLNZE PSUJCP"
)

key = "HURUF"


def clean_text(text):
    result = ""

    for char in text:
        if char in ALPHABET:
            result += char

    return result


def vigenere_decrypt(ciphertext, key):
    result = ""
    key_index = 0

    for char in ciphertext:
        cipher_index = ALPHABET.index(char)
        key_value = ALPHABET.index(key[key_index % len(key)])
        result += ALPHABET[(cipher_index - key_value) % 26]
        key_index += 1

    return result


text_vigenere = clean_text(cipher_vigenere)

print("\n=== VIGENERE CIPHER ===")
print("Panjang kunci :", len(key))
print("Kata kunci    :", key)

plaintext_vigenere = vigenere_decrypt(text_vigenere, key)
print("Plaintext     :", plaintext_vigenere)


# Enigma Machine

rotors = {
    "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO"
}

notch = {
    "I": "Q",
    "II": "E",
    "III": "V"
}

reflector_b = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

plugboard_pairs = {
    "X": "O",
    "O": "X",
    "D": "Z",
    "Z": "D",
    "N": "U",
    "U": "N"
}


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
    positions = [
        ALPHABET.index("H"),
        ALPHABET.index("G"),
        ALPHABET.index("B")
    ]

    rings = [
        ALPHABET.index("O"),
        ALPHABET.index("J"),
        ALPHABET.index("O")
    ]

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