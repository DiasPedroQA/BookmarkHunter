---
name: Template de issue personalizado
about: Descreva o propósito deste template de issue aqui.
title: Corrigir bug no sistema de autenticação
labels: "bug, alta prioridade"
assignees: "diaspedro"
---

**Descrição do problema**
Ao tentar fazer login no sistema, alguns usuários estão recebendo a mensagem de erro "Credenciais inválidas", mesmo quando as credenciais estão corretas. Esse problema ocorre principalmente em navegadores específicos, como o Safari.

## Passos para reproduzir

1. Acessar a página de login.
2. Inserir um nome de usuário e senha válidos.
3. Clicar em "Entrar".
4. Observar a mensagem de erro "Credenciais inválidas".

**Comportamento esperado**
O sistema deve permitir o login do usuário e redirecioná-lo para a página inicial após a autenticação bem-sucedida.

**Comportamento atual**
O sistema exibe a mensagem de erro "Credenciais inválidas" e não permite o acesso, mesmo com credenciais corretas.

## Contexto adicional

- O problema parece estar relacionado ao tratamento de cookies no Safari.
- Já foram verificados os logs do servidor, mas não há registros de erros durante o processo de autenticação.
- Um exemplo de usuário afetado é "usuario_teste" com a senha "senha123".

**Capturas de tela**
![Erro de autenticação](https://exemplo.com/caminho/para/imagem.png)

## Informações adicionais

- Sistema operacional: macOS Big Sur
- Navegador: Safari 15.1
- Versão do sistema: 2.3.4
