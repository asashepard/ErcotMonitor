import discord

import main
from datetime import datetime
import matplotlib.pyplot as plt


def handle_response(message) -> list:
    if message == '!ercot':
        return generate_report()
    # todo simple help message on mention (bot.py)


def generate_report() -> list:
    report = []
    text = ''
    time = datetime.now()
    time_str = f'{time.year}-{time.month}-{time.day} at {time.hour}:{time.minute}:{time.second}'  # todo fix single-digit formatting
    text += f':newspaper2:  **Report ' + time_str + ' on state of ERCOT grid**\n'
    text += 'source: *https://www.ercot.com/content/cdr/html/real_time_system_conditions.html*\n'
    text += get_data()
    report.append(text)
    update_plot()
    report.append(True)  # indicates image should be sent
    return report


def get_data() -> str:
    data_str = ''
    d = main.data_class
    for i in range(1, len(d.categories) - 5):  # -5 excludes DC data
        data_str += '- ' + d.categories[i] + ': ' + str(d.last_update[i]) + ' ' + get_momentum_emoji(d.momentum[i]) + '\n'
    return data_str


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


def update_plot() -> None:
    d = main.data_class
    fig, ax = plt.subplots()
    labels = d.categories[4], d.categories[6]
    ax.pie([d.last_update[4], d.last_update[6]], labels=labels)
    plt.savefig('plot.png')
    plt.close(fig)
