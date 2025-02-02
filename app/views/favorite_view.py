# pylint: disable=C0103, C0114, C0115, C0116, C0301, C0413

# app/views/favorite_view.py
from typing import List, Dict


def display_favorites(favorites: List[Dict]):
    """
    Função para exibir os favoritos com suas tags, atributos e conteúdo de forma organizada.

    Args:
        favorites (List[Dict]): Lista de dicionários contendo informações sobre as tags HTML.
    """
    for favorite in favorites:
        # Exibir o nome da tag
        print(f"Tag: {favorite['tag']}")

        # Exibir os atributos
        print("Atributos:")
        for key, value in favorite["attributes"].items():
            print(f"  {key}: {value}")

        # Exibir o conteúdo da tag
        print(f"Conteúdo: {favorite['content']}")

        print("-" * 40)  # Linha separadora para visualização


# # Exemplo de uso com os dados fornecidos
# favorites_data = [
#     {
#         "tag": "h3",
#         "attributes": {
#             "add_date": "1726452161",
#             "last_modified": "1733205396",
#             "personal_toolbar_folder": "true",
#         },
#         "content": "Barra de favoritos",
#     },
#     {
#         "tag": "a",
#         "attributes": {"href": "https://web.whatsapp.com/", "add_date": "1728516875"},
#         "content": "WhatsApp",
#     },
#     {
#         "tag": "a",
#         "attributes": {
#             "href": "https://www.youtube.com/watch?v=mr_mD76aXDE",
#             "add_date": "1733205396",
#         },
#         "content": "Psychedelic Radio 24/7",
#     },
# ]

# # Chamando a função para exibir os favoritos
# display_favorites(favorites_data)
