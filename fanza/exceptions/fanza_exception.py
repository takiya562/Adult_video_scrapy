class ExtractException(Exception):
    def __init__(self, formatter: str, *args: object) -> None:
        super().__init__(*args)
        self.formatter = formatter
    
    def get_message(self) -> str:
        return self.formatter.format(*self.args)

if __name__ == '__main__':
    try:
        raise ExtractException('{} {}', 'Hello', 'World')
    except ExtractException as err:
        print(err.get_message())
