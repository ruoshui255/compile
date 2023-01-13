from src.scanner import TokenType, Scanner, Token


def test_token():
    source = "12 32 for (a+b)*2"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    expected = [
        Token(TokenType.NUMBER, "12", "", 1),
        Token(TokenType.NUMBER, "32", "", 1),
        Token(TokenType.FOR, "for", "", 1),
        Token(TokenType.LEFT_PAREN, "(", "", 1),
        Token(TokenType.IDENTIFIER, "a", "", 1),
        Token(TokenType.RIGHT_PAREN, ")", "", 1),
        Token(TokenType.PLUS, "+", "", 1),
        Token(TokenType.IDENTIFIER, "b", "", 1),
        Token(TokenType.STAR, "*", "", 1),
        Token(TokenType.NUMBER, "2", "", 1),
    ]

    print(len(tokens), len(expected))

    for index, t in enumerate(tokens):
        if tokens[index] != expected[index]:
            print(t)
            print(expected[index])


# def test_token():
#     pass

if __name__ == '__main__':
    test_token()

