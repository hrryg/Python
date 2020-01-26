import discord
import sqlite3
import random
import time
TOKEN = 'NjcwMjEwOTA3MjI5NjUwOTU1.Xi2XFg.bbTw1CtVzngo5lYExGqIXl4FRZI'
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
    c.execute('create table if not exists option(r integer, p interger)')
    c.execute('select count(r) from option')
    cnt = c.fetchall()[0][0]
    if cnt == 0:
        c.execute('insert into option values (30,10)')
    c.execute('create table if not exists ans(name text, num integer)')
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
            h = '**!ippon add <お題>**  お題を追加します。\n'
            h +='**!ippon start**  IPPON GRANDPRIXを開始します。\n'
            h +='**!ippon list <page>**  登録されているお題を10件ずつ表示します。\n'
            h +='**!ippon remove <num>**  指定したお題を削除します。\n'
            h +='**!ippon option**  現在の設定を確認します。\n'
            h +='**!ippon range <num>**  登録できるお題の文字数を設定します。\n'
            h +='**!ippon point <num>**  IPPON獲得ポイントを設定します。\n'
            await message.channel.send('%s' % h)
        elif msg[1] == 'add':
            if len(msg) < 3:
                await message.channel.send('追加するお題を入力してください。')
            else:
                c.execute('select r from option')
                r = c.fetchall()[0][0]
                odai = msg[2]
                if len(odai) <= r:
                    await message.channel.send('お題**『%s』**を追加しました。' % odai)
                    c.execute('select count(id) from IG')
                    cnt = c.fetchall()[0][0]
                    c.execute('insert into IG values (?,?)', (cnt,odai))
                    conn.commit()
                else:
                    await message.channel.send('お題は**%d文字**以内で入力してください。' % r)
        elif msg[1] == 'start':
            c.execute('select count(id) from IG')
            cnt = c.fetchall()[0][0]
            rnd = random.randint(0, cnt-1)
            c.execute('select name from IG where id = (?)', (str(rnd)))
            odai = c.fetchall()[0]
            await message.channel.send('**『%s』**' % odai)
        elif msg[1] == 'list':
            if len(msg) < 3:
                await message.channel.send('ページ数を入力してください。')
            elif not msg[2].isdecimal():
                await message.channel.send('整数を入力してください。')
            else:
                page = (int(msg[2])-1)*10
                num = int(msg[2])
                c.execute('select count(id) from IG')
                cnt = c.fetchall()[0][0]
                list = '**'
                if page < cnt and page >= 0:
                    for x in range(10):
                        if page+x>=cnt:
                            break
                        c.execute('select name from IG where id = (?)', (str(page+ x),))
                        odai = c.fetchall()[0][0]
                        list += f'{page+x+1} {odai}\n'
                    await message.channel.send('%s**\n -%dページ目' % (list,num))
                else:
                    await message.channel.send('正しいページ数を入力してください。')
        elif msg[1] == 'remove':
            if not msg[2].isdecimal():
                await message.channel.send('整数を入力してください。')
            else:
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
        elif msg[1] == 'range':
            if not msg[2].isdecimal():
                await message.channel.send('整数を入力してください。')
            else:
                r = int(msg[2])
                if r > 0:
                    c.execute('update option set r = (?)',(r,))
                    await message.channel.send('登録可能なお題の文字数を**%d文字**に変更しました。' % r)
                    conn.commit()
                else:
                    await message.channel.send('正の整数を入力してください。')
        elif msg[1] == 'point':
            if not msg[2].isdecimal():
                await message.channel.send('整数を入力してください。')
            else:
                p = int(msg[2])
                if p > 0:
                    c.execute('update option set p = (?)',(p,))
                    await message.channel.send('IPPON獲得ポイントを**%d**に変更しました。' % p)
                    conn.commit()
                else:
                    await message.channel.send('正の整数を入力してください。')
        elif msg[1] == 'option':
            c.execute('select r from option')
            r = c.fetchall()[0][0]
            c.execute('select p from option')
            p = c.fetchall()[0][0]
            await message.channel.send('**登録可能なお題の文字数：%d**\n**IPPON獲得ポイント：%d**' % (r,p))
        else:
            await message.channel.send('**!ippon help** を参照して正しいコマンドを入力してください。')

client.run(TOKEN)
