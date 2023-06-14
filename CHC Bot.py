import discord, os, statsapi, re, random
from discord.ext import commands
from dog import Dog
from frog import Frog
from PickupLines import Pickup

TOKEN = ''#Token not shown in code for privacy reasons
client = commands.Bot(command_prefix='^')


@client.command()
async def dog(ctx, *args):
    if len(args) == 0:
        breed = None
    else:
        breed = '+'.join(args)
    d = Dog(breed=breed)
    await ctx.send(d.dog_pic())


@client.command()
async def frog(ctx):
    await ctx.send(Frog().ree())


@client.command()
async def pickup_line(ctx):
    send_ = Pickup().regular()
    if '_______' not in send_:
        await ctx.send(send_)
    else:
        await ctx.send(send_.replace('_______', str(ctx.message.author)[:-5]))


client.remove_command('help')


@client.command()
async def greet(ctx):
    w = True
    with open('users.txt', 'r') as f:
        if str(ctx.message.author) in f.read():
            await ctx.send('Hey Whats up?')
            await client.wait_for('message', check=lambda x: x.author == ctx.message.author)
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
        await ctx.send(
            'https://cdn.discordapp.com/attachments/749875426859679855/853865939178881044/E30To4PXIAAfbCs.png')


@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.dark_blue())
    embed.set_author(name='Help : list of commands available')
    embed.add_field(name='^dog', value='Returns a picture of a dog!', inline=False)
    embed.add_field(name='^frog', value='Returns a picture of a frog!', inline=False)
    embed.add_field(name='^pickup_line', value='Returns a pickup line. If you have suggestions message them to me.',
                    inline=False)
    embed.add_field(name='^greet', value='Get a message from the bot! (Is he friendly?)', inline=False)
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error. Try ^help\nNotify Gaeb if necessary\n({error})')



if __name__ == "__main__":
    client.run(TOKEN)
