import csv
import datetime
from decimal import Decimal
import matplotlib.pyplot as plt

reward_halving_dates = [
    datetime.date(2012, 11, 29),
    datetime.date(2016, 7, 9),
    datetime.date(2020, 5, 17),
]

def calculate_days_to_next(date):
    for x in reward_halving_dates:
        if date < x:
            break
    return ((x - date).days) / 30.0

def parse_date(x):
    try:
        date = datetime.datetime.strptime(x, '%b %d, %Y').date()
    except ValueError:
        date = datetime.datetime.strptime(x, '%B %d, %Y').date()
    return date

def get_data(filename='btc-price.csv'):
    fp = open(filename, 'r', encoding='utf-8')
    reader = csv.reader(fp)
    it = iter(reader)
    header = next(it)
    v = []
    for row in it:
        date = row[0]
        date = parse_date(date)
        price = row[1].replace(',', '')
        price = float(price)
        days_to_next = calculate_days_to_next(date)
        v.append([date, price, days_to_next])
    fp.close()
    return v

def get_data2(filename='btc-price.csv'):
    data = get_data(filename)
    data.sort()
    v = []
    ref = None
    ref_index = -1
    for i, row in enumerate(data):
        date, price, days_to_next = row
        if ref is None or date >= reward_halving_dates[ref_index]:
            print(i, row)
            ref = row
            ref_index += 1
        price = (price - ref[1]) / ref[1]
        v.append([date, price, days_to_next])
    return v

def plot(data, log_scale=True):
    x = [row[0] for row in data]
    y = [row[1] for row in data]
    z = [row[2] for row in data]

    cmap = plt.get_cmap('viridis')
    sc = plt.scatter(x, y, c=z, cmap=cmap)
    cb = plt.colorbar(sc)

    from matplotlib import ticker
    tick_locator = ticker.FixedLocator(range(46))
    cb.locator = tick_locator
    cb.update_ticks()

    if log_scale:
        plt.yscale('log')
        plt.title('log')

    for x in reward_halving_dates:
        plt.axvline(x=x, color='k')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)


def run1():
    plt.figure(figsize=(18, 10))
    data = get_data2()
    plot(data, log_scale=False)
    plt.ylabel('(price - initial) / initial')
    plt.title('Bitcoin - months till next halving')
    plt.savefig('fig1.png', dpi=300)
    #plt.show()

def run2():
    plt.figure(figsize=(18, 10))
    data = get_data()
    plot(data)
    plt.title('Bitcoin - months till next halving')
    plt.savefig('fig2.png', dpi=300)
    #plt.show()

def run1_ltc():
    plt.figure(figsize=(18, 10))
    data = get_data2('ltc-price.csv')
    plot(data, log_scale=False)
    plt.title('Litecoin - months till next Bitcoin\'s halving')
    plt.ylabel('(price - initial) / initial')
    plt.savefig('fig1-ltc.png', dpi=300)
    #plt.show()

def run2_ltc():
    plt.figure(figsize=(18, 10))
    data = get_data('ltc-price.csv')
    plot(data)
    plt.title('Litecoin - months till next Bitcoin\'s halving')
    plt.savefig('fig2-ltc.png', dpi=300)
    #plt.show()

run1_ltc()
run2_ltc()
