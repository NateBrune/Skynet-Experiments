__author__ = 'NateBrune'

import sys
import random


class Brainfuck:
    """
    Brainfuck Spec
    --------------
    30k cells (bytes initialized to 0)
    Data pointer to a specific cell
    Only eight operators:
      < move data pointer one cell left
      > move data pointer one cell right
      + increment the cell at the current data pointer
      - decrement the cell at the current data pointer
      . output the cell at the current data pointer as a character
      , input the next character to the cell at the current data pointer
      [ if the cell at the current data pointer is zero, move the instruction pointer to the matching ]
      ] move the instruction pointer to the matching [

    Ignore characters other than +-.,[]<>
    Advance instruction pointer after each instruction
    A program halts by running off its end
    """
    
    def __init__(self):
        self.cells = [0] * 30000
        self.data_pointer = 0
        # For automating the process without in and out 
        self.inputs = []
        for i in range(0,256):
            self.inputs.append("a")
        self.outputs = []
        self.inIterator = 0
        self.outIterator = 0
        self.idol= "hey"

        # Fitness Score
        self.score = 256

    def _tokenize(self, str, level=0):
        tokens = []
        while len(str) > 0:
            token = str.pop(0)
            if token == '[':
                tokens.append(self._tokenize(str, level + 1))
            elif token == ']':
                return tokens
            else:
                tokens.append(token)
        if level is not 0:
            raise SyntaxError('Malformed expression')
        return tokens

    def eval(self, src):
        """ Iterative evaluator """
        self._eval(self._tokenize(list(src)))

    def _eval(self, program):
        # the program counter
        pc = 0

        while pc < len(program):
            # current operation
            op = program[pc]

            if op == '+':
                self.cells[self.data_pointer] += 1
            elif op == '-':
                self.cells[self.data_pointer] -= 1
            elif op == '>':
                self.data_pointer += 1
            elif op == '<':
                self.data_pointer -= 1
            elif op == '.':
                try:
                    self.outputs.append(chr(self.cells[self.data_pointer]))
                except:
                    pass
            elif op == ',':
                self.cells[self.data_pointer] = ord(self.inputs[self.inIterator])
            elif isinstance(op, list):
                if self.cells[self.data_pointer]:
                    self._eval(op)
                    # retry the loop again
                    pc -= 1
            else:
                raise SyntaxError("Unrecognized operator '" + op + "' at position ", pc)

            # always advance, as specified
            pc += 1
round = 0
Continue=True
scripts = []
for i in range(0,8):
    scripts.append(''.join(random.choice("+-<>.,") for _ in range(0, 30)))
while Continue:
    #input()
    round+=1
    if (round%1000)==0:
        print("ROUND: " + str(round))
        print("IDOL : " + Brainfuck().idol)
        print("______________________")
    fitBrainId=0
    fitBrainScore=0
    brains = []
    for i in range(0,8):
        brains.append(Brainfuck())
        try:
            brains[i].eval(scripts[i])
        except:
            pass
        for inc in range(0, len(brains[i].idol)):
            if(len(brains[i].outputs)>inc):
                brains[i].score += 256 - abs(ord(brains[i].outputs[inc]) - ord(brains[i].idol[inc]))
        brains[i].score-= abs((len(brains[i].outputs)-1)-(len(brains[i].idol)-1))*128
        if brains[i].score > fitBrainScore:
            fitBrainId=i
            fitBrainScore = brains[i].score
        else:
            pass
        if (round%1000)==0:
            print("Brain " + str(i) + " scored: " + str(brains[i].score) + " " + scripts[i])       
    winningScript=scripts[fitBrainId]
    scripts[0]=winningScript
    chance = random.randint(0, 1000)
    if chance == 1002:
        scripts[0] = ''.join(i if random.randint(0, 5) else random.choice("+-<>.,") for i in scripts[0])
        scripts[0] = scripts[0][:-1]
    if (round%1000)==0:
        print("Winning Strain:     " + winningScript)
    bf = Brainfuck()
    bf.eval(winningScript)
    finstr=[]
    for letter in bf.outputs:
        finstr.append(letter)
    if (round%1000)==0:
        print("Output: " + "".join(finstr) + "\n\n")
    for i in range(1,8):
        scripts[i] = winningScript
        scripts[i]=''.join(i if random.randint(0, 5) else random.choice("+-<>.,") for i in scripts[i])
        chance = random.randint(0, 15)
        for times in range(0, chance):
            scripts[i]+=random.choice("+-<>.,")
        if "".join(finstr)==Brainfuck().idol:
            print("Winner Found!")
            print("ROUND: " + str(round))
            print("IDOL : " + Brainfuck().idol)
            print("______________________")
            print("Brain " + str(fitBrainId) + " scored: " + str(fitBrainScore) + " " + winningScript)
            print("Output: " + "".join(finstr) + "\n\n")
            Continue=False
            break
    if (round%1000)==0:
        #input()
        pass