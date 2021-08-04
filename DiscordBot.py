# -*- coding: Shift-JIS -*-

# Testing
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

	# ���b�Z�[�W���R�}���h���ǂ����𔻒�
    if not(message.content[0] == '/' or message.content[0] == '�^'):
        return

	#�R�����g�A�E�g�ƃR�}���h�̎d����
    commentPosition=re.search(r'((//)|(�^�^)).*(\n)?',message.content)

    #print(commentPosition)
    commandString=''
    commentString=''

    if commentPosition != None:
        commandString = message.content[:commentPosition.start()]
        if '\n' in commentPosition.group():
            commentString = message.content[commentPosition.start():commentPosition.end() -1]
            commandString = commandString + message.content[commentPosition.end() -1:]
        else:
            commentString = message.content[commentPosition.start():commentPosition.end()]
		#�R�����g�̐��`
        commentString = commentString.replace('�^', '/')
    else:
        commandString = message.content

    print(commandString)
    print(commentString)

    commandList = makeCommandList(commandString)


	#�R�}���h�̔���
    
    reply=''

	#�_�C�X���[��
    if commandList[0] == '/r':
		#�\���`�F�b�N

		#����(�b��I�ɑO�o�[�W�����̗��p)(�A���S���Y�����l����K�v����)
        if '-r' in commandList:
            for num in range(commandList[5]):
                reply = reply+oneDice([commandList[2], commandList[4]])
                if num != commandList[5]:
                    reply = reply + ', '
        else:
            reply = oneDice([commandList[1], commandList[3]])

        reply = f'{message.content}: ' + reply + commentString

	#�L�����N�^�[�N���G�C�g
    elif commandList[0] == '/m':
		#�\���`�F�b�N

		#����(�b��I�ɑO�o�[�W�����̗��p)(�A���S���Y�����l����K�v����)
        if '-a' in commandList:
            ablilityNumList = CoCDiceRole()
        else:
            ablilityNumList = CoCCompileText(commandList)

        PCSheet = CoCCreatePCSheet(ablilityNumList)
        reply = commentString + "\n" + PCSheet

	#Bot�̔����̍폜
    elif commandList[0] == '/delete':
		#�\���`�F�b�N

		#����(�b��I�ɑO�o�[�W�����̗��p)(�A���S���Y�����l����K�v����)
        targetMessage = await message.channel.fetch_message(123)
        await targetMessage.delete()#���b�Z�[�W�̍폜
        return

	#�˂�
    elif commandList[0] == '/neko?':
        reply = "�˂�����Ȃ��ɂ�I"

	#�˂�
    elif commandList[0] == '/neko?':
        reply = "�ɂ�H"

    #�e�X�g�p�R�}���h
    elif commandList[0] == '/test':
        print("test")

	#�G���[
    else:
        reply = "Error: Command not found"

	#�f�B�X�R�[�h�ɑ��M
    await message.channel.send(f'{message.author.mention} ' + reply)

def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

#������̃R�}���h�����X�g�ɕ���
def makeCommandList(commandString):
		##�璷���𖳂���
	#�S�p�����𔼊p������
    commandString = commandString.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
	#���ׂď�������
    commandString = commandString.lower()
    #�󔒂̒���
    commandString = ' '.join(commandString.split())
    

	#��傲�ƂɃ��X�g��
	#������ꏊ�ɋ󔒂�}��
    for i in list(range(len(commandString)-1, 0, -1)):
        if re.match(r'([0-9][a-z])|([0-9][\!\=\<\>\-\+])|([a-z][0-9])|([a-z][\!\=\<\>\-\+])|([\!\=\<\>\-\+][0-9])|([\!\=\<\>\+][a-z])', commandString[i - 1]+commandString[i]) != None:
            commandString = commandString[:i] + ' ' + commandString[i:]

    commandList=commandString.split()

    print(commandList)

	#������int/float�^�֕ϊ�
    for i in range(len(commandList)):
        if is_num(commandList[i]):
            commandList[i] = float(commandList[i])
            if commandList[i].is_integer():
                commandList[i] = int(commandList[i])
    
    return commandList

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

def CoCCompileText(commandList):
	abilityNumList=[]

	for i in commandList[1:10]:
		abilityNumList.append(int(re.sub(r"\D", "", i)))

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
