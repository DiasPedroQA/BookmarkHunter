# pylint: disable=C0114, C0115

from bs4 import BeautifulSoup


class AnalisadorHTML:
    def __init__(self, html_conteudo: str):
        """Inicializa o analisador com o conteúdo HTML."""
        self.soup = BeautifulSoup(html_conteudo, "html.parser")

    def extrair_tags(self):
        """Extrai as tags <H3> e <A> e seus atributos relevantes."""
        tags_extraidas = []

        # Extrai tags <H3>
        tags_extraidas.extend(
            {
                "tag": "H3",
                "ADD_DATE": h3.get("add_date", "").strip(),
                "LAST_MODIFIED": h3.get("last_modified", "").strip(),
                "PERSONAL_TOOLBAR_FOLDER": h3.get(
                    "personal_toolbar_folder", ""
                ).strip(),
            }
            for h3 in self.soup.find_all("h3")
        )
        # Extrai tags <A>
        tags_extraidas.extend(
            {
                "tag": "A",
                "HREF": a.get("href", "").strip(),
                "ADD_DATE": a.get("add_date", "").strip(),
                "ICON": a.get("icon", "").strip(),
            }
            for a in self.soup.find_all("a")
        )
        return tags_extraidas
