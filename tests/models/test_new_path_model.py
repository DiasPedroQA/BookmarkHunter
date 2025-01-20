# pylint: disable=C, R, E, W

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

    def test_caminho_invalido(self):
        caminho_teste = "/caminho/inexistente/"
        objeto_obtido = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        objeto_esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado=caminho_teste,
            formato_valido=True,
            extensao_arquivo=None,
            eh_absoluto=False,
            numero_diretorios=2,
            nome_arquivo=None,
            pasta_principal="caminho",
            eh_relativo=False,
        )
        self.assertEqual(
            objeto_obtido.caminho_original, objeto_esperado.caminho_original
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)

    def test_caminho_absoluto_arquivo_existente(self):
        caminho_teste = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
        objeto_obtido = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        objeto_esperado = PathData(
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
        self.assertEqual(
            objeto_obtido.caminho_original, objeto_esperado.caminho_original
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)

    def test_caminho_absoluto_arquivo_inexistente(self):
        caminho_teste = "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html"
        objeto_obtido = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        objeto_esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado=caminho_teste,
            formato_valido=True,
            extensao_arquivo=".html",
            eh_absoluto=True,
            numero_diretorios=4,
            nome_arquivo="favoritos",
            pasta_principal="Chrome",
            eh_relativo=False,
        )
        self.assertEqual(
            objeto_obtido.caminho_original, objeto_esperado.caminho_original
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)

    def test_caminho_absoluto_pasta_existente(self):
        caminho_teste = "/home/pedro-pm-dias/Downloads/Chrome/"
        objeto_obtido = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        objeto_esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado=caminho_teste,
            formato_valido=True,
            extensao_arquivo=None,
            eh_absoluto=True,
            numero_diretorios=4,
            nome_arquivo=None,
            pasta_principal="Downloads",
            eh_relativo=False,
        )
        self.assertEqual(
            objeto_obtido.caminho_original, objeto_esperado.caminho_original
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)

    def test_caminho_relativo_arquivo_inexistente(self):
        caminho_teste = "../../Downloads/Chrome/favoritos.html"
        objeto_obtido = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        objeto_esperado = PathData(
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
        self.assertEqual(
            objeto_obtido.caminho_original, objeto_esperado.caminho_original
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)

    def test_caminho_relativo_arquivo_existente(self):
        caminho_teste = "../../Downloads/Chrome/favoritos_23_12_2024.html"
        objeto_obtido = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        objeto_esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado=caminho_teste,
            formato_valido=True,
            extensao_arquivo=".html",
            eh_absoluto=False,
            numero_diretorios=4,
            nome_arquivo="favoritos_23_12_2024",
            pasta_principal="Chrome",
            eh_relativo=True,
        )
        self.assertEqual(
            objeto_obtido.caminho_original, objeto_esperado.caminho_original
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)

    def test_caminho_relativo_arquivo_inexistente(self):
        caminho_teste = "~/Downloads/Documentos/arquivo.txt"
        objeto_obtido = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        objeto_esperado = PathData(
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
        self.assertEqual(
            objeto_obtido.caminho_original, objeto_esperado.caminho_original
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)

    def test_caminho_absoluto_arquivo_inexistente(self):
        caminho_teste = "//server/share/arquivos/relatório.xlsx"
        objeto_obtido = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        objeto_esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado="//server/share/arquivos/relatrio.xlsx",
            formato_valido=True,
            extensao_arquivo=".xlsx",
            eh_absoluto=False,
            numero_diretorios=3,
            nome_arquivo="relatrio",
            pasta_principal="arquivos",
            eh_relativo=False,
        )
        self.assertEqual(
            objeto_obtido.caminho_original, objeto_esperado.caminho_original
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)

    def test_caminho_absoluto_arquivo_existente(self):
        caminho_teste = "/home/pedro-pm-dias/Meu Documento/arquivo.docx"
        objeto_obtido = (self.analisador.sanitizar_caminho(caminho=caminho_teste))
        objeto_esperado = PathData(
            caminho_original=caminho_teste,
            caminho_sanitizado=caminho_teste,
            formato_valido=False,
            extensao_arquivo=".docx",
            eh_absoluto=True,
            numero_diretorios=3,
            nome_arquivo="arquivo",
            pasta_principal="Meu Documento",
            eh_relativo=False
        )
        self.assertEqual(
            objeto_obtido.caminho_original, "/home/pedro-pm-dias/MeuDocumento/arquivo.docx"
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)

    def test_caminho_absoluto_windows_inexistente(self):
        caminho_teste = "C:\Program Files\Aplicativos\software.exe"
        objeto_obtido = self.analisador.sanitizar_caminho(caminho=caminho_teste)
        objeto_esperado = PathData(
            caminho_original="C:\Program Files\Aplicativos\software.exe",
            caminho_sanitizado="C:\Program Files\Aplicativos\software.exe",
            formato_valido=False,
            extensao_arquivo=".exe",
            eh_absoluto=True,
            numero_diretorios=3,
            nome_arquivo="software",
            pasta_principal=None,
            eh_relativo=False,
        )
        self.assertEqual(
            objeto_obtido.caminho_original, objeto_esperado.caminho_original
        )
        self.assertEqual(
            objeto_obtido.caminho_sanitizado, objeto_esperado.caminho_sanitizado
        )
        self.assertEqual(objeto_obtido.formato_valido, objeto_esperado.formato_valido)
        self.assertEqual(objeto_obtido.eh_absoluto, objeto_esperado.eh_absoluto)
        self.assertEqual(
            objeto_obtido.extensao_arquivo, objeto_esperado.extensao_arquivo
        )
        self.assertEqual(
            objeto_obtido.numero_diretorios, objeto_esperado.numero_diretorios
        )
        self.assertEqual(objeto_obtido.nome_arquivo, objeto_esperado.nome_arquivo)
        self.assertEqual(objeto_obtido.pasta_principal, objeto_esperado.pasta_principal)
        self.assertEqual(objeto_obtido.eh_relativo, objeto_esperado.eh_relativo)


if __name__ == "__main__":
    unittest.main()
