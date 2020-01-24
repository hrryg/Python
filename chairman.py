import discord
import sqlite3
import random
import time
TOKEN = 'NjcwMjEwOTA3MjI5NjUwOTU1.XisTjA.D5FacukmQ1SBvntnKjwAaweBhJ4'
client = discord.Client()

@client.event
async def on_ready():
    print('started')

@client.event
async def on_connect():

    #DB
    conn = sqlite3.connect('odai.sqlite3')
    c = conn.cursor()
    c.execute('create table if not exists IG(id integer, name text)')
    conn.commit()
    conn.close()

    channel = client.get_channel(664847464960098304)
    #接続時メッセージ
    await channel.send('どうも、チェアマン松本です')


@client.event
async def on_message(message):
    conn = sqlite3.connect('odai.sqlite3')
    c = conn.cursor()
    c.execute('create table if not exists IG(id integer, name text)')
    conn.commit()

    #送信者がBOTの場合return
    if message.author.bot:
        return
    msg = message.content.split()

    #コマンド受け取り
    if msg[0] == '!ippon':
        if len(msg) < 2:
            await message.channel.send('**IPPON GRANDPRIX**')
        elif msg[1] == 'help':
            await message.channel.send('**!ippon add <お題>**  お題を追加します。\n**!ippon start**  大喜利を開始します。\n**!ippon list <page>**  登録されているお題を10件ずつ表示します。\n**!ippon remove <num>**  指定したお題を削除します。')
        elif msg[1] == 'add':
            if len(msg) < 3:
                await message.channel.send('追加するお題を入力してください。')
            else:
                odai = msg[2]
                await message.channel.send('お題**『%s』**を追加しました。' % odai)
                c.execute('select count(id) from IG')
                cnt = c.fetchall()[0][0]
                c.execute('insert into IG values (?,?)', (cnt,odai))
                conn.commit()
        elif msg[1] == 'start':
            c.execute('select count(id) from IG')
            cnt = c.fetchall()[0][0]
            rnd = random.randint(0, cnt-1)
            c.execute('select name from IG where id = (?)', (str(rnd)))
            odai = c.fetchall()[0]
            await message.channel.send('**『%s』**' % odai)
        elif msg[1] == 'list':
            page = (int(msg[2])-1)*10
            num = int(msg[2])
            c.execute('select count(id) from IG')
            cnt = c.fetchall()[0][0]
            list = '**'
            if page < cnt and page >= 0:
                for x in range(10):
                    if page+x>=cnt:
                        break
                    c.execute('select name from IG where id = (?)', (str(page+x),))
                    odai = c.fetchall()[0][0]
                    list += f'{page+x+1} {odai}\n'
                await message.channel.send('%s**\n -%dページ目' % (list,num))
            else:
                await message.channel.send('正しいページ数を入力してください。')
        elif msg[1] == 'remove':
            page = int(msg[2])
            c.execute('select count(id) from IG')
            cnt = c.fetchall()[0][0]
            c.execute('select name from IG where id = (?)', (str(page-1),))
            odai = c.fetchall()[0][0]
            await message.channel.send('**『%s』**を削除しました。' % odai)
            c.execute('delete from IG where id = (?)', str(page-1))
            for x in range(page,cnt):
                c.execute('update IG set id = (?) where id = (?)',(str(x-1),str(x)))
            conn.commit()

client.run(TOKEN)
