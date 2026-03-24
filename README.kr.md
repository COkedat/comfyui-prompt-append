# ComfyUI Conditional Prompt Append

ComfyUI를 위한 고급 조건부 프롬프트 추가 커스텀 노드. 특정 태그가 있는지 없는지에 따라 프롬프트를 동적으로 구성 가능.
(내가 필요해서 만듦)

## 주요 기능
* **조건부 프롬프트 추가 (핵심 기능):** 새 프롬프트를 언제 추가할지 정확하게 설정할 수 있음:
  * `Always`: 검색 결과와 상관없이 무조건 프롬프트를 추가함.
  * `If Detected`: 기준 프롬프트에 검색한 태그가 **있을 때만** 추가
  * `If Not Detected`: 기준 프롬프트에 검색한 태그가 **없을 때만** 추가
* **검색 논리 옵션:** 여러 태그 검색 시 `AND` / `OR` 조건을 지원함.
* **가중치 관리:** 추가할 태그들을 자동으로 묶어서 하나의 가중치 괄호를 씌워줌 (예: `(tag1, tag2:1.2)`).
* **중복 방지:** 기준 프롬프트에 이미 들어있는 태그가 또 추가되는 걸 막아주는 `skip_duplicate` 옵션.
* **유연한 구분자:** 여러 줄(Multiline) 텍스트 입력과 커스텀 구분자를 완벽하게 지원 (예: 줄바꿈을 쉼표로 자동 변환).
* **위치 제어:** 새 프롬프트를 기준 프롬프트의 맨 앞(`front`)에 넣을지 맨 뒤(`back`)에 넣을지 선택할 수 있음.

## 설치 방법
1. ComfyUI 커스텀 노드 폴더로 이동:
   ```bash
   cd ComfyUI/custom_nodes/```
2. 이 레포지토리를 클론(Clone)함:
   ```
   git clone https://github.com/COkedat/comfyui-prompt-append```
3. ComfyUI 재시작.
4. utils/prompt 카테고리에서 Conditional Prompt Append 노드를 찾아 사용.

## 사용 방법
* **base_prompt:** 기준이 되는 메인 프롬프트 텍스트.
* **search_prompt:** `base_prompt` 안에서 찾고 싶은 대상 태그.
* **search_logic:** 여러 태그를 검색할 때 `AND` 또는 `OR` 논리를 적용할지 결정.
* **append_prompt:** 조건이 맞을 때 추가할 새로운 프롬프트.
* **condition:** 새 프롬프트를 어떤 조건(항상 추가, 감지될 때만, 감지 안 될 때만)에서 추가할지 선택.
* **input_delimiter:** 입력 프롬프트(`base_prompt`, `search_prompt` 등)의 단어들을 쪼갤 때 사용하는 구분자(기준 기호).
* **output_delimiter:** 최종 출력 프롬프트를 하나로 합칠 때 사용할 연결 구분자.
* **skip_duplicate:** 추가하려는 프롬프트가 이미 `base_prompt`에 있을 경우, 중복으로 추가되는 것을 막아줌.
* **position:** 새 프롬프트를 기준 프롬프트의 맨 앞(`front`)에 붙일지, 맨 뒤(`back`)에 붙일지 선택.
* **prompt (Output):** 조건에 따라 최종적으로 결합된 프롬프트 결과물.
* **is_detected (Output):** 검색 대상 프롬프트가 감지되었는지 여부를 BOOLEAN (True/False) 값으로 반환. 이 값을 다른 조건 노드나 스위치 노드로 연결해 사용가능.