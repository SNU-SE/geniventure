#!/usr/bin/env python3
"""
게임 콘텐츠 번역 스크립트
gv-1.json을 읽어서 gv-1-ko.json을 생성합니다.
"""
import json
import sys

# 캐릭터별 번역 매핑
CHARACTER_NAMES = {
    "HATCH": "해치 박사",
    "WEAVER": "위버 박사",
    "YEUNG": "양 교수",
    "HERRERA": "에레라 박사",
    "NETANYA": "네타냐"
}

# 주요 대화 번역 사전 (첫 번째 레벨)
TRANSLATIONS = {
    # Mission 1.1 - 시작 대화
    "Welcome, Cadet, to our underground hideout! I'm Professor Hatch, director of the Drake Breeder's Guild.":
        "환영합니다, 훈련생! 저는 드레이크 사육가 길드의 책임자 해치 박사입니다.",

    "And I'm Dr. Weaver, head of Mission Control here in the heart of our subterranean base.":
        "그리고 저는 위버 박사입니다. 이 지하 기지 중심부의 미션 컨트롤 책임자죠.",

    "Here in the Wyvern Republic, our dragons are under attack from the evil Kingdom of Darkwell, and in danger of going extinct! ":
        "여기 와이번 공화국에서는 우리 용들이 사악한 다크웰 왕국의 공격을 받고 있으며 멸종 위기에 처해 있습니다!",

    "You are training to be part of an elite team of scientists who will help us bring dragons back from the brink!":
        "여러분은 용들을 멸종 위기에서 구해낼 엘리트 과학자 팀의 일원이 되기 위한 훈련을 받게 됩니다!",

    "Time is running out and we need to train you fast! Come with me to the Sim Room. Click your VenturePad to navigate around the base.":
        "시간이 얼마 없습니다. 빨리 훈련을 시작해야 해요! 시뮬레이션 룸으로 가시죠. 벤처패드를 클릭해서 기지를 이동하세요.",

    # Challenge 1.1.1 - 시작
    "Good to meet you, Cadet! I'm Professor Yeung, and I'm in charge of the Sim Room.":
        "만나서 반갑습니다, 훈련생! 저는 양 교수이고 시뮬레이션 룸을 담당하고 있어요.",

    "This is where you can work with genes to make different looking drakes.":
        "여기에서 유전자를 조작해서 다르게 생긴 드레이크들을 만들 수 있습니다.",

    "Your task is to show us you can make 5 unique drakes. Each drake must look different from the rest.":
        "여러분의 임무는 5마리의 고유한 드레이크를 만들 수 있다는 것을 보여주는 것입니다. 각 드레이크는 다른 드레이크들과 달라야 해요.",

    "Remember, we learn what we can from drakes and then apply what we've learned to dragons. Click the purple screen to get started!":
        "기억하세요, 우리는 드레이크에서 배운 것을 용에게 적용합니다. 보라색 화면을 클릭해서 시작하세요!",

    # Challenge 1.1.1 - 성공
    "Our Cadet succeeded with the simulator, Professor Hatch!":
        "우리 훈련생이 시뮬레이터를 성공했어요, 해치 박사님!",

    "Great work, Cadet! You're now part of our team! And check out that crystal you've earned.":
        "훌륭해요, 훈련생! 이제 여러분은 우리 팀의 일원입니다! 그리고 획득한 크리스탈을 확인해 보세요.",

    "We use these crystals to power the devices that both heal and help breed our dragons. Red crystals are fairly weak, yellow crystals are a little stronger, and blue crystals are the most powerful. We need as much power as possible to build our forces and secure our defenses.":
        "우리는 이 크리스탈들을 사용해서 용을 치료하고 번식시키는 장치에 동력을 공급합니다. 빨간 크리스탈은 약하고, 노란 크리스탈은 조금 더 강하며, 파란 크리스탈이 가장 강력합니다. 우리의 전력을 강화하고 방어를 확보하기 위해 가능한 많은 힘이 필요합니다.",

    # Challenge 1.1.1 - 실패
    "You did it, but you took too many moves to earn a crystal. Let's try this one again!":
        "해냈지만 크리스탈을 얻기엔 너무 많은 이동을 했어요. 다시 시도해 봅시다!",

    # Mission 1.1 - 끝
    "Cadet, you're getting the hang of changing alleles to change the drake's traits.":
        "훈련생, 대립유전자를 바꿔서 드레이크의 형질을 변화시키는 법을 터득하고 있군요.",

    "Time to move on to the next Mission– helping out our dragon pilots.":
        "다음 미션으로 넘어갈 시간입니다 - 우리 용 조종사들을 도와주세요.",

    "It looks like you've finished everything! Open your VentureMap if you'd like to redo a challenge.":
        "모든 것을 완료한 것 같네요! 도전과제를 다시 하고 싶다면 벤처맵을 여세요.",

    # Challenge 1.2.1 - 시작
    "Now we need you to learn how to change alleles efficiently. Remember, alleles are different versions of a gene!":
        "이제 대립유전자를 효율적으로 바꾸는 법을 배워야 합니다. 기억하세요, 대립유전자는 유전자의 다른 버전입니다!",

    "Match the targeted drakes you see on the simulator screen by changing alleles where necessary.":
        "시뮬레이터 화면에 보이는 목표 드레이크와 일치하도록 필요한 곳의 대립유전자를 바꾸세요.",

    "Each allele change is a move. And it's critical that you do it in as few moves as possible! So tap on the purple simulator screen to start.":
        "각 대립유전자 변경은 한 번의 이동입니다. 가능한 적은 이동으로 하는 것이 중요합니다! 보라색 시뮬레이터 화면을 눌러서 시작하세요.",

    "You did it, but you took too many moves to earn a crystal.":
        "해냈지만 크리스탈을 얻기엔 너무 많은 이동을 했어요.",

    "Okay, Cadet! Remember the value of those crystals: red are weakest, yellow are in the middle, and blue crystals are the most powerful.":
        "좋아요, 훈련생! 크리스탈의 가치를 기억하세요: 빨강이 가장 약하고, 노랑은 중간이고, 파란 크리스탈이 가장 강력합니다.",

    # Challenge 1.2.2
    "Let's be sure you're getting this, Cadet! Try this one. Click the screen to start.":
        "확실히 이해했는지 확인해 봅시다, 훈련생! 이걸 시도해 보세요. 화면을 클릭해서 시작하세요.",

    "Cadet, keep in mind we need as many blue crystals as possible to power the devices that heal and help breed our dragons.":
        "훈련생, 우리 용을 치료하고 번식시키는 장치에 동력을 공급하기 위해 가능한 많은 파란 크리스탈이 필요하다는 것을 기억하세요.",

    # Challenge 1.2.3 - 시작
    "Okay, Cadet! Ready for a curveball?":
        "좋아요, 훈련생! 변화구를 맞을 준비가 됐나요?",

    "You don't get to see how your drake looks until you submit your answer!":
        "답을 제출하기 전까지는 드레이크가 어떻게 생겼는지 볼 수 없어요!",

    "Make it through these and you're starting to play in the big leagues!":
        "이것들을 통과하면 메이저리그에서 뛰기 시작하는 거예요!",

    "Is everything a sports analogy with you, Herrera?":
        "에레라, 모든 게 스포츠 비유인가요?",

    "What can I say, Yeung? I'm a team player. Give it a shot.":
        "뭐라고 할까요, 양? 저는 팀 플레이어거든요. 한번 해보세요.",

    "*Sigh* Okay, Cadet. The ball is in your... court. See if you can, uh, hit any home runs...?":
        "*한숨* 좋아요, 훈련생. 공은 당신의... 코트에 있어요. 어, 홈런을 칠 수 있는지 봅시다...?",

    "Yeung shoots! She scores!":
        "양이 슛! 득점입니다!",

    # Challenge 1.2.3 - 성공
    "Okay, Cadet— One more time. Click that screen and... cross the finish line!":
        "좋아요, 훈련생 — 한 번 더. 화면을 클릭하고... 결승선을 통과하세요!",

    "Go Professor Yeung, you are positively on fire!":
        "양 교수님 화이팅, 정말 불타오르고 있어요!",

    # Challenge 1.2.4
    "Mission almost complete... I know you can do this. Click the screen to start.":
        "미션이 거의 끝났어요... 할 수 있다는 걸 알아요. 화면을 클릭해서 시작하세요.",

    "Okay, Cadet. Now let's take a time out!":
        "좋아요, 훈련생. 이제 타임아웃을 가져봅시다!",

    "Another touchdown for Yeung! Ha ha! Except one tiny little thing— we're kind of in a hurry. Just saying.":
        "양의 또 다른 터치다운! 하하! 한 가지 작은 문제만 빼면요 — 우리 좀 급해요. 그냥 말하는 거예요.",
}


def translate_text(text):
    """텍스트를 번역합니다. 번역이 없으면 원본을 반환합니다."""
    # 완전 일치 검색
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]

    # 부분 일치나 유사한 패턴 (필요시 추가)
    return text


def translate_dialog_array(dialog_array):
    """대화 배열을 번역합니다."""
    if not dialog_array:
        return dialog_array

    translated = []
    for dialog in dialog_array:
        if isinstance(dialog, dict) and 'text' in dialog:
            translated_dialog = dialog.copy()
            translated_dialog['text'] = translate_text(dialog['text'])
            translated.append(translated_dialog)
        else:
            translated.append(dialog)
    return translated


def translate_dialog_object(dialog_obj):
    """대화 객체를 번역합니다."""
    if not dialog_obj:
        return dialog_obj

    translated = {}
    for key, value in dialog_obj.items():
        if key in ['start', 'middle', 'end']:
            if isinstance(value, list):
                translated[key] = translate_dialog_array(value)
            elif isinstance(value, dict):
                # end는 success/failure를 가질 수 있음
                translated[key] = {}
                for sub_key, sub_value in value.items():
                    translated[key][sub_key] = translate_dialog_array(sub_value)
            else:
                translated[key] = value
        else:
            translated[key] = value
    return translated


def translate_authoring(data):
    """전체 authoring 데이터를 번역합니다."""
    if 'application' not in data:
        return data

    result = {'application': {'levels': []}}

    for level in data['application'].get('levels', []):
        translated_level = {'missions': []}

        for mission in level.get('missions', []):
            translated_mission = mission.copy()

            # Mission dialog 번역
            if 'dialog' in mission:
                translated_mission['dialog'] = translate_dialog_object(mission['dialog'])

            # Challenges 번역
            if 'challenges' in mission:
                translated_challenges = []
                for challenge in mission['challenges']:
                    translated_challenge = challenge.copy()
                    if 'dialog' in challenge:
                        translated_challenge['dialog'] = translate_dialog_object(challenge['dialog'])
                    translated_challenges.append(translated_challenge)
                translated_mission['challenges'] = translated_challenges

            translated_level['missions'].append(translated_mission)

        result['application']['levels'].append(translated_level)

    return result


def main():
    input_file = 'src/resources/authoring/gv-1.json'
    output_file = 'src/resources/authoring/gv-1-ko.json'

    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Translating...")
    translated_data = translate_authoring(data)

    print(f"Writing {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

    print(f"✓ 번역 완료! {len(TRANSLATIONS)}개의 문자열이 번역되었습니다.")
    print(f"  번역된 파일: {output_file}")


if __name__ == '__main__':
    main()
