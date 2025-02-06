from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


def extraction_summ(text):
    if len(sent_tokenize(text)) < 90:
        num_sentences = int(0.4 * len(sent_tokenize(text)))
    else:
        num_sentences = int(0.2 * len(sent_tokenize(text)))
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    lsa_summarizer = LsaSummarizer()
    summary = lsa_summarizer(parser.document, num_sentences)
    summary_text = ' '.join(str(sentence) for sentence in summary)
    return summary_text
