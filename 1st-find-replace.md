# 첫번째 세미나
첫번째 세미나는 문자열 변경하는 것입니다. 실제 목적은
* 어려운 작업을 만났을 때 쉽게 하는 방법 생각해 보기
* 실수할 가능성이 있는 작업을 만났을 때 실수하지 않도록 하기
* 도구나 프로그램을 배우는 것보다는 무엇을 할 수 있는지 알기
  - 된다는 걸 알고 나면 (할 수 있는 사람에게)해달라고 하면 됩니다.
* 다른 직원들의 작업 이해하기

도구 활용
* Visual Studio Code
* Regular Expression - 정규식
* python - 프로그램보다는 활용

## Visual Studio Code 설치하기
* [Visual Studio Code](https://code.visualstudio.com/) 설치하기
* 한글로 번역해 놓은 [한글 Visual Studio Code 튜토리얼](https://demun.github.io/vscode-tutorial/)이 있습니다.
* 실제로는 필요할 때마다 검색해서 사용합니다. 유용한 기능이 많습니다.
  - 'vscode 멀티커서'를 검색해 보세요.

## Emerging Threats 룰 다운받기
```bash
> curl -o emergin.rules.tar.gz https://rules.emergingthreats.net/open/suricata-5.0/emerging.rules.tar.gz
> tar xzvf .\emergin.rules.tar.gz
```
## Suricata 룰 Deprecated
[suricata-5.0.0 > http-keywords > 5.12.4. uricontent](https://suricata.readthedocs.io/en/suricata-5.0.0/rules/http-keywords.html#uricontent)

uricontent를 content로 변경하고, 뒤에 http_uri 키워드를 추가해야 함.
![](https://suricata.readthedocs.io/en/suricata-5.0.0/_images/uricontent1.png) ![](https://suricata.readthedocs.io/en/suricata-5.0.0/_images/http_uri.png)
* uricontent: "문자열"; -> content: "문자열"; http_uri;

## How to change/replace
문자열 찾기/리플레이스 - find/replace
```
#alert tcp $HOME_NET any -> $EXTERNAL_NET $HTTP_PORTS (msg:"ET DELETED KitCo Kcast Ticker (agtray)"; flow: to_server,established; uricontent:"/pr/agtray.txt"; nocase; reference:url,doc.emergingthreats.net/2000569; classtype:policy-violation; sid:2000569; rev:6; metadata:created_at 2010_07_30, updated_at 2019_08_22;)
```
* 'uricontent' 찾는 건 가능 -> 찾은 문자열을 'content'로 변경하는 것 가능
* 찾은 문자열을 변경하고 - uricontent -> content
* 문자열 뒤의 문자열은 유지하고 - "/pr/agtray.txt";
* 그 뒤에 http_uri; 입력을 해야 함 - http_uri;
```
#alert tcp $HOME_NET any -> $EXTERNAL_NET $HTTP_PORTS (msg:"ET DELETED KitCo Kcast Ticker (agtray)"; flow: to_server,established; content:"/pr/agtray.txt"; http_uri; nocase; reference:url,doc.emergingthreats.net/2000569; classtype:policy-violation; sid:2000569; rev:6; metadata:created_at 2010_07_30, updated_at 2019_08_22;)
```

## 정규식을 알아두세요.
정규식, 영어로는 regular expression 이라고 합니다.
외우고 있으면 좋지만 알아두기만 해도 사용하기 편합니다. 필요하면 [regex101.com](https://regex101.com/) 을 이용하세요. 
* 위에 rule을 TEST STRING에 복사합니다.
* 'uricontent'를 REGULAR EXPRESSION 부분에 입력합니다.
  - 'uricontent'를 찾아주는 걸 알 수 있습니다.

우리가 찾고 싶은 것은 uricontent:"문자열"; 입니다.
* 정규식으로 uricontent:".*";
* 괄호를 이용하면 리플레이스할 때 이용할 수 있습니다. 'uricontent:(".*";)'
* 검색되고 Group 1 부분에 패턴이 나타나는 것을 알 수 있습니다.
* visual studio code(vscode, code)를 이용해서 정규식을 이용해서 리플레이스합니다.
```
find: uricontent:(".*";)
replace: content:$1 http_uri;
```

다른 예제로 해 볼까요
* uricontent 뒤에 "(문자열)" 형태가 존재하는 것
```
#alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS (msg:"ET DELETED TxtBlog index.php m Parameter Local File Inclusion"; flow:to_server,established; content:"GET "; depth:4; uricontent:"/index.php?m="; nocase; pcre:"/(\.\.\/){1,}/U"; reference:bugtraq,32498; reference:url,milw0rm.com/exploits/7241; reference:url,doc.emergingthreats.net/2008923; classtype:web-application-attack; sid:2008923; rev:3; metadata:affected_product Web_Server_Applications, attack_target Server, deployment Datacenter, tag Local_File_Inclusion, signature_severity Major, created_at 2010_07_30, updated_at 2019_08_22;)
```
  - 'uricontent:(".*";)'
  - uricontent 뒤의 '"' 까지 포함되어 검색 'uricontent:"/index.php?m="; nocase; pcre:"/(\.\.\/){1,}/U";'
  - 정규식의 greedy(탐욕스러운) 특성 때문입니다. 매칭이 될때 가장 길게 매칭하려고 하는 특성
  - 이 예제에서는 non-greedy(또는 lazy)로 설정해야 합니다.
  - 'uricontent:(".*?";)' 처럼 '?'를 이용해 보세요.
  - 1개의 그룹으로 검색이 됩니다. 'uricontent:"/index.php?m=";'
  - vscode 에서 테스트해 보세요.
```
find: uricontent:(".*?";)
replace: content:$1 http_uri;
```

* uricontent가 여러 개일 경우에는 어떻게 될까요? 
```
#alert http $HOME_NET any -> $EXTERNAL_NET $HTTP_PORTS (msg:"ET DELETED Zango Spyware Activity"; flow:to_server,established; uricontent:"/banman/banman.asp?ZoneID="; nocase; uricontent:"&Task="; nocase; uricontent:"&X="; nocase; reference:url,securityresponse.symantec.com/avcenter/venc/data/pf/adware.180search.html; reference:url,doc.emergingthreats.net/bin/view/Main/2003170; classtype:trojan-activity; sid:2003170; rev:4; metadata:created_at 2010_07_30, updated_at 2019_08_22;)
```
  - 'uricontent:(".*";)'
  - uricontent 여러개가 하나로 검색됩니다. 'uricontent:"/banman/banman.asp?ZoneID="; nocase; uricontent:"&Task="; nocase; uricontent:"&X=";'
  - 정규식의 greedy(탐욕스러운) 특성 때문입니다. 매칭이 될때 가장 길게 매칭하려고 하는 특성
  - 이 예제에서는 non-greedy(또는 lazy)로 설정해야 합니다.
  - 'uricontent:(".*?";)' 처럼 '?'를 이용해 보세요.
  - 3개의 그룹으로 검색이 됩니다.
  - vscode 에서 테스트해 보세요.
```
find: uricontent:(".*?";)
replace: content:$1 http_uri;
```

* 복합적인 경우, uricontent가 여러 개 있으면서 뒤에 "(문자열)" 형태도 존재하는 것 
```
#alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS (msg:"ET DELETED Possible PHP-Calendar configfile Remote .PHP File Inclusion Arbitrary Code Execution Attempt"; flow:established,to_server; uricontent:"/php-calendar-1.1/update"; nocase; uricontent:"configfile="; nocase; content:".php"; nocase; pcre:"/\x2Fphp-calendar-1.1\x2Fupdate(08|10)\x2Ephp(\x3F|.*(\x26|\x3B))configfile=[^\x26\x3B]*[^a-zA-Z0-9_]/Ui"; reference:url,securitytracker.com/alerts/2009/Dec/1023375.html; reference:cve,2009-3702; reference:url,doc.emergingthreats.net/2010531; classtype:web-application-attack; sid:2010531; rev:2; metadata:created_at 2010_07_30, updated_at 2019_08_22;)
```
  - 잘 됩니다.
  - vscode 에서 테스트해 보세요.
```
find: uricontent:(".*?";)
replace: content:$1 http_uri;
```

## 참고1, 이렇게 하기 어려울 때는 수작업(노가다)으로 바꿔야 합니다.
그럴 때 도구를 이용하면 수고가 조금 줄어듭니다.
* vscode에는 '멀티커서' 기능이 있습니다.
* 커서는 키보드의 입력을 받는 곳이므로, 멀티커서의 기능은 동시에 여러 위치에 입력할 수 있다는 의미입니다.
* 가장 마지막 예제 룰을 vscode에 복사합니다.
* 'uricontent:(".*?";)'를 검색합니다. - 검색은 윈도우에서 단축키가 일반적으로 Ctrl+F 입니다.
  - 모든 검색을 선택해 주는 Ctrl+Shift+L 키를 누릅니다.
  - esc 키를 눌러서 검색창을 닫습니다.(검색창에서 'x'를 눌러도 됨)
  - 커서가 검색한 모든 단어의 가장뒤에 깜박거립니다. 방향키를 누를면 커서 위치가 이동이 되고, 아무 키를 누르면 선택된 단어가 변경됩니다.
  - 위에 리플레이스 기능처럼 하려면, 처음 검색한 후에 가장 끝에 http_uri;를 삽입하고, 'uricontent'를 검색해서 'content'로 변경하면 됩니다. 

## 참고2, 어디에 사용하면 좋을까요?
* 룰의 업데이트 날짜 변경하기
  - 'updated_at '을 검색한 후 Ctrl+Shift+L 입력
  - 검색창 닫기(ESC, 'x')
  - 커서 위치에서 날짜 수정 2019_11_15
---

## 룰의 업데이트 날짜 변경하기

[20022406, ]

# alert tcp $EXTERNAL_NET any -> $HOME_NET $HTTP_PORTS (msg:"ET EXPLOIT TAC Attack Directory Traversal"; flow:established,to_server; content:"/ISALogin.dll?";http_uri; nocase; pcre:"/Template=.*\.\./UGi"; reference:cve,2005-3040; reference:url,secunia.com/advisories/16854; reference:url,cirt.dk/advisories/cirt-37-advisory.pdf; reference:url,doc.emergingthreats.net/bin/view/Main/2002406; classtype:attempted-recon; sid:2002406; rev:4; metadata:created_at 2010_07_30, updated_at 2019_08_22;)
# alert tcp $EXTERNAL_NET any -> $HOME_NET $HTTP_PORTS (msg:"ET EXPLOIT TAC Attack Directory Traversal"; flow:established,to_server; content:"/ISALogin.dll?"; http_uri; nocase; pcre:"/Template=.*\.\./UGi"; reference:cve,2005-3040; reference:url,secunia.com/advisories/16854; reference:url,cirt.dk/advisories/cirt-37-advisory.pdf; reference:url,doc.emergingthreats.net/bin/view/Main/2002406; classtype:attempted-recon; sid:2002406; rev:4; metadata:created_at 2010_07_30, updated_at 2019_08_22;)

alert tcp $EXTERNAL_NET any -> $HOME_NET $HTTP_PORTS (msg:"ET EXPLOIT TAC Attack Directory Traversal"; flow:established,to_server; content:"/ISALogin.dll?";http_uri; nocase; pcre:"/Template=.*\.\./UGi"; reference:cve,2005-3040; reference:url,secunia.com/advisories/16854; reference:url,cirt.dk/advisories/cirt-37-advisory.pdf; reference:url,doc.emergingthreats.net/bin/view/Main/2002406; classtype:attempted-recon; sid:2002406; rev:4; metadata:created_at 2010_07_30, updated_at 2019_08_22;)
alert tcp $EXTERNAL_NET any -> $HOME_NET $HTTP_PORTS (msg:"ET EXPLOIT TAC Attack Directory Traversal"; flow:established,to_server; content:"/ISALogin.dll?"; nocase; pcre:"/Template=.*\.\./UGi"; reference:cve,2005-3040; reference:url,secunia.com/advisories/16854; reference:url,cirt.dk/advisories/cirt-37-advisory.pdf; reference:url,doc.emergingthreats.net/bin/view/Main/2002406; classtype:attempted-recon; sid:2002406; rev:4; metadata:created_at 2010_07_30, updated_at 2019_08_22;)

sid 주석
;\s?sid:(\d+);