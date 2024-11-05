import boto3
import PyPDF2
import spacy
import re

class TextUtils:

    def __init__(self):
        self.s3 = boto3.client('s3')
        self.pypdf = PyPDF2.PdfReader

    def extract_text_from_pdf(self, caminho):
        # lê o arquivo local
        with open(caminho, 'rb') as file:
            reader = self.pypdf(file)
            text = ''
            
            # Percorre cada página do PDF
            for page in reader.pages:
                # Extrai o texto da página
                page_text = page.extract_text()
                
                # Verifica se o texto é None antes de concatenar
                if page_text:
                    text += page_text
                else:
                    print(f"Aviso: A página {reader.pages.index(page)} está vazia ou não pôde ser lida.")
                    
            return text

    def preprocess_text(text):

        custom_stop_words = {'que', 'na', 'da', 'de'}

        nlp = spacy.load('pt_core_news_sm')
        # Remove pontuação e números
        text = re.sub(r'[^\w\s]', '', text)
        # Cria um objeto Doc do spaCy e aplica lematização
        doc = nlp(text)
        # Remove stopwords e aplica lematização
        text = ' '.join(token.lemma_ for token in doc if not token.is_stop and token.text.lower(
        ) not in custom_stop_words)
        return text
