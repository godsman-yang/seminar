def get_key_nums(key):
  key_nums = []
  key_len = len(key)

  for i in range(key_len):
    # char = char -'A'
    key_value = (ord(key[i])-ord('A')) % key_len + 1
    # key_value = ord(key[i]) % key_len + 1
    print('key_value: ', key_value)
    print('key_nums: ', key_nums)

    while(True):
      if key_value in key_nums:
        # key_value += 1
        key_value = key_value % key_len +1
        print('if key_value: ', key_value)
        print('if key_nums: ', key_nums)
      else:
        key_nums.append(key_value)
        print('else key_value: ', key_value)
        print('else key_nums: ', key_nums)
        break
  return key_nums

def get_key_nums_wiki(key):
  keys = list(key)
  key_nums = keys.copy()

  for i in range(len(key_nums)):
    key_value = min(keys)
    key_index = keys.index(key_value)
    del(keys[key_index])

    key_index = key_nums.index(key_value)
    key_nums[key_index] = i + 1

    # print('key_value: ', key_value)
    # print('key_nums: ', key_nums)

  return key_nums

def make_cipher(plain_text, keynums):
  w = len(keynums)
  h = len(plain_text)//w

  cipher_matrix = [[0 for x in range(w)] for y in range(h)]
  # print(cipher_matrix) 
  
  cipher_text = ""

  for i in range(h):
    cipher_matrix[i] = list(plain_text[i*w:i*w+w])
  
  # print(cipher_matrix)

  for j in range(w):
    width = keynums.index(j + 1)
    # print("width: ", width)

    for i in range(h):
      cipher_text += cipher_matrix[i][width]
      # print(cipher_matrix[i][width])

  return cipher_text

def make_decrypted(cipher_text, keynums):
  w = len(keynums)
  h = len(cipher_text)//w

  decrypted_matrix = [[0 for x in range(w)] for y in range(h)]
  # print(cipher_matrix) 
  
  decrypted_text = ""

  index = 0
  for j in range(w):
    width = keynums.index(j + 1)
    # print("width: ", width)

    for i in range(h):
      decrypted_matrix[i][width] = cipher_text[index]
      index += 1 
      # cipher_text += cipher_matrix[i][height]
      # print(decrypted_matrix[i][width])

  # print(decrypted_matrix)

  decrypted_text =""
  for i in range(h):
    decrypted_text += ''.join(decrypted_matrix[i]) 

  return decrypted_text

plain_text = input("Input original text(default 'WEAREDISCOVEREDFLEEATONCE): ")
if(plain_text == ''):
  plain_text = "WEAREDISCOVEREDFLEEATONCE"

print("plain_text: ", plain_text)

# cipher_text
# decrypted_text

key = input("Input your key(default 'ZEBRAS'): ")
if(key == ''):
  key = "ZEBRAS"
# key = key[0:6] // default key lengh = 6
key_len = len(key)
plain_mod = len(plain_text) % key_len
if(plain_mod != 0):
  plain_text += ('*' * (key_len-plain_mod)) # key_len - 나머지
  print("plain_text(full): ", plain_text)

key_nums = get_key_nums_wiki(key)
print("key: ", key, " -> ", key_nums)

cipher_text = make_cipher(plain_text, key_nums)
print("cipher_text: ", cipher_text)

decrypted_text = make_decrypted(cipher_text, key_nums)
print("decrypted_text: ", decrypted_text)