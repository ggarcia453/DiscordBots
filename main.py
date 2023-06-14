import discord, os, statsapi, re, random
from datetime import datetime as d
from discord.ext import commands
from dotenv import load_dotenv
from LastFM import LastFM
from OpenWeather import OpenWeather
from dog import Dog
from PickupLines import Pickup


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = commands.Bot(command_prefix='^')


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def time(t: str):
    if int(t[:2]) == 0:
        return '12' + t[2:] + ' am'
    elif int(t[:2]) > 12:
        return str(int(t[:2]) - 12) + t[2:] + ' pm'
    else:
        return str(int(t[:2])) + t[2:] + ' am'



@client.command()
async def lottery(ctx):
    write, new, stock_list = False, False, ['G-Fuel', 'Big Baller Brand', 'Nintendo', 'Texas Instruments', 'Society Inc.']
    sto = True
    with open('users.txt', 'r') as f:
        if str(ctx.message.author) not in f.read():
            write, new = True, True
            await ctx.send('This appears to be your first time playing \'Lottery\'')
            await ctx.send('Here\'s how it works')
            embed = discord.Embed(colour=discord.Colour.dark_magenta())
            embed.add_field(name='Tutorial', value='You\'ll be given 5 lottery tickets.\n'
                                                   'You have three commands you can use\nBuy- '
                                                   'You can buy lottery tickets\nUse-'
                                                   'You can use lottery tickets to get money to buy lottery '
                                                   'tickets\nBet- '
                                                   'You could also bet tickets to get more tickets!\n'
                                                   'Sell-Sell your stocks\n'
                                                   'Check-Check how much you have in tickets, money and stocks\n'
                                                   'Anyways here is 5 tickets and $100 to get you started')
            await ctx.send(embed=embed)
        else:
            def check(m):
                return m.author == ctx.message.author
            await ctx.send('What would you like to do?\n(Buy, Use, Bet, Sell, Check)')
            msg = await client.wait_for('message', check=check)
            if msg.content == 'Buy':
                await ctx.send('Would you like to buy lottery tickets or stocks?')
                m = await client.wait_for('message', check=check)
                if m.content in ['Lottery', 'lottery', 'Lottery tickets', 'lottery tickets']:
                    with open("lottery_tickets_" + str(ctx.message.author)[:-5], "r") as f:
                        tickets, money = (line.rstrip('\n') for line in f.readlines())
                        await ctx.send('How many lottery tickets would you like to buy?')
                        await ctx.send(f'(Max you can buy is {int(int(money) / 10)})')
                        number = await client.wait_for('message', check=check)
                        if int(number.content) > int(int(money) / 10):
                            await ctx.send('Too many lottery tickets\nTransaction cancelled')
                        else:
                            await ctx.send(f'Purchased {number.content} tickets')
                            tickets, money, write = str(int(tickets) + int(number.content)), str(
                                int(money) - (int(number.content) * 10)), True
                elif m.content in ['Stocks', 'stocks', 'Stonks', 'stonks']:
                    if sto:
                        with open('stocks.txt', 'r') as f:
                            await ctx.send('Here are the current prices for stocks')
                            string, new_stock = '', []
                            stonk_list = [line.rstrip('\n').split('\n')[0].split('=') for line in f.readlines()]
                            for stock in stonk_list.copy():
                                string += f"{stock[0]} is now priced at ${stock[1]}\n"
                                new_stock.append(stock[0])
                            embed = discord.Embed(colour=discord.Colour.dark_teal())
                            embed.add_field(name='Stocks', value=string)
                            await ctx.send(embed=embed)
                        with open("lottery_tickets_" + str(ctx.message.author)[:-5], "r") as f:
                            tickets, money = (line.rstrip('\n') for line in f.readlines())
                        await ctx.send("What would you like to buy?")
                        m = await client.wait_for('message', check=check)
                        for n, s in enumerate(new_stock):
                            if m.content == s:
                                await ctx.send('How many shares would you like?')
                                maximum = int(int(money) / int(stonk_list[n][1]))
                                await ctx.send(f'The max you can buy is {maximum}')
                                a = await client.wait_for('message', check=check)
                                if int(a.content) > maximum:
                                    await ctx.send('You\'re trying to buy too many stocks\nDon\'t')
                                else:
                                    write = True
                                    money = int(money) - (int(a.content)* int(stonk_list[n][1]))
                                    with open("stocks_" + str(ctx.message.author)[:-5], "r") as t:
                                        k = [line.rstrip('\n') for line in t.readlines()]
                                    with open("stocks_" + str(ctx.message.author)[:-5], "w") as t:
                                        for i in range(len(k)):
                                            if i == n:
                                                t.write(a.content)
                                            else:
                                                t.write(k[i])
                                            t.write('\n')
                                    await ctx.send('Purchased')
                    else:
                        await ctx.send('Stocks cannot be bought right now')
                else:
                    await ctx.send('I\'m sorry I don\'t think you buy that')
            elif msg.content == 'Use':
                with open("lottery_tickets_" + str(ctx.message.author)[:-5], "r") as f:
                    tickets, money = (line.rstrip('\n') for line in f.readlines())
                    if int(tickets) > 1:
                        await ctx.send('Using ticket')
                        chance, tickets = random.random(), int(tickets) - 1
                        if chance < 0.25:
                            increase = 0
                        elif 0.25 < chance < 0.45:
                            increase = 10
                        elif 0.40 < chance < 0.6:
                            increase = 20
                        elif 0.6 < chance < 0.75:
                            increase = 30
                        elif 0.70 < chance < 0.85:
                            increase = 50
                        elif 0.85 < chance < 0.925:
                            increase = 100
                        elif 0.925 < chance < 0.975:
                            increase = 500
                        else:
                            increase = 1000
                        money, write = int(money) + increase, True
                        if increase != 0:
                            await ctx.send(f'You won ${increase}')
                            await ctx.send("Congrats man\n:)")
                        else:
                            await ctx.send("You won nothing.\nBetter luck next time")
                    else:
                        await ctx.send("You have no more tickets")

            elif msg.content == 'Bet' or msg.content == 'bet':
                await ctx.send('How much are you betting?')
                bet = await client.wait_for('message', check=check)
                with open("lottery_tickets_" + str(ctx.message.author)[:-5], "r") as f:
                    tickets, money = (line.rstrip('\n') for line in f.readlines())
                    if int(bet.content) < int(money):
                        await ctx.send('Heads or Tails?')
                        m = await client.wait_for('message', check=check)
                        a = random.random()
                        if 'Heads' in m.content and a >= 0.50:
                            money = int(money) + int(bet.content)
                            await ctx.send('Congrats you won your bet!')
                        elif 'Heads' in m.content and a < 0.50:
                            money = int(int(money) - int(bet.content))
                            await ctx.send('Oh no you lost your bet!')
                        elif 'Tails' in m.content and a < 0.50:
                            money = int(money) + int(bet.content)
                            await ctx.send('Congrats you won your bet!')
                        elif 'Tails' in m.content and a > 0.50:
                            money = int(int(money) - int(bet.content))
                            await ctx.send('Oh no you lost your bet')
                        else:
                            await ctx.send("Option not detected\nNothing is changed")
                        write = True
                    else:
                        await ctx.send('Invalid bet\nYou probably bet too much')
            elif msg.content == 'Sell' or msg.content == 'sell':
                await ctx.send('Which stock would you like to sell?')
                mes = await client.wait_for('message', check=check)
                found = False
                with open("lottery_tickets_" + str(ctx.message.author)[:-5], "r") as f:
                    tickets, money = (line.rstrip('\n') for line in f.readlines())
                for i, j in enumerate(stock_list):
                    if mes.content == j:
                        found = True
                        with open("stocks_" + str(ctx.message.author)[:-5], "r") as l:
                            stoks = [line.rstrip('\n') for line in l.readlines()]
                            maximum = stoks[i]
                            if int(maximum) > 0:
                                await ctx.send('How many stocks do you wish to sell?')
                                sel = await client.wait_for('message', check=check)
                                if int(sel.content) > int(maximum):
                                    await ctx.send('You\'re trying to sell too many stocks')
                                else:
                                    new_stoks = [stoks[o] for o in range(len(stoks))]
                                    new_stoks[i] = str(int(maximum) - int(sel.content))
                                    with open("stocks_" + str(ctx.message.author)[:-5], "w") as w:
                                        for a in new_stoks:
                                            w.write(str(a) + '\n')
                                    with open('stocks.txt', 'r') as st:
                                        stonk_list = [line.rstrip('\n').split('\n')[0].split('=') for line in st.readlines()]
                                        for index in range(len(stonk_list)):
                                            if index == i:
                                                price = stonk_list[i][1]
                                                break
                                    money = str(int(money) + int(sel.content) * int(price))
                                    write = True
                                    await ctx.send(f"Sold\nYou made ${int(sel.content) * int(price)}")
                            else:
                                await ctx.send('You have no stocks here')
                if not found:
                    await ctx.send('Sorry I couldn\'t find that stock')
            elif msg.content == 'Check':
                with open("lottery_tickets_" + str(ctx.message.author)[:-5], "r") as f:
                    tickets, money = (line.rstrip('\n') for line in f.readlines())
                await ctx.send(f"You have {tickets} tickets and ${money}")
                with open("stocks_" + str(ctx.message.author)[:-5], "r") as l:
                    stoc_list, v = [line.rstrip('\n') for line in l.readlines()], 'You also have '
                    for n, s in enumerate(stoc_list):
                        v += f"{s} stocks in {stock_list[n]}, "
                    await ctx.send(v[:-2])
            else:
                await ctx.send('Not a valid command')
    if write and new:
        with open("lottery_tickets_" + str(ctx.message.author)[:-5], "w") as f:
            f.write('5\n100')
        with open("stocks_" + str(ctx.message.author)[:-5], "w") as f:
            f.write('0\n0\n0\n0\n')
        with open("users.txt", "a") as f:
            f.write(str(ctx.message.author))
        with open("stock_owners.txt", "a") as q:
            q.write(str(ctx.message.author) + '-')
    elif write:
        with open("lottery_tickets_" + str(ctx.message.author)[:-5], "w") as f:
            f.write(str(tickets))
            f.write('\n')
            f.write(str(money))


@client.command()
async def ping(ctx):
    print('ping')
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms ')


@client.command()
async def stonks(ctx):
    if str(ctx.message.author) != 'Napalmguy#9929':
        with open('stocks.txt', 'r') as f:
            string, new_stock = '', []
            stonk_list = [line.rstrip('\n').split('\n')[0].split('=') for line in f.readlines()]
            for stock in stonk_list.copy():
                string += f"{stock[0]} is now priced at ${stock[1]}\n"
            embed = discord.Embed(colour=discord.Colour.dark_teal())
            embed.add_field(name='Stocks', value=string)
            await ctx.send(embed=embed)
    else:
        await ctx.send('Stock market changes are as follows')
        with open('stocks.txt', 'r') as f:
            string, new_stock = '', []
            stonk_list = [line.rstrip('\n').split('\n')[0].split('=') for line in f.readlines()]
            for stock in stonk_list.copy():
                price = int((random.random() + 0.5) * int(stock[1]))
                if int(price) < 100:
                    price = 100
                string += f"{stock[0]} is now priced at ${price}\n"
                new_stock.append([stock[0], price])
            embed = discord.Embed(colour=discord.Colour.dark_teal())
            embed.add_field(name='Stocks', value=string)
            await ctx.send(embed=embed)
        with open('stocks.txt', 'w') as f:
            for stock in new_stock:
                f.write(f'{stock[0]}={stock[1]}\n')


@client.command()
async def prices(ctx):
    with open('stocks.txt', 'r') as f:
        await ctx.send('Here are the current prices for stocks')
        string, new_stock = '', []
        stonk_list = [line.rstrip('\n').split('\n')[0].split('=') for line in f.readlines()]
        for stock in stonk_list.copy():
            string += f"{stock[0]} is now priced at ${stock[1]}\n"
            new_stock.append(stock[0])
        embed = discord.Embed(colour=discord.Colour.dark_teal())
        embed.add_field(name='Stocks', value=string)
        await ctx.send(embed=embed)


@client.command()
async def pickup_line(ctx):
    send_ = Pickup().regular()
    if '_______' not in send_:
        await ctx.send(send_)
    else:
        await ctx.send(send_.replace('_______', str(ctx.message.author)[:-5]))
    if random.random() > 0.50:
        await ctx.send("<:fuckkk:851239240083701791>")
    else:
        await ctx.send("<:fuckboi:793297429209808981>")


@client.command()
async def dog(ctx, *args):
    if len(args) == 0:
        breed = None
    else:
        breed = '+'.join(args)
    d = Dog(breed=breed)
    await ctx.send(d.dog_pic())


@client.command()
async def fish(ctx):
    await ctx.send(discord.utils.get(ctx.guild.roles, name="big bitch").mention)
    await ctx.send('This motherfucker above^ killed Mimi\'s fish apparently')
    await ctx.send(discord.utils.get(ctx.guild.roles, name="togedemaru").mention)


@client.command()
async def greet(ctx):
    w = True
    with open('users.txt', 'r') as f:
        if str(ctx.message.author) in f.read():
            await ctx.send('Hey Whats up?')
            await client.wait_for('message', check= lambda x: x.author == ctx.message.author)
            await ctx.send('I\'m not reading that man.\n I\'m glad to hear that.\nOr sorry to hear that happened')
            w = False
    if w:
        with open('users.txt', 'a') as k:
            k.write(str(ctx.message.author) + '\n')
        await ctx.send(f'..umm oh hi <@{ctx.message.author.id}> uhh')
        await ctx.send('I noticed you were uh... kinda new here\n'
                       'i uhh guess i should introduce umm\n'
                       'myself\n'
                       'im kinda... uh .. a bit nervous uwu')
        await ctx.send('https://cdn.discordapp.com/attachments/749875426859679855/853865939178881044/E30To4PXIAAfbCs.png')


@client.command()
async def music(ctx, country='United+States'):
    a, b = LastFM(ccode=country).random()
    await ctx.send(f'Your random {a} is {b}')


@client.command()
async def temperature(ctx, zipcode="92697", ccode="US"):
    weather = OpenWeather(zipcode=zipcode, ccode=ccode)
    await ctx.send(
        weather.transclude(f'The temperature in {weather.city} is @weather but it feels like {weather.feels}'))


@client.command()
async def sun(ctx, zipcode="92697", ccode="US"):
    weather = OpenWeather(zipcode=zipcode, ccode=ccode)
    a, b = str(d.fromtimestamp(weather.sunrise))[-8:], str(d.fromtimestamp(weather.sunset))[-8:]
    a, b = time(a), time(b)
    await ctx.send(f'Today the sun rose at {a} and will set at {b}')


@client.command()
async def I_hate(ctx, *args):
    if len(args) >= 1:
        a = 'I HATE {} '.format(' '.join(args).upper())
        for _ in range(6):
            a += a
        await ctx.send(a)
    else:
        await ctx.send('I HATE nothing because you did not enter something for me to hate')


@client.command()
async def standings_mlb(ctx, *args):
    league, division, year, cont = None, None, '2022', True
    for i in args:
        if i in ['AL', 'NL']:
            league = i
        if i in ['West', 'East', 'Central']:
            if 'AL' in args:
                division = 'AL ' + i
            else:
                division = 'NL ' + i
            league = None
        if i.isdigit() and int(i) in range(1969, 2022) and int(i) != 1981:
            year = i
        elif i.isdigit():
            cont = False
    if int(year) in range(1994, 2023) and cont:
        lg_dict = {'200': 'AL West',
                   '201': 'AL East',
                   '202': 'AL Central',
                   '203': 'NL West',
                   '204': 'NL East',
                   '205': 'NL Central',
                   'AL West': ('103', '200'),
                   'AL East': ('103', '201'),
                   'AL Central': ('103', '202'),
                   'NL West': ('104', '203'),
                   'NL East': ('104', '204'),
                   'NL Central': ('104', '205')}
        if league is None and division is None:
            embed = discord.Embed(
                colour=discord.Colour.gold())
            for i in list(lg_dict.keys())[:6]:
                data, standing_str = statsapi.standings_data(season=year), ''
                for team in data[int(i)]['teams']:
                    standing_str += (team['name']) + '\n'
                embed.add_field(name=f'{lg_dict[i]}', value=standing_str, inline=False)
            embed.add_field(name='More Information', value='For more detailed information enter a league or division')
            await ctx.send(embed=embed)
        if league is not None:
            embed = discord.Embed(
                colour=discord.Colour.gold())
            if league == 'AL':
                data, standing_str = statsapi.standings_data(season=year, leagueId='103'), ''
            else:
                data, standing_str = statsapi.standings_data(season=year, leagueId='104'), ''
            for a in data.values():
                standing_str = '*Includes  W  -  L\n'
                for t in a['teams']:
                    standing_str += t['name'] + '  '
                    for _ in range(len(a['div_name']) - len(t['name'])):
                        standing_str += ' '
                    standing_str += '    ' + str(t['w']) + ' - ' + str(t['l']) + '\n'
                embed.add_field(name=a['div_name'], value=standing_str, inline=False)
            embed.add_field(name='More Information',
                            value='If you wish for more detailed information, enter a division')
            await ctx.send(embed=embed)
        elif division is not None:
            embed = discord.Embed(
                colour=discord.Colour.gold())
            num = lg_dict[division]
            data, t_str = statsapi.standings_data(season=year, leagueId=str(num[0]))[int(num[1])], ''
            embed.add_field(name=data['div_name'], value='Information about this division is as follows:', inline=False)
            for t in data['teams']:
                info_str = 'The {} are currently ranked {} in the division with a record of {}-{}. '.format(t['name'], t[
                    'div_rank'], t['w'], t['l'])
                if t['gb'] != '-':
                    info_str += 'They are currently ' + str(t['gb']) + ' games back of the division lead'
                    if t['wc_gb'] != '-':
                        info_str += ' and ' + str(t['wc_gb']) + ' back of a wildcard spot.'
                    else:
                        info_str += '.'
                info_str += ' They are also ranked {} in the {}.'.format(t['league_rank'], division[:2])
                embed.add_field(name=t['name'], value=info_str, inline=False)
            await ctx.send(embed=embed)
    elif int(year) in range(1969, 1994) and cont:
        lg_dict = {'200': 'AL West',
                   '201': 'AL East',
                   '203': 'NL West',
                   '204': 'NL East'}
        if league is None and division is None:
            embed = discord.Embed(
                colour=discord.Colour.dark_orange())
            for i in lg_dict.keys():
                data, standing_str = statsapi.standings_data(season=year), ''
                for team in data[int(i)]['teams']:
                    standing_str += (team['name']) + '\n'
                embed.add_field(name=f'{lg_dict[i]}', value=standing_str, inline=False)
            embed.add_field(name='More Information', value='For more detailed information enter a league or division')
            await ctx.send(embed=embed)
        elif league is not None and division is None:
            if year == '1981':
                await ctx.send('Bot cannot handle the year \'1981\' due to the player\'s strike that year')
            else:
                await ctx.send(league)
                embed = discord.Embed(colour=discord.Colour.dark_orange())
                if league == 'AL':
                    try:
                        data = statsapi.standings_data(season=year, leagueId='103')
                    except Exception as e:
                        await ctx.send(e)
                else:
                    data = statsapi.standings_data(season=year, leagueId='104')
                for a in data.values():
                    standing_str = '*Includes  W  -  L\n'
                    for t in a['teams']:
                        standing_str += t['name'] + '  '
                        for _ in range(len(a['div_name']) - len(t['name'])):
                            standing_str += ' '
                        standing_str += '    ' + str(t['w']) + ' - ' + str(t['l']) + '\n'
                    embed.add_field(name=a['div_name'], value=standing_str, inline=False)
                embed.add_field(name='More Information',
                                value='If you wish for more detailed information, enter a division')
                await ctx.send(embed=embed)
        else:
            await ctx.send('Division and league specific stats are still under construction ')
    elif not cont:
        await ctx.send('You did not enter a valid year.\nOnly years of 1969-2021* are valid\n*1981 is not valid')


@client.command()
async def games_today_mlb(ctx, date=''):
    pattern = re.compile(r'([1][9][\d][\d]|[2][0]([0-1][\d]|'
                         r'[2][0-2]))[-]([0][\d]|[1][0-2])[-]'
                         r'([0][1-9]|[1-2][\d]|[3][0-1])')
    embed = discord.Embed(
        colour=discord.Colour.dark_orange())
    if date == '':
        data = statsapi.schedule()
        embed.set_author(name=data[0]['game_date'])
        for i in data:
            s_str = i['away_name'] + ' vs. ' + i['home_name'] + '\n'
            if i['doubleheader'] != 'N':
                s_str += 'Doubleheader Game ' + str(i['game_num']) + '\n'
            if i['status'] == 'Final':
                if 'winning_team' in i.keys():
                    s_str += i['winning_team'] + ' won this game\n' + i['summary']
                else:
                    print(i.items())
                embed.add_field(name=i['game_id'], value=s_str, inline=False)
            else:
                if i['away_probable_pitcher'] != '':
                    s_str += i['away_probable_pitcher']
                else:
                    s_str += 'Unknown'
                if i['home_probable_pitcher'] != '':
                    s_str += ' vs. ' + i['home_probable_pitcher']
                else:
                    s_str += ' vs. Unknown'
                if i['status'] == 'Postponed':
                    s_str += '\nPostponed'
                if i['status'] in ['Postponed', 'Pre-Game', 'In Progress']:
                    s_str += '\nScore: ' + str(i['away_score']) + ' - ' + str(i['home_score']) + ' ' + i[
                        'inning_state'] + ' ' + str(i['current_inning'])
                s_str += '\nLocation: ' + i['venue_name']
                embed.add_field(name=i['game_id'], value=s_str, inline=False)
        await ctx.send(embed=embed)
    elif re.match(pattern, date) is not None:
        data = statsapi.schedule(date=date)
        if len(data) > 0:
            embed.set_author(name=data[0]['game_date'])
            for i in data:
                s_str = i['away_name'] + ' vs. ' + i['home_name'] + '\n'
                if 'winning_team' in i.keys():
                    s_str += i['winning_team'] + ' won this game\n' + i['summary']
                elif i['status'] == 'Postponed':
                    s_str += 'This game has been postponed\n'
                embed.add_field(name=i['game_id'], value=s_str, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('There were no games played on this date ')
    else:
        await ctx.send('Please enter a valid date in the form YYYY-MM-DD')


@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error. Try ^help\nNotify Gaeb if necessary\n({error})')


client.remove_command('help')


@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.dark_blue())
    embed.set_author(name='Help : list of commands available')
    embed.add_field(name='^ping', value='Returns bot respond time in milliseconds', inline=False)
    embed.add_field(name='^dog', value='Return a picture of a dog!', inline=False)
    embed.add_field(name='^music', value='Returns random song or artist from the United States or another country',
                    inline=False)
    embed.add_field(name='^temperature', value='Return temperature in a city based on zipcode', inline=False)
    embed.add_field(name='^sun', value='Returns when sunrise occured and when sunset will occur.')
    embed.add_field(name='^I_hate', value='Returns a message about what the bot hates', inline=False)
    embed.add_field(name='^pickup_line', value='Returns a pickup line. If you have suggestions message them to me.', inline=False)
    embed.add_field(name='^lottery', value='Play the lottery game I created. Buy tickets Get money!',
                    inline=False)
    # embed.add_field(name='^standings_mlb',
    #               value='Return MLB standings in a specific year. Do *standings_mlb_help for more info', inline=False)
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def standings_mlb_help(ctx):
    embed = discord.Embed(colour=discord.Colour.gold())
    embed.set_author(name='Help for ^standings_mlb command')
    embed.add_field(name='year', value='Year of standings that will be returned.\n'
                                       'Currently only supports years from 1995 to 2021', inline=False)
    embed.add_field(name='league', value='Specific league that you want to see standings from', inline=False)
    embed.add_field(name='division', value='Specific division that you want to see standings from\n'
                                           'Must include a specific league as well (i.e. AL West NOT West) ',
                    inline=False)
    await ctx.send(embed=embed)


if __name__ == '__main__':
    client.run(TOKEN)
