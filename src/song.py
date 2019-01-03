class Song:
    name = ""
    artist = ""
    album = ""
    id = ""
    name_size = 0

    def compare(self, x):
        if x.name_size < self.name_size:
            return True
        else:
            return False
