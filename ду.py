import numpy as np

codes = {'Ы': [1, 1, 0, 1, 1, 0, 1, 1],
         'Ь': [1, 1, 0, 1, 1, 1, 0, 0],
         'Э': [1, 1, 0, 1, 1, 1, 0, 1],
         'Ю': [1, 1, 0, 1, 1, 1, 1, 0],
         'Я': [1, 1, 0, 1, 1, 1, 1, 1]}

class MoreThanOneError(Exception):
    pass

def encode(code):
    control_bits = control_matrix.dot(code)
    encoded = np.zeros(code.shape[0] + control_bits.shape[0] + 1)
    encoded[message_idxs] = code
    encoded[control_idxs] = control_bits
    encoded[-1] = np.sum(encoded)

    encoded = encoded % 2
    return encoded

def decode(given_code):
    code = given_code[message_idxs]
    encoded = encode(code)
    error_idxs = (encoded[control_idxs] != given_code[control_idxs]).nonzero()[0]
    error_idx = (control_idxs[error_idxs] + 1).sum() - 1

    if given_code.sum() % 2 == 0:
        raise MoreThanOneError

    H = np.array([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                  [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
    ])
    print(H.dot(given_code) % 2)
    print(f'detected error at {error_idx+1}')
    if len(error_idxs) == 0:
        return code

    given_code[error_idx] = 1 - given_code[error_idx]

    return given_code[message_idxs]

control_matrix = np.array([[1, 1, 0, 1, 1, 0, 1, 0],
                          [1, 0, 1, 1, 0, 1, 1, 0],
                           [0, 1, 1, 1, 0, 0, 0, 1],
                           [0, 0, 0, 0, 1, 1, 1, 1]])
message_idxs = np.array([3, 5, 6, 7, 9, 10, 11, 12]) - 1
control_idxs = np.setdiff1d(np.arange(12), message_idxs)
NUM_ERRORS = 1

for letter in codes.keys():
    code = np.array(codes[letter])
    encoded = encode(code)
    print(f'Letter: {letter}')
    print(f'Code: {code}')
    print(f'Encoded:\t\t{encoded}')
    try:
        curr_idxs = message_idxs.copy()
        for i in range(NUM_ERRORS):
            error_idx = np.random.choice(curr_idxs, 1)
            curr_idxs = curr_idxs[curr_idxs != error_idx]
            error_message = encoded
            error_message[error_idx] = 1 - error_message[error_idx]

        print(f'Error message:  {error_message}')
        print(f'Error is at {error_idx[0] + 1} position')
        decoded = decode(error_message)
        print(f'Decoded: {decoded}')
    except MoreThanOneError:
        print('More than one error')
    print()