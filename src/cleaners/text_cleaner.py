from . import *

class TextCleaner:
    """Class to clean words and sentences"""

    def __init__(
        self,
        use_lemmatizer: bool = False,
    ):
        """initializes the lemmatizer model from spacy"""
        if use_lemmatizer:
            spacy_download_command = "pip install spacy && python -m spacy download en_core_web_sm"
            import os

            os.system(spacy_download_command)
            import spacy

            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    def lemmatize_word(self, word: str) -> str:
        """Method to lemmatize a word

        Args:
            word (str): Original/Unclean version of the word

        Returns:
            str: Lemmatized word
        """
        return [token.lemma_ for token in self.nlp(word)][0]  # find lemma of the word
    
    def word_eliminator(self, text):
        non_ascii_pattern = re.compile(r'[^\x00-\x7F]+')
        text = non_ascii_pattern.sub('', text)

        # Remove words starting with '@' or '#'
        text = re.sub(r'\B[@#]\w+', '', text)

        # Remove URLs starting with 'http' or 'www'
        text = re.sub(r'http\S+|www\.\S+', '', text)

        return text

    def clean_sentences(
        self,
        og_sentences: list,
        more_stops: list = list(),
        lemmatize: bool = False,
    ) -> tuple:
        stops = stopwords.words("english")
        stops.extend(more_stops) if more_stops else None

        cleaning_phase = [
            str(re.sub(" +", " ", sentence)).strip() for sentence in og_sentences
        ]
        cleaining_phase = [self.word_eliminator(sentence) for sentence in cleaning_phase]
        cleaning_phase = [
            sentence.translate(
                str.maketrans(string.punctuation, " " * len(string.punctuation))
            )
            for sentence in cleaning_phase
        ]
        cleaning_phase = [
            re.sub("(\r\n)|[0-9]", "", sentence) for sentence in cleaning_phase
        ]
        cleaning_phase = [
            sentence.replace("®", "").replace("", "").replace("Ã", "").lower()
            for sentence in cleaning_phase
        ]
        cleaning_phase = [
            str(re.sub(" +", " ", sentence)).strip() for sentence in cleaning_phase
        ]
        useful_sentences = []
        useful_words = []

        for sentence, og_sent, index in zip(
            cleaning_phase, og_sentences, range(len(og_sentences))
        ):
            words = []
            for word in sentence.split():
                if word not in stops:
                    if lemmatize == True:
                        word = self.lemmatize_word(word)
                    if word not in words:
                        words.append(word.strip())

            sentence = " ".join(words)

            if sentence not in useful_sentences and words not in useful_words:
                useful_sentences.append(sentence)
                useful_words.extend(words)

        useful_sentences = [text for text in useful_sentences if text]

        return useful_sentences, useful_words