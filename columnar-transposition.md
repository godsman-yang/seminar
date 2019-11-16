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
## 문자열 입력
입력 문자열이 키로 나누어 떨어지지 않으면 '*' 문자로 채웠다.
* 위키피디아의 샘플처럼 'WEAREDISCOVEREDFLEEATONCE'를 입력하면
* 문자열은 'WEAREDISCOVEREDFLEEATONCE*****'로 변경된다.
* 나누어 떨어지지 않을 때 문자열을 추가하지 않아도 가능한지는 확인이 필요하다. 

## 암호화
'WEAREDISCOVEREDFLEEATONCE' 문자열을 키의 길이만큼 나누어서 행렬을 만든다.
* 키의 길이는 6 이다.
* 원문 문자열의 길이가 25이므로 6으로 나눠 떨어지도록 5개의 '*'를 추가한다.
```
W E A R E D
I S C O V E 
R E D F L E 
E A T O N C 
E * * * * *
```

* 키의 순서대로 컬럼을 읽는다.
* 1번 컬럼은 'EVLN*' 2번 컬럼은 'ACDT*' ... 6번 컬럼은 'WIREE'
* 암호화 결과는 'EVLN*ACDT*ESEA*ROFO*DEEC*WIREE' 이다.
```
6 3 2 4 1 5
- - - - - -
W E A R E D
I S C O V E 
R E D F L E 
E A T O N C 
E * * * * *
```

## 복호화
'EVLN*ACDT*ESEA*ROFO*DEEC*WIREE' 문자열을 키의 길이만큼 나누어진 행렬에 입력한다.
* 키의 길이는 6 이다. 이건 행의 길이가 된다.
* 컬럼의 길이(height)는 암호문 길이 / 키의 길이 = 30 / 6 = 5 이다.
* 첫번째 읽은 5개의 문자 'EVLN*'을 1번 컬럼(인덱스 4)에 입력한다.
```
6 3 2 4 1 5
0 1 2 3 4 5 - 인덱스
- - - - - -
        E
        V 
        L 
        N 
        *
```
* 두번째 읽은 5개의 문자 'ACDT*'을 2번 컬럼(인덱스 2)에 입력한다.
```
6 3 2 4 1 5
0 1 2 3 4 5 - 인덱스
- - - - - -
    A   E
    C   V 
    D   L 
    T   N 
    *   *
```
* 6번째 마지막으로 읽은 5개의 문자 'E*'을 6번 컬럼(인덱스 0)에 입력한다.
```
6 3 2 4 1 5
0 1 2 3 4 5 - 인덱스
- - - - - -
W E A R E D
I S C O V E 
R E D F L E 
E A T O N C 
E * * * * *
```
* 행의 순서대로 문자를 읽는다.
* 복호화 결과는 'WEAREDISCOVEREDFLEEATONCE*****' 이다.
```
W E A R E D
I S C O V E 
R E D F L E 
E A T O N C 
E * * * * *
```

## 실행결과

```bash
> python columnar-transposition.py
Input original text(default 'WEAREDISCOVEREDFLEEATONCE):
plain_text:  WEAREDISCOVEREDFLEEATONCE
Input your key(default 'ZEBRAS'):
plain_text(full):  WEAREDISCOVEREDFLEEATONCE*****
key:  ZEBRAS  ->  [6, 3, 2, 4, 1, 5]
cipher_text:  EVLN*ACDT*ESEA*ROFO*DEEC*WIREE
decrypted_text:  WEAREDISCOVEREDFLEEATONCE*****
```

## 질문
* full이 아닐 때, 채우지 않고도 가능한가?

## 참고사이트
* 위키피디아 - [Transposition cipher](https://en.wikipedia.org/wiki/Transposition_cipher)
  - columnar transposition
* https://crypto.interactive-maths.com/columnar-transposition-cipher.html
