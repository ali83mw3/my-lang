############CONSTANTS#####################

DIGITS = '0123456789'

#########################################
#~~~~~~~~~~~~~~~ERRORS~~~~~~~~~~~~~~~~~~~~
#########################################
class Error:
    def __init__(self, pos_start, pos_end, name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.name = name
        self.details = details
    
    def as_string(self):
        result = f'{self.name}: {self.details}'
        result += f'\nFile {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result
    
class IllegalCharError(Error):
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end,'Error Character', details)
        
#########################################
#~~~~~~~~~~~~~POSITION~~~~~~~~~~~~~~~~~~
#########################################

class Position:
    def __init__(self, index, ln, col, fn, ftxt):
        self.index = index
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    def advance(self, current_char):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col += 0
            
        return self

    def copy(self):
        return Position(self.index, self.ln, self.col, self.fn, self.ftxt)





#########################################
#~~~~~~~~~~~~~~TOKENS~~~~~~~~~~~~~~~~~~~~
#########################################

T_INT = 'T_INT'
T_FLOAT = 'FLOAT'
T_PLUS = 'PLUSE'
T_MINUS = 'MINUS'
T_MUL = 'MUL'
T_DIV = 'DIV'
T_LPAREN = 'LPAREN'
T_PRAREN = 'PRAPEN'
T_REMAIN = 'REMAIN'


class Token:
    def __init__(self,type,value=None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

############################################
#~~~~~~~~~~~~~~~~~LEXER~~~~~~~~~~~~~~~~~~~~~
############################################

class Lexer:
    def __init__(self,fn,text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
        
        
    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(T_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(T_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(T_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(T_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(T_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(T_PRAREN))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(T_REMAIN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                
                char = self.current_char
                self.advance()
                return [],IllegalCharError(pos_start,self.pos,":'" + char + "':")
            
        return tokens,None
    
    
    def make_number(self):
        num_str = ''
        dot_counter = 0
        
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_counter == 1:
                    break
                dot_counter += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_counter == 0:
            return Token(T_INT, int(num_str))
        else:
            return Token(T_FLOAT, float(num_str))
        return tokens

################################################
#~~~~~~~~~~~~~~~~~~~~RUN~~~~~~~~~~~~~~~~~~~~~~~
################################################

def run(fn,text):
    lexer = Lexer(fn,text)
    tokens ,error= lexer.make_tokens()
    
    return tokens,error
    