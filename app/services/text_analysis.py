# app/services/text_analysis.py
# pylint: disable=C

class TextAnalysis:
    """Serviço para análise de texto"""

    @staticmethod
    def analisar_caminhos(caminhos):
        """Realiza análise básica nos caminhos"""
        return {
            "total_caminhos": len(caminhos),
            "detalhes": [{"caminho": c} for c in caminhos],
        }

def analyze_text(text):
    """
    Analisa um texto fornecido.
    :param text: str
    :return: dict
    """
    words = text.split()
    char_count = len(text)
    word_count = len(words)

    return {
        "original_text": text,
        "char_count": char_count,
        "word_count": word_count,
        "words": words
    }
