import pymorphy2


class Tokenizer():

    def __init__(self):
        self._meaningless_lexemes = ['CONJ', 'PREP', None]  # conjunctions, prepositions, empty words
        self._morph = pymorphy2.MorphAnalyzer()

    def tokenize(self, text):
        result = []
        for word in text.replace('\n', ' ').split(' '):
            parsed_word = self._morph.parse(''.join(filter(str.isalpha, word)))[0]
            if parsed_word.tag.POS not in self._meaningless_lexemes:
                result.append(parsed_word.normal_form)
        return result
