#!/usr/bin/python3
import math
import decimal
import json
import enum
import re
import logging
prompt = ">>>"
goodbye = "Have a nice day!"


class StackError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class stackRPN():
    """A class that implements RPN math notation."""

    def __init__(self):
        self.stack = []
        # arbitrary ID's for different types of functions
        # they MUST be different
        # basically an enum because reasons
        self.expr_types = enum.Enum(
            "expr_types", "arithmetic stackop function constant")
        self.arithmetic = 0
        self.stackop = 1
        self.function = 2
        self.constant = 3
        expr_types = self.expr_types
        # defines which input strings run which commands
        # string for function,[actual function, category of function,num.
        # of required arguments]
        self.cmddict = {
            # string command : [ func. ref., func. category, num. args]
            'sin': [math.sin, expr_types.function, 1],
            'cos': [math.cos, expr_types.function, 1],
            'tan': [math.tan, expr_types.function, 1],
            'asin': [math.asin, expr_types.function, 1],
            'acos': [math.acos, expr_types.function, 1],
            'atan': [math.atan, expr_types.function, 1],
            'sqrt': [math.sqrt, expr_types.function, 1],
            'exp': [self.stackEXP, expr_types.arithmetic, 2],
            '^': [self.stackEXP, expr_types.arithmetic, 2],
            'deg': [math.degrees, expr_types.function, 1],
            'rad': [math.radians, expr_types.function, 1],
            'log': [math.log, expr_types.function, 1],
            'ln': [math.log, expr_types.function, 1],
            '+': [self.stackAdd, expr_types.arithmetic, 2],
            '*': [self.stackMult, expr_types.arithmetic, 2],
            '-': [self.stackSubtract, expr_types.arithmetic, 2],
            '/': [self.stackDiv, expr_types.arithmetic, 2],
            'neg': [self.stackNEG, expr_types.stackop, 1],
            'n': [self.stackNEG, expr_types.stackop, 1],
            'inv': [self.stackINV, expr_types.arithmetic, 1],
            'pi': [(lambda: math.pi), expr_types.constant, 0],
            'e': [(lambda: math.e), expr_types.constant, 0],
            'swap': [self.stackSWAP, expr_types.stackop, 2],
            's': [self.stackSWAP, expr_types.stackop, 2],
            'drop': [self.stackDROP, expr_types.stackop, 1],
            'dr': [self.stackDROP, expr_types.stackop, 1],
            'dd': [self.stackDROP, expr_types.stackop, 1],
            'dropn': [self.stackDROPN, expr_types.stackop, 1],
            'dup': [self.stackDUP, expr_types.stackop, 1],
            'd': [self.stackDUP, expr_types.stackop, 1],
            'rot': [self.stackROT, expr_types.stackop, 3],
            'clean': [self.stackCLEAN, expr_types.stackop, 0],
            'ddup': [self.stackDDUP, expr_types.stackop, 2],
            'dupn': [self.stackDUPN, expr_types.stackop, 1],
            'help': [self.stackHELP, expr_types.stackop, 0],
            "exit": [self.stackEXIT, expr_types.stackop, 0],
            "quit": [self.stackEXIT, expr_types.stackop, 0]
        }

        # these lists serve as categories, although there's probably a better
        # way to do this
        # FIXED! I now have the category of the function in the dictionary itself!
        # All hail the 1337 H4X0R!
        # self.arithmetic = ['+','-','*','/']
        # self.functions = ['sin','cos','tan','asin','acos','atan','sqrt','exp','deg','rad','log']
        # self.constants = ['pi','e']
        # self.stackops = ['swap','drop','dup','rot','clean','ddup']

    def cmd(self, c):
        """\nRun a command"""
        # retrieve the type of the function
        ctype = self.cmddict[c][1]
        # create an alias for the function from the dictionary
        command = self.cmddict[c][0]
        # retrieve required number of aguments
        numargs = self.cmddict[c][2]

        oldstack = self.getStack()

        # handle the case of generic functions from other libraries
        try:
            if ctype == self.expr_types.function:
                    # the command will receive one value as an argument
                self.stack.append(decimal.Decimal(command(self.stack.pop())))
                # For some reason, None appears in the stack sometimes, so
                # clean it

            # if stack has more than one item
            elif (ctype == self.expr_types.arithmetic):
                # if stack has more than one item
                # if len(self.stack) > numargs - 1:
                # 		command()
                    # run command corresponding to input
                self.stack.append(decimal.Decimal(command()))
            elif (ctype == self.expr_types.stackop):
                command()
            # if command is a constant
            elif ctype == self.expr_types.constant:
                self.stack.append(decimal.Decimal(command()))
        except IndexError as e:
            self.setStack(oldstack)
            raise StackError("Invalid arguments for that function.")

    def interpret(self, s):
        """
        The workhorse of the object.
        Interprets lines of input as commands or numeric input or other
        functions.
        """
        # for sym in ['+','-','*','/']:
        # 	s = s.replace(sym,' ' + sym)
        # print('s:',s)
        results = re.split(r"(\+|\*|\-|\-|\/|[\s+])", s)
        logging.debug(results)
        for i in results:
            # print('i:',i)
            # if input not a command in the dictionary
            if not i.isspace() and i != "" and not (i.lower() in self.cmddict.keys()):
                # if command is a number
                if i.replace(' ', '').replace('.', '').isdigit():
                    # add the typed number to the stack
                    print("Pushed:", i)
                    self.stack.append(decimal.Decimal(i))
                else:
                    raise ValueError("Invalid command!")
            # otherwise run the associated command
            elif (i.lower() in self.cmddict):
                self.cmd(i)

    def stackINV(self):
        """
        Calculates the reciprocal of the value in the bottom register.
        """
        args = 1
        a = self.stack.pop()
        a = 1 / a
        return a

    def stackNEG(self):
        self.stack.append(-self.stack.pop())

    def stackAdd(self):
        """\nAdds the bottom two numbers of the stack"""
        try:
            args = 2
            a, b = self.stack.pop(), self.stack.pop()
            return b + a
        except IndexError:
            raise StackError("Not enough values for addition.")

    def stackSubtract(self):
        """\nSubtracts the bottom two values in the stack"""
        args = 2
        a, b = self.stack.pop(), self.stack.pop()
        return b - a

    def stackMult(self):
        """\nMultiplies the bottom two values in the stack"""
        a, b = self.stack.pop(), self.stack.pop()
        return (b * a)

    def stackDiv(self):
        """\nDivides the bottom two values in the stack"""
        a, b = self.stack.pop(), self.stack.pop()
        return(decimal.Decimal(b) / decimal.Decimal(a))

    def stackEXP(self):
        """\nRaises the number in the second to last register the the power of the last register"""
        # this command is different because it sort of takes two values
        args = 2
        exp, num = self.stack.pop(), self.stack.pop()
        num = num**exp
        return(num)
        # print("test")

    def getStack(self):
        """\nReturns the stack as a list"""
        return self.stack[:]

    def setStack(self, l):
        """\nSets the stack. Expects a list."""
        self.stack = l[:]

    def stackDUP(self):
        """\nDuplicates the bottom value of the stack"""
        args = 2
        self.stack.append(self.stack[-1])

    def stackDUPN(self):
        """\nDuplicates the bottom N items on the stack"""
        old = self.stack[:]
        try:
            n = int(self.stack.pop())
            args = [self.stack.pop() for i in range(n)]
            args = args[:] + args[:]
            self.stack = self.stack + args
        except IndexError:
            self.stack = old[:]
            raise StackError()

    def stackDROP(self):
        """\nDeletes the bottom value of the stack"""
        del self.stack[-1]

    def stackDROPN(self):
        """\nDeletes the bottom value of the stack"""
        old = self.stack[:]
        n = self.stack.pop()
        try:
            for i in range(int(n)):
                self.stack.pop()
        except IndexError:
            self.stack = old[:]
            raise StackError()

    def stackSWAP(self):
        """\nSwaps the bottom two values of the stack"""
        args = 2
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def stackROT(self):
        """\nRotates the bottom 3 values of the stack"""
        # shuffle the values around, easy peasy
        args = 3
        self.stack[-1], self.stack[-2], self.stack[-3] = self.stack[-2], self.stack[-3], self.stack[-1]

    def stackCLEAN(self):
        """\nClean any invalid values from the stack"""
        if None in self.stack:
            self.stack.remove(None)

    def stackDDUP(self):
        """\nDuplicate the bottom 2 items in the stack"""
        args = 2
        a, b = self.stack.pop(), self.stack.pop()
        self.stack += [b, a, b, a]
        # for i in [b,a,b,a]:
        # 	self.stack.append(i)

    def stackEXIT(self):
        exit()

    def stackHELP(self):
        """
        Print out commands
        """
        args = 0
        print("Welcome to the RPN calculator in Python!\nEnter math functions and arithmetic operators in RPN.\nHere are some commands:")
        for i in sorted(self.cmddict.keys()):
            try:
                print("<\'{0}\':{1}>\n".format(i, self.cmddict[i][0].__doc__))
            except AttributeError:
                print("<No help available.>\n")

    def __str__(self):
        curstack = self.getStack()
        return '\n'.join(["{0} : {1}".format(len(curstack) - i, curstack[i]) for i in range(0, len(curstack))])


def main():
    """\nRun in interactive mode"""
    # create an instance of RPN
    instance = stackRPN()
    try:
        # with open("settings.json") as f:
            # print(f.read())
            # settings = json.load(f)
        settings = {
            "prompt": ">>>",
            "goodbye": "Have a nice day!"
        }
    except FileNotFoundError:
        print("Settings file not found. Creating it with defaults...")
        with open("settings.json", 'w') as f:
            settings = {'prompt': '>>>', 'goodbye': 'Have a nice day!'}
            f.write(json.dumps(settings))

    prompt = settings['prompt']
    goodbye = settings['goodbye']

    print("Welcome the command line RPN calculator!\nType 'help' for a list of functions.")
    while True:
        toExit = False
        # get input from the user
        try:
            userinput = input('>>>')
            if userinput in ['exit', 'quit']:
                print("Have a nice day!")
                toExit = True
        except:
            print("\nHave a nice day!")
            exit()
            toExit = True
        # give that input to the stack
        try:
            instance.interpret(userinput)
        except (StackError, ValueError) as e:
            print(e)
        # get the current stack
        newlist = instance.getStack()
        # print out the stack
        print("Current stack:")
        print(instance)

        if toExit:
            logging.info(instance)
            exit()

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    main()
