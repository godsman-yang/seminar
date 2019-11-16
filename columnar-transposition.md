# columnar transposition
암호화 방법 중에 columnar transposition을 구현한다.
전치암호 방법 중에 하나로 행렬, 2차원 배열을 이용한다.

이해하기 쉽도록 wikipedia의 설명대로 구현한다. 플레인 문자열은 "WEAREDISCOVEREDFLEEATONCE"을 이용하고, 키는 "ZEBRAS"를 이용한다.
"ZEBRAS" 키를 632415 로 변환되는 방법도 구현한다.

## ZEBRAS Key 변환
키는 행렬의 컬럼을 나타낸다. 1부터 키의 길이까지의 숫자로 나타난다.
* ZEBRAS는 6문자이므로 1부터 6까지의 숫자로 나타나야 한다.
* 단순히 문자%26 을 이용하면 위키피디아의 샘플과 값이 다르다.
* 키 중에 가장 작은 문자부터 순서대로 숫자를 부여한다.
* 'ZEBRAS' 는 가장 작은 문자인 'A'는 1, 'B'는 2 ... 가장 나중 문자 'Z'는 6이다.
* 순서대로 나열하면 632415가 된다.
* 같은 문자가 있을 경우 앞의 문자에 작은 수를 할당한다.
* 'AAAAAA'를 키로 사용하면 123456이 된다.

```python
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
```

## 암호화


## 복호화


## 질문
* key 값이 겹칠 때, 두번째는 +1을 한다.
* full이 아닐 때, 채우지 않고도 가능한가?
*

## 참고사이트
* 위키피디아 - [Transposition cipher](https://en.wikipedia.org/wiki/Transposition_cipher)
  - columnar transposition
* https://crypto.interactive-maths.com/columnar-transposition-cipher.html
