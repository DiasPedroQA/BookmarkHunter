# pylint: disable=C

import unittest
from app.models.path_model import CaminhoBase


class TestCaminhoBase(unittest.TestCase):

    def setUp(self):
        self.caminhos_validos = [
            "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
            "/home/pedro-pm-dias/Downloads/Chrome/",
            "../../Downloads/Chrome/favoritos_23_12_2024.html",
            "../../Downloads/Chrome/",
        ]
        self.caminhos_invalidos = [
            "",  # Caminho vazio
            " " * 261,  # Caminho muito longo
            "invalid_path_with_<>_chars",  # Caminho com caracteres inválidos
        ]

    def test_sanitizar_caminho(self):
        # sourcery skip: no-loop-in-tests
        for caminho in self.caminhos_validos:
            analisador = CaminhoBase(caminho)
            self.assertTrue(analisador.caminho_sanitizado)

        for caminho in self.caminhos_invalidos:
            with self.assertRaises(ValueError):
                CaminhoBase(caminho)

    def test_validar_caminho(self):
        # sourcery skip: no-loop-in-tests
        for caminho in self.caminhos_validos:
            analisador = CaminhoBase(caminho)
            validacao = analisador.validar_caminho()
            self.assertIn("valido", validacao)
            self.assertIn("tipo", validacao)
            self.assertIn("arquivo_ou_pasta", validacao)

    def test_obter_metadados(self):
        # sourcery skip: no-loop-in-tests
        for caminho in self.caminhos_validos:
            analisador = CaminhoBase(caminho)
            metadados = analisador.obter_metadados()
            self.assertIsInstance(metadados, dict)

    def test_gerar_json(self):
        # sourcery skip: no-loop-in-tests
        for caminho in self.caminhos_validos:
            analisador = CaminhoBase(caminho)
            json_data = analisador.gerar_json()
            self.assertIsInstance(json_data, str)


if __name__ == "__main__":
    unittest.main()
