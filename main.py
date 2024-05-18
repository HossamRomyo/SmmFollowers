import requests
 
prefix = '!'
import discord
import asyncio
import yaml
config = yaml.safe_load(open('config.yml', 'r').read())

admins = config['admins']

intents = discord.Intents.default()
intents.presences = True
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
target_message_content = ":moneybag: | justmanooo, has transferred `$1` to <@1206056394285916280>"
def calculate_tax(args):
    try:
        args2 = int(args)
        
    except ValueError:
        return ":information_source: Error: It must be a number"

    if not args2:
        return ":information_source: Error: Must be a number"

    if args2 < 1:
        return ":information_source: Error: The number must be larger than 1"

    tax = args2 * 20 // 19 + 1

    if args2 == 1:
        return f":notes: The Final Cost Is: 1"

    return f"{tax}"
async def logger(order,response):
    channel = client.get_channel(config['logchannel'])  
    await channel.send(f'**Received Order : {order} , \n Order ID: {response}**')

async def editFunc2(message, args):
    if message.author.id in admins:
        config['logchannel'] = args[0]
        await message.channel.send(f'**Successfully edited log channel to : {args[0]}**')
        with open('config.yml', 'w') as f:
            yaml.safe_dump(config, f)
async def editFunc3(message, args):
    if message.author.id in admins:
        args0 = args[0]
        args1 = args[1]
        if args0 == 'instaf':
            config['instaf'] == args[1]
        elif args0 == 'instal':
            config['instal'] == args[1]
        elif args0 == 'instav':
            config['instav'] == args[1]
        elif args0 == 'tikl':
            config['tikl'] == args[1]
        elif args0 == 'tikl':
            config['tikl'] == args[1]
        elif args0 == 'tikv':
            config['tikv'] == args[1]
        elif args0 == 'tikf':
            config['tikf'] == args[1]
        else:
            await message.channel.send('incorrect product')
            return None
        await message.channel.send('Successfully edited')
        with open('config.yml', 'w') as f:
            yaml.safe_dump(config, f)
async def editFunc(message, args):
    print(message.author.id)
    if message.author.id in admins:
        print(args)
        args0 = args[0]
        if args0 == 'instaf':
            config['instafPrice'] == args[1]
        elif args0 == 'instal':
            config['instalPrice'] == args[1]
        elif args0 == 'instav':
            config['instavPrice'] == args[1]
        elif args0 == 'tikl':
            config['tiklPrice'] == args[1]
        elif args0 == 'tikl':
            config['tiklPrice'] == args[1]
        elif args0 == 'tikv':
            config['tikvPrice'] == args[1]
        elif args0 == 'tikf':
            config['tikfPrice'] == args[1]
        else:
            await message.channel.send('incorrect product')
            return None
        await message.channel.send('Successfully edited')
        with open('config.yml', 'w') as f:
            yaml.safe_dump(config, f)
async def ping_function(message):
    print("Hi")
    await message.channel.send("hello world")
async def buy_function(message, args):
    print(args)  
    if len(args) > 3:
        await message.channel.send("Invalid usage. Use: !buy <quantity> <product> <buyer>")
        return
    
    print(args[0])
    quantity = args[0]
    product = args[1]
    buyer = args[2]
    
    response = f"Buying {quantity} {product} for {buyer}"
    

    price = None
    quantity = int(quantity)
    if product == "tikf":
        if quantity >= 50:
            idd = config['tikf']
            price = config['tikfPrice'] * int(quantity)
        else:
            await message.channel.send('**اقل كميه للطلب 50**')
    elif product == "tikv":
        if quantity >= 100:

            idd = config['tikv']
            price = config['tikvPrice'] * int(quantity)
        else:
            await message.channel.send('**اقل كميه للطلب 100**')
    elif product == "tikl":
        if quantity >= 10:

            idd = config['tikl']
            price = config['tiklPrice'] * int(quantity)
        else:
            await message.channel.send('**اقل كميه للطلب 10**')
    elif product == "instav":
        if quantity >= 100:

            idd = config['instav']
            price = config['instavPrice'] * int(quantity)
        else:
            await message.channel.send('**اقل كميه للطلب 100**')
    elif product == "instal":
        if quantity >= 100:

            idd = config['instal']
            price = config['instalPrice'] * int(quantity)
        else:
            await message.channel.send('**اقل كميه للطلب 100**')
    elif product == "instaf":
        if quantity >= 10:

            idd = config['instaf']
            price = config['instafPrice'] * int(quantity)
        else:
            await message.channel.send('**اقل كميه للطلب 10**')
    else:
        await message.channel.send('incorrect product.')
        return None
    result = calculate_tax(price)
    if message.author.id in admins:
        x = True
    else:
        await message.channel.send(f'** تم استلام طلبك برجاء التحويل خلال 60 ثانيه كحد اقصي , رسالة التحويل :**')
        await message.channel.send(f'`#credit 1125881792466001930 {result}`')
        def check(msg):
            print(price)
            return (msg.author.id == 282859044593598464 and
                    f"has transferred `${price}`" in msg.content and
                    any(user.id == 1125881792466001930 for user in msg.mentions))
        
        try:
            msg = await client.wait_for('message', check=check, timeout=60.0)
            x = True
        except asyncio.TimeoutError:
            x = False
    if x == True:
        sendOrder = requests.post(f'https://smmtrending.com/api/v2?key=f61a3b6009a70c29e3d035dee5ee1573&action=add&service={idd}&link={buyer}&quantity={quantity}')
        print(sendOrder.text)
        if 'error' not in sendOrder.text:
            await message.channel.send('** الطلب قيد التنفيذ , مدة الاكتمال : 1 - 10 دقائق**')
            await logger(args,sendOrder.json()['order'])
        elif 'error' in sendOrder.text:
            await message.channel.send(f'Order Failed due to : {sendOrder.json()["error"]}')
            logger(args,sendOrder.text)

    else:
        await message.channel.send('**فشلت العمليه , لم يتم ارسال المبلغ المطلوب في الوقت المحدد .**')    


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
message_content = """
**للطلب :
- !buy (العدد) (اسم الخدمة) (الرابط)

For order:
- !buy (count) (service name) (link)

أسماء الخدمات تكون كالتالي:
- لايكات انستجرام: instal
- مشاهدات انستجرام: instav
- متابعات انستجرام: instaf

- لايكات تيك توك: tikl
- مشاهدات تيك توك: tikv
- متابعات تيك توك: tikf

---
- لرؤية المخزون: !stock
- لرؤية الأسعار: !prices

! قبل الشراء تاكد من قرائه الروم التالي : <#1241176244075233310> !
**
"""
message_content2 = """
**~# Our Stock :\n\n Followers :2m \nAccount Likes : 2b \nAccountsViews : 100m \n\nAccountFollow :20k \nAccount Likes : 30k \nAccount Views : 2b**
"""
message_content3 = f'**~# Our Prices :\n\n insta : \n\n Followers :{config["instafPrice"]} \nAccount Likes : {config["instalPrice"]} \nAccountsViews : {config["instavPrice"]} \n\ntik : \n\n AccountFollow :{config["tikfPrice"]} \nAccount Likes : {config["tiklPrice"]} \nAccount Views : {config["tikvPrice"]} **'
@client.event
async def on_message(message):
    command, *args = message.content.split()

    if message.content.startswith('!helloworld'):
        await ping_function(message)
    elif command == ('!buy'):
        await buy_function(message, args) 
    elif message.content.startswith('!stock'):
        embed = discord.Embed(
        title="المخزون",
        description=message_content2,
        color=0x7289DA
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1241140499985727578/1241182813177385003/237F0A4C-1454-40F4-B9B3-7C9BF21485AB.jpg?ex=66494512&is=6647f392&hm=09e8c3a6a9e1af243444b0d6d09700738db44b434cb951fbae97ba8ab3dfa99c&=&format=webp&width=989&height=473")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1241140499985727578/1241182813177385003/237F0A4C-1454-40F4-B9B3-7C9BF21485AB.jpg?ex=66494512&is=6647f392&hm=09e8c3a6a9e1af243444b0d6d09700738db44b434cb951fbae97ba8ab3dfa99c&=&format=webp&width=989&height=473")

        embed.set_footer(text="Powered by EgyStore")
        await message.channel.send(embed=embed)    
    elif command == ('!editprice'):
        await editFunc(message, args) 
    elif command == ('!editlog'):
        await editFunc2(message, args) 
    elif command == ('!editid'):
        await editFunc3(message, args) 
    elif message.content.startswith('!prices'):
        embed = discord.Embed(
        title="الاسعار",
        description=message_content3,
        color=0x7289DA
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1241140499985727578/1241182813177385003/237F0A4C-1454-40F4-B9B3-7C9BF21485AB.jpg?ex=66494512&is=6647f392&hm=09e8c3a6a9e1af243444b0d6d09700738db44b434cb951fbae97ba8ab3dfa99c&=&format=webp&width=989&height=473")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1241140499985727578/1241182813177385003/237F0A4C-1454-40F4-B9B3-7C9BF21485AB.jpg?ex=66494512&is=6647f392&hm=09e8c3a6a9e1af243444b0d6d09700738db44b434cb951fbae97ba8ab3dfa99c&=&format=webp&width=989&height=473")

        embed.set_footer(text="Powered by EgyStore")
        await message.channel.send(embed=embed)
    elif message.content.startswith('!help'):
        embed = discord.Embed(
        title="طرق الطلب",
        description=message_content,
        color=0x7289DA
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1241140499985727578/1241182813177385003/237F0A4C-1454-40F4-B9B3-7C9BF21485AB.jpg?ex=66494512&is=6647f392&hm=09e8c3a6a9e1af243444b0d6d09700738db44b434cb951fbae97ba8ab3dfa99c&=&format=webp&width=989&height=473")
        
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1241140499985727578/1241182813177385003/237F0A4C-1454-40F4-B9B3-7C9BF21485AB.jpg?ex=66494512&is=6647f392&hm=09e8c3a6a9e1af243444b0d6d09700738db44b434cb951fbae97ba8ab3dfa99c&=&format=webp&width=989&height=473")
        embed.set_footer(text="Powered by EgyStore")

        await message.channel.send(embed=embed)
    elif message.content.startswith('!admins'):
        await message.channel.send('editprice , editlog, editid')
client.run(config['bot_token'])
