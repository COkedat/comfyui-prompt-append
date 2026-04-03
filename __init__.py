import re

def clean_tag(tag: str) -> str:
    """프롬프트에서 괄호와 가중치를 제거하고 순수 텍스트만 추출 + 소문자화"""
    cleaned = re.sub(r'[()\[\]{}]|:\d+(?:\.\d+)?', '', tag)
    return cleaned.strip().lower()

class ConditionalPromptAppendNode:
    """
    ComfyUI에서 인식할 커스텀 노드 클래스
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # 입력 프롬프트
                "base_prompt": ("STRING", {"multiline": True, "default": ""}),
                
                # 입력 프롬프트에서 검색할 프롬프트
                "search_prompt": ("STRING", {"multiline": True, "default": ""}),
                
                # 검색 논리 옵션 (OR: 하나라도 감지 (기본 값), AND: 모두 감지)
                "search_logic": (["OR", "AND"],),
                
                # 추가 프롬프트
                "append_prompt": ("STRING", {"multiline": True, "default": ""}),
                
                # 추가 조건 여부 (Always: 항상 추가, If Not Detected: 감지 X, If Detected: 감지 O)
                "condition": (["Always", "If Not Detected", "If Detected"],),
                
                # 입력 프롬프트 구분자 (기본값: ",")
                "input_delimiter": ("STRING", {"default": ","}),
                
                # 출력 프롬프트 추가 프롬프트와 결합 시 구분자 (기본값: ", ")
                "output_delimiter": ("STRING", {"default": ", "}),
                
                # 추가 프롬프트가 입력 프롬프트에 존재할 시 제거 스킵 여부 (기본값: True)
                "skip_duplicate": ("BOOLEAN", {"default": True}),
                
                # 가중치 (기본값: 1.0)
                "weight": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.05}),
                
                # 추가 프롬프트 결합시 입력 프롬프트 앞뒤 위치 설정 (기본값: back)
                "position": (["back", "front"],),
            },
        }
    
    # 반환 타입
    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("prompt", "is_detected")
    FUNCTION = "process"
    CATEGORY = "utils/prompt"

    def process(self, base_prompt, search_prompt, search_logic, append_prompt, condition, input_delimiter, output_delimiter, skip_duplicate, weight, position):
        base_prompt = base_prompt.strip()
        in_delim = input_delimiter if input_delimiter else ","
        
        # 1. 기존 프롬프트 파싱
        existing_cleaned_tags = set()
        if base_prompt:
            existing_cleaned_tags = {clean_tag(tag) for tag in base_prompt.split(in_delim) if tag.strip()}
            
        # 2. 프롬프트 검색 (AND / OR 조건에 따른 is_detected 판단)
        is_detected = False
        if search_prompt.strip():
            # "\n"을 in_delim으로 치환 후 split으로 리스트화
            normalized_search_prompt = search_prompt.replace('\n', in_delim)
            search_tags = [clean_tag(tag) for tag in normalized_search_prompt.split(in_delim) if tag.strip()]
            
            if search_tags: # 검색할 태그가 존재하는 경우에만 실행
                if search_logic == "AND":
                    # 모든 검색 태그가 기존 프롬프트에 있어야 is_detected가 True
                    is_detected = all(tag in existing_cleaned_tags for tag in search_tags)
                else: # "OR" (기본 작동 방식)
                    # 검색 태그 중 하나라도 기존 프롬프트에 있으면 is_detected가 True
                    is_detected = any(tag in existing_cleaned_tags for tag in search_tags)
                    
        # 3. 추가 조건 검사
        # 추가 여부는 기본으로 False
        should_append = False
        if condition == "Always":
            # Always는 검색 결과와 관계 없이 항상 추가
            should_append = True
        elif condition == "If Not Detected" and not is_detected:
            # If Not Detected일 때, is_detected가 False일 경우
            should_append = True
        elif condition == "If Detected" and is_detected:
            # If Detected일 때, is_detected가 True일 경우
            should_append = True
            
        # 4. 프롬프트 추가 로직 (조건을 만족할 때만 실행)
        
        # 최종적으로 추가될 프롬프트 리스트
        tags_to_add = []
        
        # 추가 해야한다면
        if should_append and append_prompt.strip():
            # "\n"을 in_delim으로 치환 후 split으로 리스트화
            normalized_prompt = append_prompt.replace('\n', in_delim)
            new_tags = [tag.strip() for tag in normalized_prompt.split(in_delim) if tag.strip()]
            
            # 프롬프트 추가
            for tag in new_tags:
                clean_new = clean_tag(tag)
                
                # 프롬프트 중복 여부 검사 + 제거 스킵 여부 확인
                if skip_duplicate and clean_new in existing_cleaned_tags:
                    continue
                
                # 프롬프트 추가
                existing_cleaned_tags.add(clean_new)
                
                # 태그 리스트 추가
                tags_to_add.append(tag)
                    
        # 5. 결과 반환 처리
        # 추가할 프롬프트가 없다면 그냥 입력 프롬프트 반환
        if not tags_to_add:
            return (base_prompt, is_detected)
        
        # 순수 태그들을 먼저 구분자(예: 쉼표)로 결합
        new_prompt_str = output_delimiter.join(tags_to_add)
        
        # 결합된 전체 텍스트에 가중치 적용 (1.0이 아닐 경우)
        if weight != 1.0:
            new_prompt_str = f"({new_prompt_str}:{weight})"
        
        if not base_prompt:
            # 입력 프롬프트가 없을 경우, 추가 프롬프트만 반환
            result_prompt = new_prompt_str
        elif position == "front":
            # position이 front라면 입력 프롬프트 앞에 추가
            result_prompt = f"{new_prompt_str}{output_delimiter}{base_prompt}"
        else:
            # position이 back이라면 입력 프롬프트 뒤로 추가
            result_prompt = f"{base_prompt}{output_delimiter}{new_prompt_str}"
            
        # 결과 반환
        return (result_prompt, is_detected)

# ComfyUI 시스템에 노드 등록
NODE_CLASS_MAPPINGS = {
    "ConditionalPromptAppendNode": ConditionalPromptAppendNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ConditionalPromptAppendNode": "Conditional Prompt Append"
}