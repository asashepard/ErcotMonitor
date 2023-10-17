import re

import discord

import bot
import main
from datetime import datetime
from rpy2 import robjects
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")  # fix for 'Fail to allocate bitmap' error


def handle_response(message) -> bool:
    if message == '!ercot':
        generate_report()
        return False
    if message == '!ercotcreate':
        generate_repeating()
        return True  # should repeat (defaults subsequently updated in bot.py)
    elif '<@1162096462633631773>' in message:  # mention of ErcotMonitor
        generate_help()
        return False


# GENERATE METHODS #


def generate_report() -> discord.Embed:
    bot.embed = generate_embed(title=':newspaper2:  **Detailed report on current state of ERCOT grid**',
                               colour=discord.Colour.blue(),
                               field_name='Complete data',
                               field_values=get_data(),
                               footer='generated ' + get_formatted_time(True))
    return bot.embed


def generate_repeating() -> discord.Embed:
    bot.embed = generate_embed(title=':newspaper2: :red_circle:  **Live report on ERCOT grid health**',
                               colour=discord.Colour.red(),
                               field_name='Vital indicators',
                               field_values=get_data(
                                   tuple([main.data_class.nwd, main.data_class.nwd + 3, main.data_class.nwd + 5])),
                               footer='updated ' + get_formatted_time())
    return bot.embed


def generate_embed(title, colour, field_name, field_values, footer) -> discord.Embed:
    embed = discord.Embed(title=title, description='Source: *' + main.data_class.URL + '*', colour=colour)
    embed.add_field(name=field_name, value=field_values)
    embed.set_footer(text=footer)
    update_plot()
    embed.set_image(url='attachment://plot.png')
    return embed


def generate_warning() -> str:
    return ':rotating_light: @everyone **POWER EMERGENCY**\nCurrent frequency: ' + str(main.data_class.last_update[
        main.data_class.nwd]) + ' hertz'


def generate_help() -> bool:
    text = ':grey_question: **Commands**\n'
    text += '**!ercot**\n- generates simple + visual report on grid status\n'
    text += '**!ercot_create**\n- generates self-updating report on grid status (required administrator permission)\n'
    return False


# ACCESS METHODS #


def get_data(spec=tuple(range(0, main.data_class.categories.__len__()))) -> str:
    data_str = ''
    d = main.data_class
    pre = get_r_analysis()
    for i in range(d.nwd, len(d.categories) - 5):  # -4 excludes DC data
        if i in spec:
            data_str += '- ' + d.categories[i] + ': ' + str(d.last_update[i])
            if i != d.nwd + 3 and i != d.nwd + 5:
                data_str += ' ' + get_momentum_emoji(d.momentum[i])
            # warning
            if i == d.nwd and float(d.last_update[d.nwd]) < 59.7:
                data_str += ' :warning:'
            # prediction
            elif i == d.nwd + 3:
                data_str += ' **-- proj. △ in 30m: ' + str(pre[0]) + '**'
            elif i == d.nwd + 5:
                data_str += ' **-- proj. △ in 30m: ' + str(pre[1]) + '**'
            data_str += '\n'
    return data_str


def get_r_analysis() -> list:
    capacity_script = open('capacity.R', 'r').read()
    demand_script = open('demand.R', 'r').read()
    capacity = robjects.r(f'''{capacity_script}''')
    demand = robjects.r(f'''{demand_script}''')
    c_thirty_pre = float(re.split('\s+', capacity.__str__().split('hourofday')[2])[1]) / 2  # prediction for 30 minutes
    d_thirty_pre = float(re.split('\s+', demand.__str__().split('hourofday')[2])[1]) / 2  # prediction for 30 minutes
    return [d_thirty_pre, c_thirty_pre]


# UTIL METHODS #


def get_momentum_emoji(momentum) -> str:
    if momentum > 1:
        return ':arrow_double_up:'
    elif momentum < -1:
        return ':arrow_double_down:'
    elif momentum > 0:
        return ':arrow_up:'
    elif momentum < 0:
        return ':arrow_down:'
    return ':arrow_right:'


def get_formatted_time(seconds=False) -> str:
    if seconds:
        return datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
    return datetime.now().strftime("%m/%d/%Y at %H:%M")


def update_plot() -> None:
    d = main.data_class
    fig, ax = plt.subplots()
    labels = d.categories[main.data_class.nwd + 3], d.categories[main.data_class.nwd + 5]
    ax.pie([d.last_update[main.data_class.nwd + 3], d.last_update[main.data_class.nwd + 5]], labels=labels)
    plt.savefig('plot.png')
