class Result():
    def __init__(self,answer:str,guess:str):
        assert len(answer)==5 and len(guess)==5
        self.answer=answer.lower()
        self.guess=guess.lower()

        self.output=[0,0,0,0,0]
        self.ignorePos=[]
        self.markedLettersInAnswer=[]

        self.generateOutput()

    def letterInAnswer(self,l):
        return l in self.answer

    def guessMatches(self):
        return self.answer==self.guess

    def lettersInAnswer(self):
        output=[]
        for letter in self.guess:
            if self.letterInAnswer(self,letter):
                output.append(letter)
        return output

    def letterIsGreen(self,pos,l):
        return self.answer[pos]==l

    def letterIsYellow(self,pos,l):
        if self.letterIsGreen(pos,l): return False
        return l in self.answer

    def getPosInAnswer(self,l):
        return self.answer.find(l)

    def markLetterGreen(self,pos):
        self.output[pos]=2
        self.ignorePos.append(pos)
        self.markedLettersInAnswer.append(pos)

    def markLetterYellow(self,pos):
        self.output[pos]=1
        self.ignorePos.append(pos)      

    def duplicates(self):
        for letter in self.answer:
            if self.answer.count(letter) > 1:
                return True

    def generateOutput(self):
        if self.guessMatches():
            self.output=[2,2,2,2,2]
        for letter in enumerate(self.guess):
            if self.letterIsGreen(*letter):
                self.markLetterGreen(letter[0])
        if not self.duplicates():
            for letter in enumerate(self.guess):
                if letter[0] in self.ignorePos: continue
                if self.letterIsYellow(*letter):
                    self.markLetterYellow(letter[0])
        else:
            for letter in enumerate(self.guess):
                if letter[0] in self.ignorePos: continue
                if self.letterIsYellow(*letter):
                    for letter2 in enumerate(self.answer):
                        if letter2[1] == letter and self.output[letter2[0]]>0: continue
                        self.markLetterYellow(letter[0])
                    
class Wordldle():
    def __init__(self):
        try: 
            from datetime import datetime
            import random,sys
        except ModuleNotFoundError as e:
            raise Exception(
                "Required modules are missing. Exiting program.")
            
        self.datetime=datetime
        self.random=random
        self.sys=sys

        self.words,self.answers=self.interperetFiles()
        self.random.seed(str(self.datetime.utcnow().date()).replace("-",""))

        self.answer=self.answers[self.random.randint(0,len(self.answers)-1)]
        del self.answers

        self.answer="otter"

        self.guessCounter=0

        while self.guessCounter < 6:
            guess=self.guessInput()
            pattern=Result(self.answer,guess).output
            self.outputColors(guess,pattern)

    def outputColors(self,guess,pattern):
        colors=["\033[40m","\033[43m","\033[42m"]
        self.sys.stdout.write("\033[F")
        self.sys.stdout.flush()
        for letter in enumerate(guess):
            print(f"\033[1m{colors[pattern[letter[0]]]}{letter[1]}\033[0m",end="")
        print()

    def guessInput(self):
        while True:
            guess=input(f"Guess #{self.guessCounter+1}:\n\n").lower()
            if len(guess) == 5 and guess in self.words:
                self.guessCounter+=1
                return guess                
            print("Invalid guess, try again.")
            
    def interperetFiles(self):
        x=self.interperetCsv("words.txt")
        y=self.interperetCsv("answers.txt")
        return x,y

    def interperetCsv(self,path):
        with open(path,"r") as f: return f.read().split(",")

Wordldle()