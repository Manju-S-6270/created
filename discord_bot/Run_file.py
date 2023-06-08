import discord
import discord.app_commands
import re
import requests
import sympy
import csv


client = discord.Client(intents=discord.Intents.all())
TAKEN = "[トークンは見せられません]"
ROLE_MESSAGE_ID = 1064822508580245554 #ロール付与用メッセージID
ROLE_ID = 1064826018013122681 #ロール付与用ロールID
 
RETURN_CHANNEL_ID = 1064818485793927198 #オウム返し用チャンネルID

MATH_CHANNEL_ID = 1072438819909029928 #四則演算用チャンネルID
CHTH_CHANNEL_ID = 1074967489613668362 #方程式用チャンネルID
x = sympy.Symbol('x') #方程式用 "x" の宣言

async def get_uuid_username(num):
    url = f"https://auth.aristois.net/token/{num}" #URLの定義
    response = requests.get(url).json() #URLに向けて送信
    uuid = response["uuid"] #UUIDを受け取る
    username = response["username"] #ユーザーネームを受け取る
    return uuid, username

def get_onready():
    GUILD_ID = 830028839564083232 #接続完了通知用 ギルドID
    ORADY_ID = 1069895289827246111 #接続完了通知用 チャンネルID
    guild_onready = client.get_guild(GUILD_ID) #接続完了通知用 ギルド
    channel_onready = guild_onready.get_channel(ORADY_ID) #接続完了通知用 チャンネル
    return channel_onready #チャンネル情報を返す

def mcsaveuser(UUID,MCID,DSID):
    with open('save.csv', mode='a', newline='') as csvfile:
        uuid_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        uuid_writer.writerow([DSID, UUID, MCID])


GLOBAL_CHANNEL_NM = "gchatongt" #現在未使用

@client.event
async def on_ready(): #サーバーとの接続時に実行する
    print("on_ready") #クライアント上に"on_ready"と表示させる
    print(discord.__version__) #クライアント上にバージョン情報を表示させる
    sendfor = get_onready() #get_onreadyの戻り値をsendforに入れる
    await sendfor.send("Bot \"Greatest Tester\" is online.") #接続完了通知
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Waiting for input..."))


@client.event
async def on_message(message): #メッセージが来た時
    if not message.author.bot: #メッセージの送信者がBotじゃない時
        if message.content == "/shutdown": #内容が"Shutdown"だった時 -- Shutdownコマンド
            sendfor = get_onready() ##get_onreadyの戻り値をsendforに入れる
            await sendfor.send("Bot \"Greatest Tester\" is offline.") #接続解除通知
            await client.close() #サーバーとの通信を切る
            return
        
        if message.channel.id == RETURN_CHANNEL_ID: #送信された場所が"オウム返し"だった時(ID指定) -- オウム返し
            await message.channel.send(message.content) #オウム返す
            print(message.content) #上の内容をクライアントに表示させる
        
        if message.channel.id == MATH_CHANNEL_ID: #送信された場所が"math"だった時(ID指定) -- 四則演算
            if re.match("^[0-9\+\-\*\/\(\)\.]+$", message.content): #送信されたメッセージの先頭が数字に関することだった時
                result = eval(message.content) #計算する
                await message.author.send("Result: " + str(result)) #計算結果を送信した人にDMで送信する
                print(message.content, "=", result) #計算結果をクライアントに表示する
        
        if message.channel.id == CHTH_CHANNEL_ID: #送信された場所が"char_math"だった時(ID指定) -- 方程式
            sol = sympy.solve(message.content,x) #計算する
            await message.author.send("Result: " + str(sol)) #計算結果を送信した人にDMで送信する
            print(message.content, "=", sol) #計算結果をクライアントに表示する
        
        if message.channel.type == discord.ChannelType.private: #送信された場所がDMだった時 -- ID登録
            if len(message.content) == 6 and message.content.isnumeric(): #送信されたメッセージが番号で、6桁だった場合
                uuid, username = await get_uuid_username(message.content) #UUID,USERNAMEを受け取る
                mcsaveuser(uuid,username,message.author.id)
                Guild = client.get_guild(830028839564083232)
                Member = Guild.get_member(message.author.id)
                await Member.edit(nick=username)
                await message.channel.send(f"[あなたはログインしました]\n以下の内容で登録しました。\nMinecraft UUID: {uuid}\nMinecraft Username: {username}\n紐づけ先Discordユーザー: {message.author.name}")
                print(f"UUID: {uuid}\nUsername: {username} has been registered by Discord User: {message.author.name} via DM")
                
                embedlist = discord.embed(color=discord.Colour.green, title="Minecraft register service", type='rich', url=None, description="次の通り、登録されました。", timestamp="")
                embedlist.add_field("登録されたMinecraftアカウント名", {username}, inline=True)
                
        
                
            
                

@client.event
async def on_raw_reaction_add(payload): #リアクションが追加されたとき -- ロール付与
    if payload.message_id == ROLE_MESSAGE_ID: #指定されたメッセージだった時
        Guild = client.get_guild(payload.guild_id) #ギルドを取得する
        Roles = Guild.get_role(ROLE_ID) #ロールを取得する
        await payload.member.add_roles(Roles, reason="Reaction Role", atomic=True) #ロールを付与する


client.run(TAKEN,reconnect=True)
