# app/controllers/path_controller.py
from app.services.path_service import PathService

class PathController:
    def __init__(self):
        self.path_service = PathService()

    def processar_dados(self, dados_entrada):
        """
        Processa os dados recebidos, chamando os serviços necessários.
        """
        try:
            resultado = self.path_service.analisar_caminhos(dados_entrada)
            return {"status": "success", "data": resultado}
        except ValueError as e:
            return {"status": "error", "message": str(e)}
