def aes(key, key_size, plaintext):
    
    num_rounds = {16: 10, 24: 12, 32: 14}[key_size]
    expanded_key = key_expansion(key, key_size, num_rounds)

    
    state = add_round_key(plaintext, expanded_key[:key_size])
    
    
    for i in range(1, num_rounds):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, expanded_key[i*key_size:(i+1)*key_size])

    
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, expanded_key[num_rounds*key_size:])
    
    return state

def key_expansion(key, key_size, num_rounds):
    word_size = key_size // 8
    num_words = len(key) // word_size
    expanded_key_size = 4 * (num_rounds + 1) * word_size
    expanded_key = bytearray(expanded_key_size)
    

    for i in range(num_words):
        expanded_key[i*word_size:(i+1)*word_size] = key[i*word_size:(i+1)*word_size]
        
   
    for i in range(num_words, 4 * (num_rounds + 1)):
        temp = expanded_key[(i-1)*word_size:i*word_size]
        if i % num_words == 0:
            temp = bytearray(sub_word(rot_word(temp)))  
          
            temp[0] ^= RCON[i // num_words]
        elif num_words > 6 and i % num_words == 4:
            temp = sub_word(temp) 
        temp = xor_bytes(temp, expanded_key[(i-num_words)*word_size:(i-num_words+1)*word_size])
        expanded_key[i*word_size:(i+1)*word_size] = temp
        
    return expanded_key

def sub_word(word):
    return [S_BOX[b] for b in word]

  import sys

def sub_bytes(state):
    s_box = [
        [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7,


def rot_word(word):
    return word[1:] + word[:1]

def xor_bytes(a, b):
    return bytearray([x ^ y for (x, y) in zip(a, b)])

def sub_bytes(state):
    for i in range(len(state)):
        state[i] = S_BOX[state[i]]
    return state

def shift_rows(state):
    for i in range(4):
        state[i::4] = state[i::4][i:] + state[i::4][:i]
    return state

def mix_columns(state):
    for i in range(0, len(state), 4):
        a = state[i]
        b = state[i+1]
        c = state[i+2]
        d = state[i+3]
        state[i]   = multiply(a, 2) ^ multiply(b, 3) ^ c ^ d
        state[i+1] = a ^ multiply(b, 2) ^ multiply(c, 3) ^ d
        state[i+2] = a ^ b ^ multiply(c, 2) ^ multiply(d, 3)
        state[i+3] = multiply(a, 3) ^ b ^ c ^ multiply
