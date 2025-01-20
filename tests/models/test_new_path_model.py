import unittest
from app.models.new_path_model import AnalisadorCaminhoString, PathData


class TestAnalisadorCaminhoString(unittest.TestCase):
    """
    Classe de testes para o AnalisadorCaminhoString.

    Contém testes unitários que verificam diferentes cenários de sanitização
    de caminhos usando a classe `AnalisadorCaminhoString`.
    """

    def setUp(self):
        """
        Configura o ambiente de teste.

        Este método inicializa a instância de `AnalisadorCaminhoString` usada em cada teste.
        """
        self.analisador = AnalisadorCaminhoString()

    def test_caminho_windows(self):
        """
        Testa um caminho Windows com espaços nos nomes de diretórios.
        """
        caminho = "C:\\Program Files\\Aplicativos\\software.exe"
        resultado = self.analisador.sanitizar_caminho(caminho)
        esperado = PathData(
            caminho_original=caminho,
            caminho_sanitizado="C:\\ProgramFiles\\Aplicativos\\software.exe",
            formato_valido=True,
            extensao_arquivo=".exe",
            eh_absoluto=True,
            numero_diretorios=3,
            nome_arquivo="software",
            pasta_principal="Aplicativos",
            eh_relativo=False,
        )
        self.assertEqual(resultado, esperado)

    def test_caminho_inexistente(self):
        """
        Testa um caminho inexistente.
        """
        caminho_teste = "/caminho/inexistente/"
        resultado = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado="/caminho/inexistente/",
            formato_valido=True,
            eh_absoluto=False,
            extensao_arquivo=None,
            numero_diretorios=2,
            nome_arquivo=None,
            pasta_principal="caminho",
            eh_relativo=False,
        )
        self.assertEqual(resultado, esperado)

    def test_caminho_absoluto_arquivo(self):
        """
        Testa um caminho absoluto para um arquivo HTML.
        """
        caminho_teste = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
        resultado = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado=caminho_teste,
            formato_valido=True,
            extensao_arquivo=".html",
            eh_absoluto=True,
            numero_diretorios=4,
            nome_arquivo="favoritos_23_12_2024",
            pasta_principal="Chrome",
            eh_relativo=False,
        )
        self.assertEqual(resultado, esperado)

    def test_caminho_relativo_html(self):
        """
        Testa um caminho relativo para um arquivo HTML.
        """
        caminho_teste = "../../Downloads/Chrome/favoritos.html"
        resultado = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado=caminho_teste,
            formato_valido=True,
            extensao_arquivo=".html",
            eh_absoluto=False,
            numero_diretorios=4,
            nome_arquivo="favoritos",
            pasta_principal="Chrome",
            eh_relativo=True,
        )
        self.assertEqual(resultado, esperado)

    def test_caminho_com_espacos(self):
        """
        Testa um caminho com espaços em nomes de diretórios.
        """
        caminho_teste = "/home/pedro-pm-dias/Meu Documento/arquivo.docx"
        resultado = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado="/home/pedro-pm-dias/MeuDocumento/arquivo.docx",
            formato_valido=True,
            extensao_arquivo=".docx",
            eh_absoluto=False,
            numero_diretorios=3,
            nome_arquivo="arquivo",
            pasta_principal="MeuDocumento",
            eh_relativo=False,
        )
        self.assertEqual(resultado, esperado)

    def test_caminho_com_til(self):
        """
        Testa um caminho com '~' para referenciar o diretório do usuário.
        """
        caminho_teste = "~/Downloads/Documentos/arquivo.txt"
        resultado = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado="/Downloads/Documentos/arquivo.txt",
            formato_valido=True,
            extensao_arquivo=".txt",
            eh_absoluto=False,
            numero_diretorios=2,
            nome_arquivo="arquivo",
            pasta_principal="Documentos",
            eh_relativo=False,
        )
        self.assertEqual(resultado, esperado)

    def test_caminho_servidor(self):
        """
        Testa um caminho de rede compartilhada (servidor).
        """
        caminho_teste = "//server/share/arquivos/relatório.xlsx"
        resultado = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado="//server/share/arquivos/relatório.xlsx",
            formato_valido=True,
            extensao_arquivo=".xlsx",
            eh_absoluto=False,
            numero_diretorios=3,
            nome_arquivo="relatrio",
            pasta_principal="arquivos",
            eh_relativo=False,
        )
        self.assertEqual(resultado, esperado)


if __name__ == "__main__":
    unittest.main()
