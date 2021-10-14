class ExtractException(Exception):
    def __init__(self, formatter: str, *args: object) -> None:
        super().__init__(*args)
        self.formatter = formatter
    
    def get_message(self) -> str:
        return self.formatter.format(*self.args)

class EmptyGenreException(Exception):
    def __init__(self, message, url):
        self.message = message
        self.url = url


class FormatException(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    try:
        raise ExtractException('{} {}', 'Hello', 'World')
    except ExtractException as err:
        print(err.get_message())
