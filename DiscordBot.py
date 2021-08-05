# -*- coding: utf-8 -*-

# Testing
# インストールした discord.py を読み込む
from asyncio.windows_events import NULL
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

        # メッセージがコマンドかどうかを判定
    if not(message.content[0] == '/' or message.content[0] == '／'):
        return

        # コメントアウトとコマンドの仕分け
    commentPosition = re.search(r'((//)|(／／)).*(\n)?', message.content)

    # print(commentPosition)
    commandString = ''
    commentString = ''

    if commentPosition != None:
        commandString = message.content[:commentPosition.start()]
        if '\n' in commentPosition.group():
            commentString = message.content[commentPosition.start():commentPosition.end() - 1]
            commandString = commandString + message.content[commentPosition.end() - 1:]
        else:
            commentString = message.content[commentPosition.start():commentPosition.end()]
            # コメントの整形
        commentString = commentString.replace('／', '/')
    else:
        commandString = message.content

    #print(commandString)
    #print(commentString)

    commandList = makeCommandList(commandString)

    # コマンドの判定

    reply = ''

    # ダイスロール
    if commandList[0] == '/r':
        # 構文チェック
        if re.match(r'/r (-r )?((\d+ d \d+)|(ccb))( (\+|\-) \d+)?( (>=)|(>)|(<=)|(<)|(==)|(!=) \d+)?( \d+)?', ' '.join([str(n) for n in commandList])) == None:
            errorMessage = "/r Command Syntax Error"
            await message.channel.send(f'{message.author.mention} ' + 'Error: ' + errorMessage)
            return

        repeatTimes = 1
        if commandList[1] == '-r' and type(commandList[-1]) == int and type(commandList[-2]) == int:
            diceList = commandList[2:-1]
            repeatTimes = commandList[-1]
        elif commandList[1] == '-r':
            errorMessage = "/r Command Syntax Error"
            await message.channel.send(f'{message.author.mention} ' + 'Error: ' + errorMessage)
            return
        else:
            diceList = commandList[1:-1] + [commandList[-1]]

        ccbFlag = False
        if diceList[0] == 'ccb':
            diceList.pop(0)
            diceList = [1, 'd', 100] + diceList
            ccbFlag = True

        checkFixedNum = [i for i, x in enumerate(diceList) if x == '+' or x == '-']
        if checkFixedNum == []:
            checkFixedNum = -1
        else:
            checkFixedNum = checkFixedNum[0]
        checkJudgeStatus = [i for i, x in enumerate(diceList) if x == '>' or x == '>=' or x == '<' or x == '<=' or x == '==' or x == '!=']
        if checkJudgeStatus == []:
            checkJudgeStatus = -1
        else:
            checkJudgeStatus = checkJudgeStatus[0]

        # 処理
        for num in range(repeatTimes):
            #通常ダイス
            resultDiceList = [random.randint(1, diceList[2]) for i in range(diceList[0])]
            diceSum = sum(resultDiceList)
            #固定値足し引き
            if checkFixedNum != -1:
                if diceList[checkFixedNum] == '-':
                    diceSum = diceSum - diceList[checkFixedNum + 1]
                elif diceList[checkFixedNum] == '+':
                    diceSum = diceSum + diceList[checkFixedNum + 1]
            #成功判定
            if checkJudgeStatus != -1:
                if diceList[checkJudgeStatus] == '>':
                    resultStatus = str(diceSum > diceList[checkJudgeStatus + 1])
                elif diceList[checkJudgeStatus] == '>=':
                    resultStatus = str(diceSum >= diceList[checkJudgeStatus + 1])
                elif diceList[checkJudgeStatus] == '<':
                    resultStatus = str(diceSum < diceList[checkJudgeStatus + 1])
                    if ccbFlag and diceSum < diceList[checkJudgeStatus + 1] / 5:
                        resultStatus = 'Special'
                elif diceList[checkJudgeStatus] == '<=':
                    resultStatus = str(diceSum <= diceList[checkJudgeStatus + 1])
                    if ccbFlag and diceSum < diceList[checkJudgeStatus + 1] / 5:
                        resultStatus = 'Special'
                elif diceList[checkJudgeStatus] == '==':
                    resultStatus = str(diceSum == diceList[checkJudgeStatus + 1])
                elif diceList[checkJudgeStatus] == '!=':
                    resultStatus = str(diceSum != diceList[checkJudgeStatus + 1])
                if ccbFlag and diceSum > 96:
                    resultStatus = resultStatus + '/Fumble!'
                elif ccbFlag and diceSum <= 5:
                    resultStatus = resultStatus + '/Critical!'
            #文字列整形
            reply = reply + '(' + str(resultDiceList[0])
            for i in range(len(resultDiceList)-1):
                reply = reply + '+' + str(resultDiceList[i + 1])
            reply = reply + ')'

            if checkFixedNum != -1:
                reply = reply + diceList[3] + str(diceList[4])

            reply = reply + ' = ' + str(diceSum)

            if checkJudgeStatus != -1:
                reply = reply + " -> " + resultStatus

            reply = reply + ', '

        reply = commandString + ' : ' + reply + commentString

        # キャラクタークリエイト
    elif commandList[0] == '/m':
        # 構文チェック
        if commandList[1] == '-a' and len(commandList) != 2:
            errorMessage = "/m Command Syntax Error"
            await message.channel.send(f'{message.author.mention} ' + 'Error: ' + errorMessage)
            return

        # 処理(暫定的に前バージョンの流用)(アルゴリズムを考える必要あり)
        if '-a' in commandList:
            ablilityNumList = CoCDiceRole()
        else:
            ablilityNumList = CoCCompileText(commandList)

        PCSheet = CoCCreatePCSheet(ablilityNumList)
        reply = commentString + "\n" + PCSheet

        # Botの発言の削除
    elif commandList[0] == '/d':
        # 構文チェック
        if commandList[1] != 4593:
            errorMessage = "/d Wrong Pass"
            await message.channel.send(f'{message.author.mention} ' + 'Error: ' + errorMessage)
            return

        # 処理(暫定的に前バージョンの流用)(アルゴリズムを考える必要あり)
        targetMessage = await message.channel.fetch_message(commandList[2])
        await targetMessage.delete()  # メッセージの削除
        return

        # ねこ
    elif commandList[0] == '/neko?':
        reply = "ねこじゃないにゃ！"

        # ねこ
    elif commandList[0] == '/neko?':
        reply = "にゃ？"

    # テスト用コマンド
    elif commandList[0] == '/test':
        print("test")

        # エラー
    else:
        errorMessage = "Command not found"
        await message.channel.send(f'{message.author.mention} ' + 'Error: ' + errorMessage)
        return

        # ディスコードに送信
    await message.channel.send(f'{message.author.mention} ' + reply)


def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

# 文字列のコマンドをリストに分割
def makeCommandList(commandString):
    # 冗長性を無くす
    # 全角文字を半角文字に
    commandString = commandString.translate(str.maketrans(
        {chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    # すべて小文字に
    commandString = commandString.lower()
    # 空白の調整
    commandString = ' '.join(commandString.split())

    # 語句ごとにリスト化
    # 分ける場所に空白を挿入
    for i in list(range(len(commandString)-1, 0, -1)):
        if re.match(r'([0-9][a-z])|([0-9][\!\=\<\>\-\+])|([a-z][0-9])|([a-z][\!\=\<\>\-\+])|([\!\=\<\>\-\+][0-9])|([\!\=\<\>\+][a-z])', commandString[i - 1]+commandString[i]) != None:
            commandString = commandString[:i] + ' ' + commandString[i:]

    commandList = commandString.split()

    # 数字をint/float型へ変換
    for i in range(len(commandList)):
        if is_num(commandList[i]):
            if '.' in commandList[i]:
                commandList[i] = float(commandList[i])
            else:
                commandList[i] = int(commandList[i])

    return commandList

def CoCDiceRole():
    # [STR,CON,POW,DEX,APP,SIZ,INT,EDU,年収・財産(ダイス目)]
    abilityNumList = []

    incomeList = [0, 0, 150, 200, 250, 300, 350, 400, 450,
                  500, 600, 700, 800, 900, 1000, 2000, 3000, 5000]

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

    return abilityNumList


def CoCCompileText(commandList):
    abilityNumList = []

    for i in commandList[1:10]:
        abilityNumList.append(int(re.sub(r"\D", "", i)))

    abilityNumList = CoCDamageBonusCal(abilityNumList)

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
    PCSheet = "名前入力欄(ふり仮名)性別:　職業:　年齢:　PL:\nSTR:"\
        + str(ablilityNumList[0]) + "  DEX:" + str(ablilityNumList[3]) + "  INT:" + str(ablilityNumList[6]) + "  アイデア:" + str(ablilityNumList[6]*5) + "\n"\
        + "CON:" + str(ablilityNumList[1]) + "  APP:" + str(ablilityNumList[4]) + "  POW:" + str(ablilityNumList[2]) + "  幸運:" + str(ablilityNumList[2]*5) + "\n"\
        + "SIZ:" + str(ablilityNumList[5]) + "  SAN:" + str(ablilityNumList[2]*5) + "  EDU:" + str(ablilityNumList[7]) + "  知識:" + str(ablilityNumList[7]*5) + "\n"\
        + "HP:" + str(-(-(ablilityNumList[1] + ablilityNumList[5]) // 2)) + "  MP:" + str(ablilityNumList[2]) + "  回避:" + str(ablilityNumList[3] * 2) + "  ﾀﾞﾒｰｼﾞﾎﾞｰﾅｽ:" + ablilityNumList[9] + "\n"\
        + "――――――――――――――――――――――――――\n[技能](職業技能点:" + str(ablilityNumList[7] * 20) + "  個人技能点:" + str(ablilityNumList[6] * 10) + ")" + "\n"\
        + "[職業技能]\n技能名:％(+)  技能名:％(+)  技能名:％(+)\n技能名:％(+)  技能名:％(+)  技能名:％(+)\n"\
        + "[職業選択技能]\n技能名:％(+)  技能名:％(+)  技能名:％(+)\n[個人技能]\n技能名:％(+)  技能名:％(+)  技能名:％(+)\n――――――――――――――――――――――――――\n"\
        + "[持ち物]\n・武器\n[――――――――ここに記入――――――――]\n・防具\n[――――――――ここに記入――――――――]\n・所持品\n[――――――――ここに記入――――――――]\n\n"\
        + "特記:\n\n[プロフィール]\n\n年収:" + \
        str(ablilityNumList[8]) + "万、財産:" + str(ablilityNumList[8] * 5) + "万"

    return PCSheet


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
