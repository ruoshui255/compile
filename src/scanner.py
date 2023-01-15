from src.token import TokenType, keywords, Token
from src.utils import error_compiler


class Scanner:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
        self.error = False

    def scan_tokens(self):
        while not self.at_end():
            self.start = self.current
            self.scan_token()

        self.add_token(TokenType.EOF, None)
        return self.tokens

    def scan_token(self):
        c: str = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                type = TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                self.add_token(type)
            case "=":
                type = TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                self.add_token(type)
            case "<":
                type = TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                self.add_token(type)
            case ">":
                type = TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                self.add_token(type)
            case "/":
                if self.match("/"):
                    # comment
                    while self.peek() != "\n" and (not self.at_end()):
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | " \r" | "\t":
                return
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case "o":
                if self.match("r"):
                    self.add_token(TokenType.OR)
                else:
                    self.report_error(self.line, "o args error")
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    self.report_error(self.line, "Unexpected character")

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def peek(self):
        if self.at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current+1]

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def match(self, expected):
        if self.at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def at_end(self):
        return self.current >= len(self.source)

    def string(self):
        while self.peek() != '"' and (not self.at_end()):
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.at_end():
            self.report_error(self.line, "Unterminated string.")
            return

        # the closing "
        self.advance()

        value = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            # consume the "."
            self.advance()
            while self.peek().isdigit():
                self.advance()
        number = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, number)

    def identifier(self):
        while self.peek().isdigit() or self.peek().isalpha():
            self.advance()

        text = self.source[self.start: self.current]
        type = keywords.get(text, None)
        if type is None:
            type = TokenType.IDENTIFIER
        self.add_token(type)

    def report_error(self, token, msg):
        error_compiler(token, msg)
        self.error = True
