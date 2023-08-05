# -*- coding: utf-8 -*-

import sys
import argparse

import lazyinit

def main():
	parser = argparse.ArgumentParser(description='Scaffold some projects')
	subparsers = parser.add_subparsers(metavar='<command>', prog='lazybones', help='init, create, destroy, build, run', dest='cmd')
	init = subparsers.add_parser('init')

	create = subparsers.add_parser('create')
	create.add_argument('-s', '--source', help='Creates a source file in appropriate dirs', metavar='<filename>')
	create.add_argument('-i', '--include', help='Creates a header/include file in appropriate dirs for C-family projects', metavar='<filename>')
	create.add_argument('-c', '--class', help='Creates a class (header & source) in the appropriate dirs for C-family projects', metavar='<filename>')

	destroy = subparsers.add_parser('destroy')
	destroy.add_argument('-s', '--source', help='Destroy a source file', metavar='<filename>')
	destroy.add_argument('-i', '--include', help='Destroy a header/include file', metavar='<filename>')
	destroy.add_argument('-c', '--class', help='Destroys a class (header & source)', metavar='<filename>')
	args = parser.parse_args()

	if args.cmd == 'init':
		lazyinit.init()
