# app/models/bookmark_model.py
# pylint: disable = C

import json
from typing import Dict
from bs4 import BeautifulSoup, ResultSet, Tag


# Entrada HTML
pages = """
<H3 ADD_DATE="1726278565" LAST_MODIFIED="1726278565">Barra de favoritos</H3>
<A HREF="https://gemini.google.com/app" ADD_DATE="1708744361">Gemini</A>
<SPAN CLASS="invalid">Texto inválido</SPAN>
<DT><H3 ADD_DATE="1684718385" LAST_MODIFIED="1686149971">MEI</H3>
<DL><p>
<DT><A HREF="https://www.gov.br/nfse/pt-br" ADD_DATE="1682469973" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACvUlEQVQ4jY2TS0hUcRTGv/O/9+odZ5xsSkvCoCgTm0xToidYURTVIsgKCtpE0KIgaBGSdBcJBUFYi4giKFrIbIo2FSFKYEExjaPpaKT00J4+Rptm7vN/WuSYUJG/7TnnO+fA9wEAmEEAMBELrxt5WbUXk0QiUDATIhEoMAyRjFXXWYlKz+yuaPrcXlGUFc8u+CetrbUqAHDX/J1mYjU7r9cw95X3cc+8A9keZoi/zRLABBAHdz9es3apZ4T81jYpVTdc8knbvqwNNcUv7iQz1DC7qvctALABQQbkNAHgRFPicOGcwNVZ+Xm+sXFL9g+lROKD5ylko357RNlVem8wlck5G6yM3cxeQzQpwk5q2+dR+8fHEZvHvts2s5TMzC9fj/KRiwlZc6zTed5yiLm/nMfjq+6PdJQvn3rLgCDj1kDk6wTVvR1KugRSQkGVNq4o4INbi6EKj05e/QLdeigv7GpioeUqpuWNErjRtzx+iQhMG46/eCUUrVwVUjJDeJJh2i4tLvbh/NElXBDQYVxvodPr6znosz0Joeq5hIwpnwHeaZGnK8jTVVYEoCoEXRMI5Wt4/8VE/Y03UBTg0NZCdjwJIoAZLAggQgFJ4RNScjtDCP4FJDO5Hjjo13hgKEXNreNUvdSloG55OTmqqghkMhaf8xcMVwcq44+EJ73LnmMmFTVXBdgVgpnII4JDqqpzW8ewm/nUjHy/VNMW2hxXbvKHYw1UMphhA4IAYPPJ6B5Vy73BpIXSpisFmBypyUBOGqe23Fa2LHrwzXL9jf5w9AoR5HQvTBmp9kR7uGRO6kwoMLHPsoVbWjSo7Sh7grK5XXe/W/n1wYpo7x8e+J2FOgUAOB7YbPZUMvdXM/eWveO+hYf/Z+VpRaZv0VW7091V8kfnymt9T9cuAADGDMKUbUh2hWuSHSv3z2jrJD8BdVVhEN4nTVYAAAAASUVORK5CYII=">empresa MEI CNPJ NFS-e</A>
</DL><p>
<DT><A HREF="https://www8.receita.fazenda.gov.br/SimplesNacional/aplicacoes.aspx?id=48" ADD_DATE="1682476883">Simples Nacional</A>
<DL><p>
<DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
<DT><A HREF="https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh" ADD_DATE="1686055702" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACMklEQVQ4jZWSv09TURTHz7nvB7wX2w6gTDJISCQ0Qd9rhzJodWokkaSmdQD/AcrUvwQDCyaYyE6NRE20HZoUaEs7tYTaQmlSgoPVqukPWt579zg8Ak108U73fs/nDuecDzqcLvifwwYfRPRPaDC//sAYQ0REHORs9CokIpFzzjk3TdMwDFVVLcsiIkTgnGRZBgDTNEXxEpMkiT0Ph+OfP2Uz6ZcrK6Io6h7944f3mXR6b29X07RX6+uRSKTTaY+Njb2Nbc3NPWF3p6Y8Hs9xtbq8HIlGo/4HD/1+/9Hxcb1ebzS+jY/ffrG4QJxr2v1AIND80WQIcFgqhUOhrVhM1zVJlguFQjgUehYMfimV3m1vT05Ojt685fP5arVadn+fAYAsy4wxy7Qs0+p2u9PT07lc3v/oMQDkc3lFUbxe76xvtlAs/v7183JKnHMiIiCG2O/3T0/r5+ddUZKKBwfVk5PI0tLExJ14PA4AIhEZhgEAqqoKojCsKJXKUTAYBACH09VsNjPpzOLiQqfTyaSzTJAYMrw3M5NKpebnnyaTyV6vp+taKpXa2dl1u93ErXgiDgDlcqVcKSvKsDAyMoqIRPR6Y2N1da3VarlcLkDs9XqJRKLxvXF29lUQhDebm6XDwyFZxqFh5eLCIG4B0A2H0zCMfr9vb1VRVXtlnXZblCRFUYgIHU4XQwREu3XbDiJCRHsSiMgYIyK7KgIAJwKiK3lsc66Es9FrlwatHDTv78S+/wF72SshkV+RyAAAAABJRU5ErkJggg==">[pt-BR] Fundamentos do Git, um guia completo - DEV Community</A>
<DT><A HREF="https://martinfowler.com/articles/practical-test-pyramid.html" ADD_DATE="1691737793" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAB3ElEQVQ4jW2SPWhUQRSFz52ZN+8t+1yNa2wkICgpDPgT0eAWJtokrForsRcXESUgaGIhSMDKIuBiL6iViIVYiX+IqI0GhCARRNhNkRh92V2z772ZazFG9m+qYeZ+99xzuORvKgIAQEToOsxsmF8emxjuyxum+dXvyn1Yy8YYhzCz44UgKURHC+UqMhmdzQbGWABae8ycxGmSpPXGeoeuUkrWV6PJM8fLcxfXan88T1UqKwAP7dlZvvvkQul2sDlsBYQxJsiF9x8+n731YHv/lk+fvxVGLxVGLz999n7/vl2AQbs3wQwpRVyLqtUVAIuLlWj5V7RcuXHz3tt3X0CetdwGbFyk9j0AcZwAjbk700tLP69MlTO5rLW2J8Au1oPDg1dnzpfOncrnc9Ae0Na+FYCbNAyDsaN7lZJxnIA7q1sBcvG/ej0/MV569PiNZQZ1C0ABLoa0Vl8HIKQAxOmzs0JQ4GvbJSKIKElMuHXbyeIIgMHdOw4VDmutiKjHQIAQgpprjRPFkcKRoQ8fFwYG+q9fm2w2EyL02C2A3PIxc5oaon9OPE/9rzDML8bGD/Tl7cbyCWdDa+miYrDzSgRmENiXOiM9A+FLT7GNXKfuid0LMy/8/iE5Mkxfo+pfL0nGtVO5/GUAAAAASUVORK5CYII=">A Pirâmide do Teste Prático</A>
</DL><p>
"""

# Função para extrair texto de uma tag HTML
def extrair_tags(html: str) -> ResultSet[Tag]:
    soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
    tags: ResultSet[Tag] = soup.find_all(True)  # Encontra todas as tags
    return tags

# Filtra as tags extraídas para obter os dados
def filtrar_tags(page: str) -> str:
    tags_extraidas: ResultSet[Tag] = extrair_tags(page)
    dados_encontrados: Dict[str, Dict[str, str]] = {}

    for tag in tags_extraidas:
        # Atributos comuns a todas as tags
        tag_comum = {
            "texto": tag.text.strip(),
            "add_date": tag.attrs.get("add_date", "Não encontrado"),
            "tag_name": tag.name
        }

        if tag.name == "h3":
            # Se for tag h3, adicionar atributos extras
            tag_ok = {
                **tag_comum,
                "last_modified": tag.attrs.get("last_modified", "Não encontrado")
            }
            dados_encontrados[tag.text.strip()] = tag_ok
        
        elif tag.name == "a":
            # Se for tag a, adicionar atributos extras
            tag_ok = {
                **tag_comum,
                "href": tag.attrs.get("href", "Não encontrado")
            }
            dados_encontrados[tag.text.strip()] = tag_ok
        
        else:
            # Para tags inválidas, apenas atributos comuns
            dados_encontrados[tag.text.strip()] = tag_comum

    return json.dumps(dados_encontrados, indent=4, ensure_ascii=False)

# Exemplo de chamada
resultado_json = filtrar_tags(pages)
print("\n\nResultado final em JSON:")
print(resultado_json)
