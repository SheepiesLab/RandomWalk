import random
import statistics
import json

import click

random.seed()

def load_config(file):
    return json.load(open(file, 'r'))

def dice_range(start, end):
    return random.randrange(start, end)

def random_walk_once(conf):
    d = dice_range(*(conf['dice_range']))
    for o in conf['dice_steps']:
        if d in range(*o['range']):
            return o['steps']

def random_walk(conf):
    i = 0
    for _ in range(conf['rolls']):
        i = i + random_walk_once(conf)
    return i

def repeated_random_walk(conf):
    res = []
    for _ in range(conf['repeat']):
        res.append(random_walk(conf))
    return res

@click.command(help='A program to simulate random walking.')
@click.option('-c', '--conf', default='./config.json', help='Config file path.')
@click.option('-l', '--log', default='./results.log', help='Result log file path.')
def main(conf, log):
    conf = load_config(conf)
    for exp in conf:
        res = repeated_random_walk(exp)
        with open(log, 'a') as f:
            json.dump({
                "max": max(res),
                "mean": statistics.mean(res),
                "results": res
            }, f)

if __name__ == "__main__":
    main()
