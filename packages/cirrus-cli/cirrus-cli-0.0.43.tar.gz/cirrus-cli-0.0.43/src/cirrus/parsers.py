#!/usr/bin/env python
#parsers.py

import argparse



def attr_list(x):
    if ',' in x:
        return [ y for y in x.split(',') if len(y.strip())]
    else:
        return [x]

def parse1():

    parser = argparse.ArgumentParser()
    parser.add_argument('--plugin','-p', dest='plugin', default=None)

    opts, _ = parser.parse_known_args()

    return opts


def parse2():

    parser = argparse.ArgumentParser()
    parser.add_argument('--plugin','-p', dest='plugin', default=None)
    parser.add_argument('--environment','-e', default=None, dest='env')
    parser.add_argument('--role', '-r', default=None, dest='role')
    parser.add_argument('--nodes', '-n', default=None, dest='nodes')
    parser.add_argument('--attributes', '-a', type=attr_list, default=None, dest='attrs')


    opts = parser.parse_args()
    for x in vars(opts):
        print x, getattr(opts, x)


def parse3():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plugin','-p', dest='plugin', default=None)
    parser.add_argument('--herp', default=None, dest='herp')
    parser.add_argument('--role', default=None, dest='derp')

    opts = parser.parse_args()
    print opts



if __name__ == '__main__':
    opts = parse1()
    if opts.plugin == 'chef':
        parse2()
    else:
        parse3()

