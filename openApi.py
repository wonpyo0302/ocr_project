from openai import OpenAI
import os
client = OpenAI(
    api_key= os.environ["OPENAI_API_KEY"]
)

def responseChatFnc(userQuestion, language):
    if language == "en":
        messages = [
            {"role":"system","content":"You are a helpful assistant in the summary"},
            {"role": "user", "content": f"Summarize the following. \n {userQuestion}"}
        ]
    elif language == "ko":
        messages = [
            {"role":"system","content":"You are a helpful assistant in the summary"},
            {"role": "user", "content": f"다음의 내용을 한국어로 요약해줘. \n {userQuestion}"}
        ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= messages,
        max_tokens=4000,
        temperature=0.8,
        n=1
    )

    return response.choices[0].message.content

strKo = '선거 장면을 설정하기 위한 예산'
strKo +='고든 브라운은 그리니치 표준시 12시 30분에 9번째 예산안을 발표할 때, 노동당의 3선 연임 도전의 중심에 경제를 놓으려고 할 것입니다. 그는 낮은 실업률과 이자율과 함께 지속적인 경제 안정의 중요성을 강조할 것으로 예상됩니다. 고든 브라운 총리는 휘발유세를 동결하고 인지세 기준을 ?귥쭥 6만에서 인상할 것으로 예상됩니다. 그러나 보수당과 자유민주당은 유권자들이 노동당 정권하에서 더 높은 세금과 더 많은 수단 시험에 직면해야 한다고 주장합니다.'
strKo += '재무부 관리들은 선거를 앞두고 기부금을 지급하지는 않을 것이라고 말했으나 브라운 총리는 20억 파운드의 여유가 있는 것으로 알려졌습니다.'
strKo +='- 스탬프 관세 임계값이 ?귥쭥60,000에서 증가합니다'
strKo +='- 휘발유 관세 동결'
strKo +='- 빈곤가정에 대한 세액공제 제도의 연장'
strKo +='- 연금 수령자를 위한 가능한 도움 인지세의 문턱을 높이는 것은 처음 구매하는 사람들을 돕기 위한 것인데, 이것은 아마도 세 주요 정당들의 총선 선언문의 주제일 것입니다. 10년 전, 구매자들은 잉글랜드와 웨일즈에서만 거의 50만 개의 부동산이 있어 인지세를 피할 수 있는 훨씬 더 큰 기회가 있었는데, 이것은 ?귥쭥 60,000 미만에 팔렸습니다. 그 이후로, 영국의 평균 부동산 가격은 두 배 이상 올랐고, 인지세의 시작 문턱은 높아지지 않았습니다. 세금 공제 결과, 인지세가 발생하는 부동산의 수는 정부의 세금 징수와 함께 급증했습니다. 자민당은 2월에 인지세 문턱을 ?귥쭥 150,000으로 높이려는 그들 자신의 제안을 발표했습니다.'
strKo +='보수당은 또한 올리버 레트윈 그림자 총리가 인지세를 "고전적인 노동당 스텔스세"로 상표를 붙이면서 문턱을 높이는 방안을 제안할 것으로 보입니다. 보수당은 만약 노동당이 정권을 되찾는다면, 총리가 주는 것은 무엇이든 높은 세금으로 환수될 것이라고 말합니다. 그림자 재무장관 조지 오스본은 "현재 영국 경제를 보는 모든 사람들은 공공 재정이 급격히 악화되었다고 말하고, 블랙홀이 있다고 말합니다"라고 말했습니다. "만약 노동당이 당선된다면, 선거 후 예산에서 대략 귥쭥 100억 파운드 정도의 매우 상당한 세금 인상이 있을 것입니다."'
strKo +='그러나 현재 의회의 희망자인 브라운의 전 고문 에드 볼스는 경제에 대한 토리의 계획을 조사한 결과 두 주요 정당 사이에 다음 의회 말까지 투자에 350억 파운드의 귥쭥 차이가 있을 것이라고 말했습니다. 그는 "저는 우리가 지출 약속을 이행하기 위해 시작한 계획에 어떤 변화도 필요하다는 것을 받아들이지 않습니다"라고 덧붙였습니다'
strKo +='자유민주당의 데이비드 로즈 의원은 "총리는 의심할 여지 없이 오늘 우리에게 경제가 얼마나 훌륭하게 돌아가고 있는지 말해줄 것"이라고 말했습니다. "하지만 그 많은 것들이 지난 몇 년간 개인 및 소비자 부채의 증가에 기반을 두고 있는데, 이는 금리가 상당한 방식으로 올라가야 한다면 잠재적으로 경제를 상당히 취약하게 만듭니다." 사회당의 알렉스 샐먼드 대표는 자신의 당이 최초 구매자들에게 귥쭥 2,000 보조금을 도입하고 법인세를 감면하며 수단 테스트에서 자유로운 시민 연금을 도입할 것이라고 말했습니다.'

print("ko요약본 : {}".format(responseChatFnc(strKo,language="ko")))
print("\n")

strEn = 'Budget to set scene for election'
strEn +='Gordon Brown will seek to put the economy at the centre of Labour\'s bid for a third term in power when he delivers his ninth Budget at 1230 GMT. He is expected to strKoess the importance of continued economic stability, with low unemployment and interest rates. The chancellor is expected to freeze petrol duty and raise the stamp duty threshold from ?귥쭥60,000. But the Conservatives and Lib Dems insist voters face higher taxes and more means-testing under Labour.'
strEn +='Treasury officials have said there will not be a pre-election giveaway, but Mr Brown is thought to have about ?귥쭥2bn to spare.'
strEn +='- Increase in the stamp duty threshold from ?귥쭥60,000 '
strEn +='- A freeze on petrol duty '
strEn +='- An extension of tax credit scheme for poorer families '
strEn +='- Possible help for pensioners The stamp duty threshold rise is intended to help first time buyers - a likely theme of all three of the main parties general election manifestos. Ten years ago, buyers had a much greater chance of avoiding stamp duty, with close to half a million properties, in England and Wales alone, selling for less than ?귥쭥60,000. Since then, average UK property prices have more than doubled while the starting threshold for stamp duty has not increased. Tax credits As a result, the number of properties incurring stamp duty has rocketed as has the government\'s tax take. The Liberal Democrats unveiled their own proposals to raise the stamp duty threshold to ?귥쭥150,000 in February.'
strEn +='The Tories are also thought likely to propose increased thresholds, with shadow chancellor Oliver Letwin branding stamp duty a "classic Labour stealth tax". The Tories say whatever the chancellor gives away will be clawed back in higher taxes if Labour is returned to power. Shadow Treasury chief secretary George Osborne said: "Everyone who looks at the British economy at the moment says there has been a sharp deterioration in the public finances, that there is a black hole," he said. "If Labour is elected there will be a very substantial tax increase in the Budget after the election, of the order of around ?귥쭥10bn."'
strEn +='But Mr Brown\'s former advisor Ed Balls, now a parliamentary hopeful, said an examination of Tory plans for the economy showed there would be a ?귥쭥35bn difference in investment by the end of the next parliament between the two main parties. He added: "I don\'t accept there is any need for any changes to the plans we have set out to meet our spending commitments."'
strEn +='For the Lib Dems David Laws said: "The chancellor will no doubt tell us today how wonderfully the economy is doing," he said. "But a lot of that is built on an increase in personal and consumer debt over the last few years - that makes the economy quite vulnerable potentially if interest rates ever do have to go up in a significant way." SNP leader Alex Salmond said his party would introduce a ?귥쭥2,000 grant for first time buyers, reduce corporation tax and introduce a citizens pension free from means testing. Plaid Cymru\'s economics spokesman Adam Price said he wanted help to get people on the housing ladder and an increase in the minimum wage to ?귥쭥5.60 an hour.'

print("en요약본 : {}".format(responseChatFnc(strKo,language="en")))
print("\n")
