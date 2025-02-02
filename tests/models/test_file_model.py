# pylint: disable=C

import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from app.models.file_model import InformacoesCaminho


class TestInformacoesCaminho(unittest.TestCase):

    @patch("app.models.file_model.Path.exists", return_value=True)
    @patch("app.models.file_model.GeneralServices")
    @patch("app.models.file_model.HtmlTag")
    def setUp(self, MockHtmlTag, MockGeneralServices):
        self.mock_html_tag = MockHtmlTag.return_value
        self.mock_general_services = MockGeneralServices.return_value
        self.caminho = "/fake/path/to/file.html"
        self.informacoes_caminho = InformacoesCaminho(caminho_string=self.caminho)

    @patch("app.models.file_model.Path.exists", return_value=False)
    def test_init_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            InformacoesCaminho(caminho_string="/non/existent/path")

    def test_nomenclatura(self):
        caminho = Path(self.caminho)
        expected = {
            "nome_puro": caminho.stem,
            "extensoes": caminho.suffixes,
            "pai": str(caminho.parent),
            "raiz": caminho.root,
            "partes": list(caminho.parts),
            "caminho_absoluto": str(caminho.absolute()),
            "caminho_resolvido": str(caminho.resolve()),
        }
        result = self.informacoes_caminho.nomenclatura(caminho)
        self.assertEqual(result, expected)

    def test_validar_caminho(self):
        caminho = Path(self.caminho)
        expected = {
            "eh_absoluto": "Sim" if caminho.is_absolute() else "Não",
            "eh_arquivo": "Sim" if caminho.is_file() else "Não",
            "eh_diretorio": "Sim" if caminho.is_dir() else "Não",
            "existe": "Sim" if caminho.exists() else "Não",
            "eh_link_simbolico": "Sim" if caminho.is_symlink() else "Não",
        }
        result = self.informacoes_caminho.validar_caminho(caminho)
        self.assertEqual(result, expected)

    @patch("app.models.file_model.access", return_value=True)
    def test_verificar_permissoes(self):
        caminho = Path(self.caminho)
        expected = {
            "leitura": "Sim",
            "escrita": "Sim",
            "execucao": "Sim",
        }
        result = self.informacoes_caminho.verificar_permissoes(caminho)
        self.assertEqual(result, expected)

    @patch("app.models.file_model.Path.stat")
    def test_obter_estatisticas(self, mock_stat):
        mock_stat.return_value = MagicMock(
            st_size=1024, st_ctime=1609459200, st_mtime=1609459200, st_atime=1609459200
        )
        self.mock_general_services.converter_tamanho.return_value = "1 KB"
        self.mock_general_services.converter_timestamp.return_value = (
            "2021-01-01 00:00:00"
        )
        caminho = Path(self.caminho)
        expected = {
            "tamanho": "1 KB",
            "data_criacao": "2021-01-01 00:00:00",
            "data_modificacao": "2021-01-01 00:00:00",
            "data_acesso": "2021-01-01 00:00:00",
        }
        result = self.informacoes_caminho.obter_estatisticas(caminho)
        self.assertEqual(result, expected)

    @patch(
        "builtins.open",
        new_callable=unittest.mock.mock_open,
        read_data="fake html content",
    )
    def test_ler_arquivo_html(self):
        result = self.informacoes_caminho.ler_arquivo_html(self.caminho)
        self.assertEqual(result, ["fake html content"])

    @patch(
        "app.models.file_model.InformacoesCaminho.ler_arquivo_html",
        return_value=["<html></html>"],
    )
    def test_process_html_file(self):
        self.mock_html_tag.get_tags_data.return_value = [{"tag": "html"}]
        result = self.informacoes_caminho.process_html_file(self.caminho)
        self.assertEqual(result, [{"tag": "html"}])

    @patch(
        "app.models.file_model.InformacoesCaminho.obter_informacoes",
        return_value={"nome": "file.html"},
    )
    @patch(
        "app.models.file_model.InformacoesCaminho.process_html_file",
        return_value=[{"tag": "html"}],
    )
    def test_gerar_json_completo(self):
        result = self.informacoes_caminho.gerar_json_completo()
        expected = json.dumps(
            {"nome": "file.html", "tags_html": [{"tag": "html"}]},
            indent=4,
            ensure_ascii=False,
        )
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
