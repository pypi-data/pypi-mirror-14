"""
Copyright 2016 Gu Zhengxiong <rectigu@gmail.com>

This file is part of BinTut.

BinTut is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BinTut is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BinTut.  If not, see <http://www.gnu.org/licenses/>.
"""


from binascii import hexlify
from sys import exit
from time import sleep
from cmd import Cmd

try:
    import gdb
except ImportError:
    pass
from colorama import Back

from .helpers import get_bits
from .utils import cyan, green, red, yellow


def print_stack():
    bits = get_bits()
    sp = '$esp' if bits == 32 else '$rsp'
    count = 32
    before = (count*4) / 2
    stack = gdb.execute(
        'x/{}wx {}-{}'.format(count, sp, int(before)),
        to_string=True)
    repr_stack(stack, Register().sp)
    print()


def repr_stack(stack, sp):
    for line in stack.splitlines():
        addr, values = line.split(':')
        values = ' '.join(values.split())
        if addr == sp:
            print(Back.GREEN + red(addr, res=False), yellow(values))
        else:
            print(red(addr), cyan(values))


def print_asm():
    frame = gdb.selected_frame()
    arch = frame.architecture()
    pc = frame.pc()
    asms = arch.disassemble(pc, pc+32)
    found = False
    for index, asm in enumerate(asms):
        if asm['addr'] == pc:
            before = asms[index-8:index]
            just = asms[index]
            after = asms[index+1:index+1+8]
            for one in before + [just] + after:
                print(repr_asm(one, pc))
            found = True
            break
    if not found:
        raise RuntimeError('pc not found')

def repr_asm(asm, pc):
    child = gdb.selected_inferior()
    mem = child.read_memory(asm['addr'], asm['length'])
    line = '{:25} {:25} {}'.format(
        cyan(hex(asm['addr']), res=False),
        green(hexlify(mem).decode('utf-8'), res=False),
        red(asm['asm']), res=False)
    if asm['addr'] == pc:
        return Back.GREEN + line
    else:
        return line


def print_reg():
    print(Register())


class Register(object):
    def __init__(self):
        reg_info = gdb.execute('info registers', to_string=True)
        names = []
        for one in reg_info.splitlines():
            name, value, dummy_desc = one.split(None, 2)
            setattr(self, name, value)
            if name in ['esp', 'rsp']:
                setattr(self, 'sp', value)
            if name in ['ebp', 'rbp']:
                setattr(self, 'bp', value)
            if name in ['eip', 'rip']:
                setattr(self, 'ip', value)
            names.append(name)

    def __repr__(self):
        try:
            return 'RIP: {} RSP: {} RBP: {}\n'.format(
                self.rip, self.rsp, self.rbp)
        except AttributeError:
            return 'EIP: {} ESP: {} EBP: {}\n'.format(
                self.eip, self.esp, self.ebp)


def redisplay(burst=False, course=None, repl=True, target=None):
    try:
        dummy_bits = get_bits()
    except gdb.error as error:
        print(error)
        exit(0)
    gdb.execute('shell clear')
    course = course if course else ''
    course += ' @ ' + target if target else ''
    if burst:
        print(red('==> Burst Mode: {}\n'.format(course)))
    else:
        print(yellow('==> Single Mode: {}\n'.format(course)))
    try:
        print_stack()
        print_reg()
        print_asm()
    except gdb.MemoryError:
        pass
    if burst:
        sleep(0.2)
    elif repl:
        try:
            print()
            REPL().cmdloop()
        except Exception as error:
            print(error)
            exit(1)


class REPL(Cmd):
    prompt = yellow('>>> ')

    @staticmethod
    def do_EOF(dummy):
        return True

    @staticmethod
    def do_quit(dummy):
        return True

    def do_redis(self, dummy_line):
        redisplay(repl=False)

    def default(self, line):
        try:
            output = gdb.execute(line, to_string=True)
        except gdb.error as error:
            print(red('Error executing command: {}'.format(line)))
            print(error)
        else:
            print(output)
