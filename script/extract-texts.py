#!/usr/bin/env python3
"""
gv-1.json에서 모든 고유한 텍스트를 추출합니다.
"""
import json

def extract_texts_from_dialog(dialog_array, texts_set):
    """대화 배열에서 텍스트를 추출합니다."""
    if not dialog_array:
        return

    for dialog in dialog_array:
        if isinstance(dialog, dict) and 'text' in dialog:
            texts_set.add(dialog['text'])


def extract_texts_from_dialog_object(dialog_obj, texts_set):
    """대화 객체에서 텍스트를 추출합니다."""
    if not dialog_obj:
        return

    for key, value in dialog_obj.items():
        if key in ['start', 'middle', 'end']:
            if isinstance(value, list):
                extract_texts_from_dialog(value, texts_set)
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    extract_texts_from_dialog(sub_value, texts_set)


def extract_all_texts(data):
    """authoring 데이터에서 모든 고유한 텍스트를 추출합니다."""
    texts = set()

    if 'application' not in data:
        return texts

    for level in data['application'].get('levels', []):
        for mission in level.get('missions', []):
            # Mission dialog
            if 'dialog' in mission:
                extract_texts_from_dialog_object(mission['dialog'], texts)

            # Challenge dialogs
            if 'challenges' in mission:
                for challenge in mission['challenges']:
                    if 'dialog' in challenge:
                        extract_texts_from_dialog_object(challenge['dialog'], texts)

    return texts


def main():
    input_file = 'src/resources/authoring/gv-1.json'
    output_file = 'translation-needed.txt'

    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Extracting unique texts...")
    texts = extract_all_texts(data)

    print(f"Writing {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, text in enumerate(sorted(texts), 1):
            f.write(f"{i}. {text}\n\n")

    print(f"✓ 추출 완료! {len(texts)}개의 고유한 텍스트를 찾았습니다.")
    print(f"  출력 파일: {output_file}")


if __name__ == '__main__':
    main()
