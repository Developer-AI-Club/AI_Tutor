import openai
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
openai.api_key = "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"


user = input("Type something: ")
# if user.lower() == "exit":
#     break
prompt = f"Summarize the Wikipedia page for {user}"

response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=3500,
    temperature=0.5,
    top_p=1.0,
)

summary = response["choices"][0]["text"]

def summarize_text(text, num_sentences):
    # parse the text into a document object
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # create a summarizer using the LexRank algorithm
    summarizer = LexRankSummarizer()

    # summarize the document and return the specified number of sentences
    summary = summarizer(parser.document, num_sentences)

    # return the summary as a list of strings
    return [str(sentence) for sentence in summary]

summary = summarize_text(summary, 7)
print(summary)
