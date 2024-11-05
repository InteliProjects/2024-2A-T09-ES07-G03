import unittest
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import re

# Função de pré-processamento
def preprocess_text(text):
    custom_stop_words = {'que', 'na', 'da', 'de'}
    nlp = spacy.load('pt_core_news_sm')
    # Remove pontuação e números
    text = re.sub(r'[^\w\s]', '', text)
    # Cria um objeto Doc do spaCy e aplica lematização
    doc = nlp(text)
    # Remove stopwords e aplica lematização
    text = ' '.join(token.lemma_ for token in doc if not token.is_stop and token.text.lower() not in custom_stop_words)
    return text

# Função a ser testada
def tagging(text):
    text = preprocess_text(text)
    vectorizer = TfidfVectorizer(ngram_range=(1, 3))  
    tfidf_matrix = vectorizer.fit_transform([text])  # O TF-IDF espera uma lista de textos
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    tfidf_scores = dict(zip(feature_names, scores))
    sorted_keywords = sorted(tfidf_scores.items(), key=lambda item: item[1], reverse=True)
    top_keywords = [keyword for keyword, score in sorted_keywords[:10]]  # Top 10 palavras-chave
    return top_keywords

# Classe de testes
class TestTaggingFunction(unittest.TestCase):

    def test_tagging_basic(self):
        # Teste com uma frase simples
        text = "O botafogo é o maior clube."

        # Chama a função a ser testada
        result = tagging(text)

        # Verifica se as palavras-chave estão corretas
        expected_keywords = ['botafogo', 'maior', 'clube']
        self.assertTrue(all(keyword in result for keyword in expected_keywords))

    def test_tagging_with_punctuation(self):
        text = "Fala fogão!! Este é um teste. Olá mundo?"

        result = tagging(text)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0) 

    def test_tagging_empty_text(self):
        text = ""

        result = tagging(text)

        self.assertEqual(result, [])

    def test_tagging_short_text(self):
        text = "Oi!"

        result = tagging(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "oi")

if __name__ == '__main__':
    unittest.main()