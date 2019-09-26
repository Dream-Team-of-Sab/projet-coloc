def file_to_dict(filename):
    result = dict()
    with open(filename) as f:
        for line in f:
            (key, value) = [a.strip() for a in line.split('=')]
            result.update({key : value})
    return result

class Config:
    def __init__(self, paramDict={}):
        self._dictionary = paramDict

    def param(self, key):
        return self._dictionary[key]
