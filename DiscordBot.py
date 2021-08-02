# -*- coding: Shift-JIS -*-

# �C���X�g�[������ discord.py ��ǂݍ���
import discord
import re
import random

# ������Bot�̃A�N�Z�X�g�[�N���ɒu�������Ă�������
f = open('TokenID.txt', 'r')
TOKEN = f.read()
f.close()

# �ڑ��ɕK�v�ȃI�u�W�F�N�g�𐶐�
client = discord.Client()

# �N�����ɓ��삷�鏈��
@client.event
async def on_ready():
    # �N��������^�[�~�i���Ƀ��O�C���ʒm���\�������
    print('���O�C�����܂���')

# ���b�Z�[�W��M���ɓ��삷�鏈��
@client.event
async def on_message(message):
    # ���b�Z�[�W���M�҂�Bot�������ꍇ�͖�������
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
        reply = f'{message.author.mention}'+ "�˂�����Ȃ��ɂ�I"
        await message.channel.send(reply)

    elif '/neko' in message.content:
        reply = f'{message.author.mention}'+ "�ɂ�H"
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
	#[STR,CON,POW,DEX,APP,SIZ,INT,EDU,�N���E���Y(�_�C�X��)]
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
		abilityNumList.append("�\�Q��")

	return abilityNumList

def CoCCreatePCSheet(ablilityNumList):
	PCSheet="���O���͗�(�ӂ艼��)����:�@�E��:�@�N��:�@PL:\nSTR:"\
	   + str(ablilityNumList[0]) + "  DEX:" +  str(ablilityNumList[3]) + "  INT:" +  str(ablilityNumList[6]) + "  �A�C�f�A:" +  str(ablilityNumList[6]*5) + "\n"\
	   + "CON:" + str(ablilityNumList[1]) + "  APP:" +  str(ablilityNumList[4]) + "  POW:" +  str(ablilityNumList[2]) + "  �K�^:" +  str(ablilityNumList[2]*5) + "\n"\
	   + "SIZ:" + str(ablilityNumList[5]) + "  SAN:" +  str(ablilityNumList[2]*5) + "  EDU:" +  str(ablilityNumList[7]) + "  �m��:" +  str(ablilityNumList[7]*5) + "\n"\
	   + "HP:" + str(-(-(ablilityNumList[1] + ablilityNumList[5]) // 2)) + "  MP:" +  str(ablilityNumList[2]) + "  ���:" +  str(ablilityNumList[3] * 2) + "  ��Ұ���ްŽ:" + ablilityNumList[9] + "\n"\
	   + "�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\\n[�Z�\](�E�ƋZ�\�_:" + str(ablilityNumList[7] * 20) + "  �l�Z�\�_:" + str(ablilityNumList[6] * 10) + ")" + "\n"\
	   + "[�E�ƋZ�\]\n�Z�\��:��(+)  �Z�\��:��(+)  �Z�\��:��(+)\n�Z�\��:��(+)  �Z�\��:��(+)  �Z�\��:��(+)\n"\
	   + "[�E�ƑI���Z�\]\n�Z�\��:��(+)  �Z�\��:��(+)  �Z�\��:��(+)\n[�l�Z�\]\n�Z�\��:��(+)  �Z�\��:��(+)  �Z�\��:��(+)\n�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\\n"\
	   + "[������]\n�E����\n[�\�\�\�\�\�\�\�\�����ɋL���\�\�\�\�\�\�\�\]\n�E�h��\n[�\�\�\�\�\�\�\�\�����ɋL���\�\�\�\�\�\�\�\]\n�E�����i\n[�\�\�\�\�\�\�\�\�����ɋL���\�\�\�\�\�\�\�\]\n\n"\
	   + "���L:\n\n[�v���t�B�[��]\n\n�N��:" + str(ablilityNumList[8]) + "���A���Y:" + str(ablilityNumList[8] * 5) + "��"
	print(PCSheet)

	return PCSheet


# Bot�̋N����Discord�T�[�o�[�ւ̐ڑ�
client.run(TOKEN)