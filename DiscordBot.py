# -*- coding: Shift-JIS -*-

# インストールした discord.py を読み込む
import discord
import re
import random

# 自分のBotのアクセストークンに置き換えてください
f = open('TokenID.txt', 'r')
TOKEN = f.read()
f.close()

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if '/r' in message.content:
        patternA = '/r (\d+)d(\d+)'
        patternB = '/r (repeat)\((\d+)d(\d+)\,(\d+)\)'

        if re.match(patternA,message.content):
            diceNumber = replaceNumber(message.content)
            reply = f'{message.author.mention} : {message.content}= ' + oneDice(diceNumber)
        elif re.match(patternB,message.content):
            diceNumber=replaceNumber(message.content)
            reply = f'{message.author.mention} : {message.content}= '
            for num in range(diceNumber[2] - 1):
                reply = reply+oneDice(diceNumber)
                if num != diceNumber[2]:
                    reply = reply + ', '
        else:
            reply = f'{message.author.mention} : {message.content} is error'
        await message.channel.send(reply)

    if '/PCM' in message.content:
        patternA = '/PCM_auto'
        patternB = '/PCM_B.*'
        
        if re.match(patternA,message.content):
            ablilityNumList = CoCDiceRole()
        elif re.match(patternB,message.content):
            ablilityNumList = CoCCompileText(message.content)

        PCSheet = CoCCreatePCSheet(ablilityNumList)

        reply = f'{message.author.mention}'+ "\n" + PCSheet
        await message.channel.send(reply)

    if '/neko?' in message.content:
        reply = f'{message.author.mention}'+ "ねこじゃないにゃ！"
        await message.channel.send(reply)

    elif '/neko' in message.content:
        reply = f'{message.author.mention}'+ "にゃ？"
        await message.channel.send(reply)

def oneDice(diceNumber):
    reply = '('
    diceAll = 0
    for num in range(diceNumber[0]):
        diceResult = random.randrange(1, diceNumber[1] + 1)
        reply = reply + str(diceResult)
        if num != diceNumber[0] - 1:
            reply = reply + '+'
        diceAll += diceResult
    reply = reply + ') = ' + str(diceAll)
    return reply

def replaceNumber(message):
    messageString = str(message)
    messageString = messageString.replace('/r','').replace('repeat(','').replace(')','')
    messageString = messageString.replace('d',',')
    numList = [int(x.strip()) for x in messageString.split(',')]
    return numList

def CoCDiceRole():
	#[STR,CON,POW,DEX,APP,SIZ,INT,EDU,年収・財産(ダイス目)]
	abilityNumList=[]

	incomeList=[0,0,150,200,250,300,350,400,450,500,600,700,800,900,1000,2000,3000,5000]

	for i in range(5):
		abillityNum = 0
		for num in range(3):
		    abillityNum += random.randrange(1, 6 + 1)
		abilityNumList.append(abillityNum)

	for i in range(2):
		abillityNum = 0
		for num in range(2):
		    abillityNum += random.randrange(1, 6 + 1)
		abilityNumList.append(abillityNum + 6)
	
	abillityNum = 0
	for num in range(3):
		abillityNum += random.randrange(1, 6 + 1)
	abilityNumList.append(abillityNum + 3)

	abillityNum = 0
	for num in range(3):
		abillityNum += random.randrange(1, 6 + 1)
	abilityNumList.append(incomeList[abillityNum - 1])
	
	abilityNumList = CoCDamageBonusCal(abilityNumList)

	print(abilityNumList)

	return abilityNumList

def CoCCompileText(text):
	abilityNumList=[]

	result = re.findall(r"\d+", text)

	for i in range(8):
		abilityNumList.append(int(result[i]))

	abilityNumList.append(int(result[8]))

	abilityNumList = CoCDamageBonusCal(abilityNumList)

	print(abilityNumList)

	return abilityNumList

def CoCDamageBonusCal(abilityNumList):
	checkNum = abilityNumList[0] + abilityNumList[5]
	if 2 <= checkNum and checkNum <= 12:
		abilityNumList.append("-1D6")
	elif 13 <= checkNum and checkNum <= 16:
		abilityNumList.append("-1D4")
	elif 17 <= checkNum and checkNum <= 24:
		abilityNumList.append("0")
	elif 25 <= checkNum and checkNum <= 32:
		abilityNumList.append("+1D4")
	elif 33 <= checkNum and checkNum <= 40:
		abilityNumList.append("+1D6")
	elif 41 <= checkNum and checkNum <= 56:
		abilityNumList.append("+2D6")
	elif 57 <= checkNum and checkNum <= 72:
		abilityNumList.append("+3D6")
	elif 73 <= checkNum and checkNum <= 88:
		abilityNumList.append("+4D6")
	elif 89 <= checkNum and checkNum <= 104:
		abilityNumList.append("+5D6")
	else:
		abilityNumList.append("表参照")

	return abilityNumList

def CoCCreatePCSheet(ablilityNumList):
	PCSheet="名前入力欄(ふり仮名)性別:　職業:　年齢:　PL:\nSTR:"\
	   + str(ablilityNumList[0]) + "  DEX:" +  str(ablilityNumList[3]) + "  INT:" +  str(ablilityNumList[6]) + "  アイデア:" +  str(ablilityNumList[6]*5) + "\n"\
	   + "CON:" + str(ablilityNumList[1]) + "  APP:" +  str(ablilityNumList[4]) + "  POW:" +  str(ablilityNumList[2]) + "  幸運:" +  str(ablilityNumList[2]*5) + "\n"\
	   + "SIZ:" + str(ablilityNumList[5]) + "  SAN:" +  str(ablilityNumList[2]*5) + "  EDU:" +  str(ablilityNumList[7]) + "  知識:" +  str(ablilityNumList[7]*5) + "\n"\
	   + "HP:" + str(-(-(ablilityNumList[1] + ablilityNumList[5]) // 2)) + "  MP:" +  str(ablilityNumList[2]) + "  回避:" +  str(ablilityNumList[3] * 2) + "  ﾀﾞﾒｰｼﾞﾎﾞｰﾅｽ:" + ablilityNumList[9] + "\n"\
	   + "――――――――――――――――――――――――――\n[技能](職業技能点:" + str(ablilityNumList[7] * 20) + "  個人技能点:" + str(ablilityNumList[6] * 10) + ")" + "\n"\
	   + "[職業技能]\n技能名:％(+)  技能名:％(+)  技能名:％(+)\n技能名:％(+)  技能名:％(+)  技能名:％(+)\n"\
	   + "[職業選択技能]\n技能名:％(+)  技能名:％(+)  技能名:％(+)\n[個人技能]\n技能名:％(+)  技能名:％(+)  技能名:％(+)\n――――――――――――――――――――――――――\n"\
	   + "[持ち物]\n・武器\n[――――――――ここに記入――――――――]\n・防具\n[――――――――ここに記入――――――――]\n・所持品\n[――――――――ここに記入――――――――]\n\n"\
	   + "特記:\n\n[プロフィール]\n\n年収:" + str(ablilityNumList[8]) + "万、財産:" + str(ablilityNumList[8] * 5) + "万"
	print(PCSheet)

	return PCSheet


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)