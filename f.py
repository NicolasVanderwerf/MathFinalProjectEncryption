def encrypt(plaintext, key_matrix, modulo, alphabet):
    # Map chars to numbers from 0 to len(alphabet)-1
    char_to_num = {char: idx for idx, char in enumerate(alphabet)}
    num_to_char = {v: k for k, v in char_to_num.items()}
    padding_val = len(alphabet)  # Use a padding value outside the char range

    # Convert plaintext to numbers
    numbers = [char_to_num[c] for c in plaintext if c in char_to_num]

    # Pad if necessary
    if len(numbers) % 2 != 0:
        numbers.append(padding_val)

    plaintext_matrix = np.array(numbers).reshape(-1, 2).T
    ciphertext_matrix = (key_matrix.dot(plaintext_matrix) % modulo).T

    # Convert back to chars (skip padding_val when converting back)
    ciphertext = []
    for pair in ciphertext_matrix:
        for num in pair:
            if num != padding_val:
                if num in num_to_char:
                    ciphertext.append(num_to_char[num])
                else:
                    # If something unexpected, place a placeholder
                    ciphertext.append('?')
    return ''.join(ciphertext), ciphertext_matrix


def decrypt(ciphertext, inverse_key_matrix, modulo, alphabet):
    char_to_num = {char: idx for idx, char in enumerate(alphabet)}
    num_to_char = {v: k for k, v in char_to_num.items()}
    padding_val = len(alphabet)

    numbers = [char_to_num[c] for c in ciphertext if c in char_to_num]
    if len(numbers) % 2 != 0:
        numbers.append(padding_val)

    cipher_matrix = np.array(numbers).reshape(-1, 2)
    decrypted_matrix = (inverse_key_matrix.dot(cipher_matrix.T) % modulo).T

    # Convert back to text and remove padding
    plaintext_chars = []
    for pair in decrypted_matrix:
        for num in pair:
            if num == padding_val:
                # Padding encountered, skip it
                continue
            if num in num_to_char:
                plaintext_chars.append(num_to_char[num])
            else:
                plaintext_chars.append('*')
    return ''.join(plaintext_chars).rstrip('A')