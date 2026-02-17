import uuid


class CRDTCharacter:

    def __init__(self, char, position, char_id=None):

        self.char = char

        self.position = position

        self.id = char_id or str(uuid.uuid4())

        self.deleted = False


class CRDTDocument:

    def __init__(self):

        self.characters = []


    def insert(self, position, char):

        new_char = CRDTCharacter(char, position)

        if position >= len(self.characters):

            self.characters.append(new_char)

        else:

            self.characters.insert(position, new_char)

        return new_char


    def delete(self, position):

        if position < len(self.characters):

            self.characters[position].deleted = True


    def get_text(self):

        return "".join(

            c.char for c in self.characters

            if not c.deleted
        )


    def load_text(self, text):

        self.characters = []

        for i, char in enumerate(text):

            self.characters.append(

                CRDTCharacter(char, i)
            )
