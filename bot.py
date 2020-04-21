import math
import random
import discord
import re
from discord.ext import commands

client = commands.Bot(command_prefix='!')

votes = 0
mutelist = []
citylist = []
text = ' Абакан Азов Александров Алексин Альметьевск Анапа Ангарск \
    Анжеро-Судженск Апатиты Арзамас Армавир Арсеньев Артем Архангельск Асбест \
    Астрахань Ачинск Балакова Балахна Балашиха Балашов Барнаул Батайск Белгород \
    Белебей Белово Белогорск Белорецк Белореченск Бердск Березники Березовский \
    Бийск Биробиджан Благовещенск Бор '


@client.event
async def on_ready():
    print("Connected")
    


@client.command(pass_context=True)
async def hello(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send('Салам Алейкум! Я здесь новенький')


@client.command(pass_context=True)
async def flip(ctx):
    x = round(random.random())
    author = ctx.message.author
    if x == 0:
        await ctx.send(f'{author.mention} Решка')
    else:
        await ctx.send(f'{author.mention} Орел')


@client.command(pass_context=True)
async def fliр(ctx):
    author = ctx.message.author
    await ctx.send(f'{author.mention} Решка')


@client.command(pass_context=True)
async def roll(ctx, max=100, min=1):
    x = round(random.randint(min, max))
    author = ctx.message.author
    await ctx.send(f'{author.mention} Ролл от {min} до {max}: {x}')

#member: discord.Member
@client.command(pass_context=True)
async def city(ctx):
    channel = client.get_channel(702128536076550144)
    if(len(citylist)==0):
        i = ctx.message.content
        author = ctx.message.author
        id = author.id
        role = discord.utils.get(author.guild.roles, name = 'shaharlar')
        citylist.append(id)
        print('add to citylist')
        print('citylsit id:')
        print(citylist)

        await author.add_roles(role)
        await channel.send(f'Погнали {author.mention}')
        
    else:
         await channel.send(f'Занято нафик')


@client.event
async def on_message(message):
    global text
    user = str(message.author.id)
    user1 = int(user)
    user2 = '<@!' + user + '>'
    print('new message')
    print('message user: ' + user)
    #print('message user1: ' + user1)
    channel = client.get_channel(702128536076550144)
    if user2 in mutelist:
        await message.channel.purge(limit=1)
        #await client.delete_message(message)
        print("delete")
    elif user1 in citylist:
        print('check city')
        print(str(message.content))
        print(re.search(f'\\s[{str(message.content)}]\\w+\\s', text, re.IGNORECASE).group(0))
        if(str(message.content) == re.search(str(message.content), text, re.IGNORECASE).group(0)):
            text = re.sub((str)(message.content),' <Этот город уже был> ', text)
            c = (str)(message.content[-1])
            print(c)
            
            result = re.search(f'\\s[{c}]\\w+\\s', text, re.IGNORECASE)
            result = result.group(0)
            print(result)
            if result in text:
                await channel.send(result.strip())
                print('>>> ' + result.strip() ) 
                text = re.sub(result,' <Этот город уже был> ', text)
                await channel.send(text)
            else:
                 await channel.send('>>> Не найдено подходящего города!')
        else:
            await channel.send('>>> Было!')
    else:
        pass

    await client.process_commands(message)


@client.command()
async def mute(ctx, mention):
    m = mention
    mutelist.append(m)
    if(mutelist.count(m)>=3):
        await ctx.send(f'{mention} add to mutelist')
    else:
        await ctx.send(f'{mention} has {mutelist.count(m)} votes')


    print("add")
    print(mutelist)


@client.command()
async def unmute(ctx,mention):
    m = mention
    print(m)
    user = str(ctx.author.id)
    user = '<@!' + user + '>'

    if(m != user ):
        if (mutelist.count(m) >= 2):
            mutelist.remove(m)
            await ctx.send(f'{mention} has {mutelist.count(m)} votes')

            print("remove")
        elif (mutelist.count(m) == 1):
            mutelist.remove(m)
            await ctx.send(f'{mention} has {mutelist.count(m)} votes')
            print("remove")    
        elif(mutelist.count(m) == 0):
            await ctx.send(f'{mention} remove from mutelist')
    elif((m == user)&(mutelist.count(m) >= 0)):
        await ctx.send(f'{mention} ты дурак? Ты в муте :clown:')



@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command(pass_context=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=10)


token = "Njk3NzIyODU5NzAyNzE0NDE5.Xo7bUg.xrQds3ezBKNBafUaM204MRSwQ5A"

client.run(token)
