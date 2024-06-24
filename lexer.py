import string

# /////////////// ALFABET ///////////////
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS


# /////////////// ERROR ///////////////
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as__string(self):
        result = f"{self.error_name}: {self.details}"
        return result


class ShowError(Error):
    def __init__(self, details):
        super().__init__('ERROR', details)


# /////////////// TOKEN //////////////
TC_INT = 'INT'
TC_DOUBLE = 'DOUBLE'
TC_IDENTIFIER = 'IDENTIFIER'
TC_KEYWORD = 'KEYWORD'
TC_EQ = 'EQ'
TC_PLUS = 'PLUS'
TC_MINUS = 'MINUS'
TC_TIMES = 'TIMES'
TC_DIVIDE = 'DIVIDE'
TC_PLUSPLUS = 'PLUSPLUS'
TC_OPENPAREN = 'OPENPARENTHESES'
TC_CLOSEPAREN = 'CLOSEPARENTHESES'
TC_OPENBRACE = 'OPENBRACE'
TC_CLOSEBRACE = 'CLOSEBRACE'
TC_SEMICOLON = 'SEMICOLON'
TC_NEQ = 'NEQ'
TC_EQEQ = 'EQEQ'
TC_GTEQ = 'GTEQ'
TC_LTEQ = 'LTEQ'
TC_GT = 'GT'
TC_LT = 'LT'
TC_GET = 'GET'
TC_PRINT = 'PRINT'
TC_IF_ELSE = 'IF_ELSE'
TC_FOR = 'FOR'
TC_STRING = 'STRING'

KEYWORDS = {
    'get': TC_GET,
    'print': TC_PRINT,
    'if': TC_IF_ELSE,
    'for': TC_FOR,
    'else': TC_IF_ELSE,
    'int': TC_INT,
    'double': TC_DOUBLE,
}


class Token:
    def __init__(self, _type_, value=None):
        self.type = _type_
        self.value = value

    def __repr__(self):
        if self.value: return f'<{self.type}: {self.value}>'
        return f'<{self.type}>'


# /////////////// LEXER ///////////////
class Lexer:

    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.text = file.read()
        self.pos = -1
        self.in_string = False
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in ' \n':
                self.advance()
            elif self.current_char in ' ':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                self.advance()
                if self.current_char == '+':
                    tokens.append(Token(TC_PLUSPLUS))
                    self.advance()
                else:
                    tokens.append(Token(TC_PLUS))
            elif self.current_char == '-':
                tokens.append(Token(TC_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TC_TIMES))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TC_DIVIDE))
                self.advance()
            elif self.current_char == '\\':
                self.advance()
                if self.current_char == '*':  # تشخیص کامنت‌های چندخطی
                    self.advance()
                    self.skip_comment()
            elif self.current_char == '++':
                tokens.append(Token(TC_PLUSPLUS))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TC_OPENPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TC_CLOSEPAREN))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TC_OPENBRACE))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TC_CLOSEBRACE))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TC_SEMICOLON))
                self.advance()
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TC_EQEQ))
                    self.advance()
                else:
                    tokens.append(Token(TC_EQ))
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TC_NEQ))
                    self.advance()
                else:
                    return [], ShowError("'!' can only be used as '!='")
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TC_GTEQ))
                    self.advance()
                else:
                    tokens.append(Token(TC_GT))
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TC_LTEQ))
                    self.advance()
                else:
                    tokens.append(Token(TC_LT))
            elif self.current_char == '"':
                tokens.append(self.make_string())
            else:
                char = self.current_char
                self.advance()
                return [], ShowError("'" + char + "'")
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        # Check for leading zero
        if self.current_char == '0':
            self.advance()
            if self.current_char and self.current_char in DIGITS:
                return 'ERROR', ShowError("Leading zeros are not allowed")

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TC_INT, int(num_str)), None
        else:
            # Check if there's no digit after dot
            if num_str.endswith('.'):
                return 'ERROR', ShowError("Numbers must not end with a dot")
            return Token(TC_DOUBLE, float(num_str)), None

    def make_identifier(self):
        identifier_str = ''

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            identifier_str += self.current_char
            self.advance()

        token_type = KEYWORDS.get(identifier_str, TC_IDENTIFIER)
        return Token(token_type, identifier_str)

    def skip_comment(self):
        while self.current_char is not None:
            if self.current_char == '*':
                self.advance()
                if self.current_char == '\\':
                    self.advance()
                    break
            else:
                self.advance()

    def make_string(self):
        string_str = ''
        self.advance()
        self.in_string = True

        while self.current_char is not None:
            if self.current_char == '"':
                self.advance()
                self.in_string = False
                return Token(TC_STRING, string_str)
            else:
                string_str += self.current_char
                self.advance()
        return 'ERROR'


# /////////////// RUN ///////////////
def run(file_path):
    lexer = Lexer(file_path)
    tokens, error = lexer.make_tokens()
    return tokens, error
# Run the lexer on a file
file_path = r'code.text'
tokens, error = run(file_path)
if error:
    print(error.as__string())
else:
    for token in tokens:
        print(token)



# import string
#
# # /////////////// ALPHABET ///////////////
# DIGITS = '0123456789'
# LETTERS = string.ascii_letters
# LETTERS_DIGITS = LETTERS + DIGITS
#
#
# # /////////////// ERROR ///////////////
# class Error:
#     def __init__(self, error_name, details):
#         self.error_name = error_name
#         self.details = details
#
#     def as_string(self):
#         result = f"{self.error_name}: {self.details}"
#         return result
#
#
# class ShowError(Error):
#     def __init__(self, details):
#         super().__init__('ERROR', details)
#
#
# # /////////////// TOKEN //////////////
# TC_INT = 'INT'
# TC_DOUBLE = 'DOUBLE'
# TC_IDENTIFIER = 'IDENTIFIER'
# TC_KEYWORD = 'KEYWORD'
# TC_EQ = 'EQ'
# TC_PLUS = 'PLUS'
# TC_MINUS = 'MINUS'
# TC_TIMES = 'TIMES'
# TC_DIVIDE = 'DIVIDE'
# TC_PLUSPLUS = 'PLUSPLUS'
# TC_OPENPAREN = 'OPENPAREN'
# TC_CLOSEPAREN = 'CLOSEPAREN'
# TC_OPENBRACE = 'OPENBRACE'
# TC_CLOSEBRACE = 'CLOSEBRACE'
# TC_SEMICOLON = 'SEMICOLON'
# TC_NEQ = 'NEQ'
# TC_EQEQ = 'EQEQ'
# TC_GTEQ = 'GTEQ'
# TC_LTEQ = 'LTEQ'
# TC_GT = 'GT'
# TC_LT = 'LT'
# TC_GET = 'GET'
# TC_PRINT = 'PRINT'
# TC_IF_ELSE = 'IF_ELSE'
# TC_FOR = 'FOR'
# TC_STRING = 'STRING'
#
# KEYWORDS = {
#     'get': TC_GET,
#     'print': TC_PRINT,
#     'if': TC_IF_ELSE,
#     'for': TC_FOR,
#     'else': TC_IF_ELSE,
#     'int': TC_INT,
#     'double': TC_DOUBLE,
# }
#
#
# class Token:
#     def __init__(self, _type_, value=None):
#         self.type = _type_
#         self.value = value
#
#     def __repr__(self):
#         if self.value: return f'<{self.type}: {self.value}>'
#         return f'<{self.type}>'
#
# # /////////////// LEXER ///////////////
# class Lexer:
#     def __init__(self, file_path):
#         with open(file_path, 'r') as file:
#             self.text = file.read()
#         self.pos = -1
#         self.current_char = None
#         self.advance()
#
#     def advance(self):
#         self.pos += 1
#         self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
#
#     def make_tokens(self):
#         tokens = []
#         while self.current_char is not None:
#             if self.current_char in ' \t\n':
#                 self.advance()
#             elif self.current_char in DIGITS:
#                 token, error = self.make_number()
#                 if error:
#                     return [], error
#                 tokens.append(token)
#             elif self.current_char in LETTERS:
#                 tokens.append(self.make_identifier())
#             elif self.current_char == '+':
#                 self.advance()
#                 if self.current_char == '+':
#                     tokens.append(Token(TC_PLUSPLUS))
#                     self.advance()
#                 else:
#                     tokens.append(Token(TC_PLUS))
#             elif self.current_char == '-':
#                 tokens.append(Token(TC_MINUS))
#                 self.advance()
#             elif self.current_char == '*':
#                 tokens.append(Token(TC_TIMES))
#                 self.advance()
#             elif self.current_char == '/':
#                 tokens.append(Token(TC_DIVIDE))
#                 self.advance()
#             elif self.current_char == '\\':
#                 self.advance()
#                 if self.current_char == '*':  # تشخیص کامنت‌های چندخطی
#                     self.advance()
#                     self.skip_comment()
#             elif self.current_char == '(':
#                 tokens.append(Token(TC_OPENPAREN))
#                 self.advance()
#             elif self.current_char == ')':
#                 tokens.append(Token(TC_CLOSEPAREN))
#                 self.advance()
#             elif self.current_char == '{':
#                 tokens.append(Token(TC_OPENBRACE))
#                 self.advance()
#             elif self.current_char == '}':
#                 tokens.append(Token(TC_CLOSEBRACE))
#                 self.advance()
#             elif self.current_char == ';':
#                 tokens.append(Token(TC_SEMICOLON))
#                 self.advance()
#             elif self.current_char == '=':
#                 self.advance()
#                 if self.current_char == '=':
#                     tokens.append(Token(TC_EQEQ))
#                     self.advance()
#                 else:
#                     tokens.append(Token(TC_EQ))
#             elif self.current_char == '!':
#                 self.advance()
#                 if self.current_char == '=':
#                     tokens.append(Token(TC_NEQ))
#                     self.advance()
#                 else:
#                     return [], ShowError("'!' can only be used as '!='")
#             elif self.current_char == '>':
#                 self.advance()
#                 if self.current_char == '=':
#                     tokens.append(Token(TC_GTEQ))
#                     self.advance()
#                 else:
#                     tokens.append(Token(TC_GT))
#             elif self.current_char == '<':
#                 self.advance()
#                 if self.current_char == '=':
#                     tokens.append(Token(TC_LTEQ))
#                     self.advance()
#                 else:
#                     tokens.append(Token(TC_LT))
#             elif self.current_char == '"':
#                 token, error = self.make_string()
#                 if error:
#                     return [], error
#                 tokens.append(token)
#             else:
#                 char = self.current_char
#                 self.advance()
#                 return [], ShowError(f"Illegal character '{char}'")
#         return tokens, None
#
#     def make_number(self):
#         num_str = ''
#         dot_count = 0
#
#         # Check for leading zero
#         if self.current_char == '0':
#             self.advance()
#             if self.current_char and self.current_char in DIGITS:
#                 return None, ShowError("Leading zeros are not allowed")
#
#         while self.current_char != None and self.current_char in DIGITS + '.':
#             if self.current_char == '.':
#                 if dot_count == 1:
#                     break
#                 dot_count += 1
#             num_str += self.current_char
#             self.advance()
#
#         if dot_count == 0:
#             return Token(TC_INT, int(num_str)), None
#         else:
#             # Check if there's no digit after dot
#             if num_str.endswith('.'):
#                 return None, ShowError("Numbers must not end with a dot")
#             return Token(TC_DOUBLE, float(num_str)), None
#
#     def make_identifier(self):
#         identifier_str = ''
#         while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
#             identifier_str += self.current_char
#             self.advance()
#         token_type = KEYWORDS.get(identifier_str, TC_IDENTIFIER)
#         return Token(token_type, identifier_str)
#
#     def skip_comment(self):
#         while self.current_char is not None:
#             if self.current_char == '*':
#                 self.advance()
#                 if self.current_char == '\\':
#                     self.advance()
#                     break
#             else:
#                 self.advance()
#
#     def make_string(self):
#         string_str = ''
#         escape_character = False
#         self.advance()  # Skip the opening quote
#         while self.current_char is not None:
#             if escape_character:
#                 if self.current_char == 'n':
#                     string_str += '\n'
#                 elif self.current_char == 't':
#                     string_str += '\t'
#                 else:
#                     string_str += self.current_char
#                 escape_character = False
#             else:
#                 if self.current_char == '\\':
#                     escape_character = True
#                 elif self.current_char == '"':
#                     self.advance()
#                     return Token(TC_STRING, string_str), None
#                 else:
#                     string_str += self.current_char
#             self.advance()
#         return None, ShowError("Unterminated string")
#
# # /////////////// RUN ///////////////
# def run(file_path):
#     lexer = Lexer(file_path)
#     tokens, error = lexer.make_tokens()
#     return tokens, error
#
# # Run the lexer on a file
# file_path = r'code.txt'
# tokens, error = run(file_path)
# if error:
#     print(error.as__string())
# else:
#     for token in tokens:
#         print(token)

