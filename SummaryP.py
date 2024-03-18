import nltk
import pandas as pd
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

#Citim datele din fisierul csv
df = pd.read_csv('search_results.csv')
#print(df)

#lista cuvintelor cheie
cuvinte_cheie = ['because', 'why', 'how']

#initializam spacy pentru analiza semantica
nlp = spacy.load('en_core_web_sm')

#initializam sumarizatorul TextRank
sumarizator = TextRankSummarizer()


for index, row in df.iterrows():
    #extragem paragrafele pe rând
    paragrafe = row['paragrafe'].split('\n') if isinstance(row['paragrafe'], str) else []

    #parcurgem fiecare paragraf
    for paragraf in paragrafe:

        #verificam daca paragraful contine una dintre cuvintele cheie
        if any(cuvant_cheie in paragraf for cuvant_cheie in cuvinte_cheie):
            #tokenizam paragraful pentru a-l pregati pentru sumarizare
            parser = PlaintextParser.from_string(paragraf, Tokenizer('english'))

            #sumarizam paragraful folosind TextRank
            rezumat = sumarizator(parser.document, 4) #sumarizam in 4 propozitii
            print("Titlu:", row['titlu'])
            print("Link:", row['link'])
            print("Paragraf original:", paragraf)
            print("Rezumat:", "\n".join(str(prop) for prop in rezumat))
            print("\n")
