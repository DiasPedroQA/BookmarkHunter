# pylint: disable=C, R, E, W

# Suíte de testes

import unittest
from app.models.new_path_model import PathAnalyzer


class TestPathAnalyzer(unittest.TestCase):
    """
    Testes unitários para a classe PathAnalyzer.
    """

    def test_is_absolute(self):
        """
        Testa se o método is_absolute() identifica corretamente caminhos absolutos.
        """
        self.assertTrue(
            PathAnalyzer(
                "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
            ).is_absolute()
        )
        self.assertFalse(
            PathAnalyzer(
                "pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
            ).is_absolute()
        )
        self.assertTrue(PathAnalyzer("//servidor/compartilhamento").is_absolute())
        self.assertFalse(PathAnalyzer("").is_absolute())

    def test_is_valid_path(self):
        """
        Testa se o método is_valid_path() valida corretamente os caminhos.
        """
        self.assertTrue(
            PathAnalyzer(
                "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
            ).is_valid_path()
        )
        self.assertTrue(
            PathAnalyzer(
                "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
            ).is_valid_path()
        )
        self.assertTrue(
            PathAnalyzer("/caminho/valido/sem/chars_especiais").is_valid_path()
        )
        self.assertFalse(PathAnalyzer("invalid<>chars").is_valid_path())

    def test_get_basename(self):
        """
        Testa se o método get_basename() retorna o nome do arquivo ou pasta corretamente.
        """
        self.assertEqual(
            PathAnalyzer(
                "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
            ).get_basename(),
            "favoritos_23_12_2024.html",
        )
        self.assertEqual(
            PathAnalyzer("/home/pedro-pm-dias/Downloads/").get_basename(), "Downloads"
        )
        self.assertEqual(
            PathAnalyzer("caminho_relativo.html").get_basename(),
            "caminho_relativo.html",
        )
        self.assertEqual(PathAnalyzer("/").get_basename(), "")

    def test_get_directory(self):
        """
        Testa se o método get_directory() retorna o diretório pai corretamente.
        """
        self.assertEqual(
            PathAnalyzer(
                "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
            ).get_directory(),
            "/home/pedro-pm-dias/Downloads/Chrome",
        )
        self.assertEqual(
            PathAnalyzer("/caminho/sem_arquivo/").get_directory(), "/caminho"
        )
        self.assertEqual(
            PathAnalyzer("Chrome/favoritos_23_12_2024.html").get_directory(), "Chrome"
        )
        self.assertEqual(PathAnalyzer("/").get_directory(), "")

    def test_has_extension(self):
        """
        Testa se o método has_extension() identifica corretamente extensões de arquivos.
        """
        self.assertTrue(
            PathAnalyzer(
                "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
            ).has_extension(".html")
        )
        self.assertFalse(
            PathAnalyzer("/home/pedro-pm-dias/Downloads/exemplo.pdf").has_extension(
                ".html"
            )
        )
        self.assertTrue(
            PathAnalyzer("favoritos_23_12_2024.HTML").has_extension(".HTML")
        )
        self.assertFalse(PathAnalyzer("favoritos_23_12_2024").has_extension(".html"))

    def test_count_segments(self):
        """
        Testa se o método count_segments() conta corretamente os segmentos do caminho.
        """
        self.assertEqual(
            PathAnalyzer(
                "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
            ).count_segments(),
            5,
        )
        self.assertEqual(PathAnalyzer("/").count_segments(), 0)
        self.assertEqual(
            PathAnalyzer(
                "../Downloads/Chrome/favoritos_23_12_2024.html"
            ).count_segments(),
            4,
        )
        self.assertEqual(PathAnalyzer("/redundante//slashes///").count_segments(), 2)


if __name__ == "__main__":
    unittest.main()
