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
