import logging
from typing import Iterator

logging.basicConfig(level=logging.INFO)


class SQLParser:
    def __init__(self, sql: str):
        self.sql = sql
        self.position = 0
        self.length = len(sql)

    def parse_statements(self) -> Iterator[str]:
        """Parse SQL into individual statements, properly handling functions and procedures."""
        buffer = []
        in_string = False
        string_char = None
        in_comment = False
        in_dollar_quotes = False
        dollar_quote_tag = None

        while self.position < self.length:
            char = self.sql[self.position]
            next_char = self.sql[self.position + 1] if self.position + 1 < self.length else None

            # Handle comments
            if not in_string and not in_dollar_quotes and char == '-' and next_char == '-':
                in_comment = True
            elif in_comment and char == '\n':
                in_comment = False
                buffer.append(char)

            # Handle strings
            elif not in_comment and not in_dollar_quotes and char in ["'", '"']:
                if not in_string:
                    in_string = True
                    string_char = char
                elif string_char == char:
                    if next_char == char:  # Handle escaped quotes
                        self.position += 1
                    else:
                        in_string = False
                buffer.append(char)

            # Handle dollar-quoted strings
            elif not in_string and not in_comment and char == '$':
                if not in_dollar_quotes:
                    # Look ahead for the dollar quote tag
                    tag_end = self.sql.find('$', self.position + 1)
                    if tag_end != -1:
                        dollar_quote_tag = self.sql[self.position:tag_end + 1]
                        in_dollar_quotes = True
                elif dollar_quote_tag:
                    # Check if this is the closing dollar quote
                    if self.sql[self.position:self.position + len(dollar_quote_tag)] == dollar_quote_tag:
                        in_dollar_quotes = False
                        dollar_quote_tag = None
                buffer.append(char)

            # Handle statement delimiter
            elif not in_string and not in_comment and not in_dollar_quotes and char == ';':
                buffer.append(char)
                statement = ''.join(buffer).strip()
                if statement:
                    yield statement
                buffer = []

            else:
                buffer.append(char)

            self.position += 1

        # Don't forget the last statement
        statement = ''.join(buffer).strip()
        if statement:
            yield statement
