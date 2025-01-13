# """
# main.py

# Este módulo inicializa e executa a aplicação Flask.

# Funções:
#     create_app: Cria e configura a aplicação Flask.

# Variáveis:
#     app: Instância da aplicação Flask.
#     debug: Indica se a aplicação deve ser executada em modo de depuração.

# Uso:
#     Este script deve ser executado diretamente para iniciar a aplicação Flask.
# """

# import os
# import logging
# from app import create_app

# logging.basicConfig(level=logging.INFO)

# app = create_app()

# if __name__ == "__main__":
#     logging.info("Iniciando a aplicação Flask...")
#     debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
#     app.run(debug=debug, host="0.0.0.0", port=5000)
