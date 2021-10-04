class ExtractException(Exception):
    def __init__(self, message, url):
        self.message = message
        self.url = url


class EmptyGenreException(Exception):
    def __init__(self, message, url):
        self.message = message
        self.url = url


class FormatException(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    try:
        raise ExtractException('Extract sample error msg', 'sample.com')
    except ExtractException as err:
        print("catch exception\nmsg: {}\t url:{}".format(err.message, err.url))
