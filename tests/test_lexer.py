from src.scanner import Scanner
from src.token import TokenType, Token


def test_token():
    source = "12 32 for (a+b)*2"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    expected = [
        Token(TokenType.NUMBER, "12", 12, 1),
        Token(TokenType.NUMBER, "32", 32, 1),
        Token(TokenType.FOR, "for", None, 1),
        Token(TokenType.LEFT_PAREN, "(", None, 1),
        Token(TokenType.IDENTIFIER, "a", None, 1),
        Token(TokenType.PLUS, "+", None, 1),
        Token(TokenType.IDENTIFIER, "b", None, 1),
        Token(TokenType.RIGHT_PAREN, ")", None, 1),
        Token(TokenType.STAR, "*", None, 1),
        Token(TokenType.NUMBER, "2", 2, 1),
        Token(TokenType.EOF, "11", None, 1),
    ]

    print(len(tokens), len(expected))

    for index, t in enumerate(tokens):
        if tokens[index] != expected[index]:
            print(f"res:    <{t}>\nexpect: <{expected[index]}>\n")
            # print(expected[index])


# def test_token():
#     pass

if __name__ == '__main__':
    test_token()

