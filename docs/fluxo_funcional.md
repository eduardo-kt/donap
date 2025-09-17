# Fluxo Funcional do DonApp

Este documento descreve o fluxo funcional do sistema DonApp, desde o login do usuário até a execução das principais funcionalidades.

---

## 1. Tela Inicial / Login
1. O usuário inicia o aplicativo.
2. O sistema solicita usuário e senha.
3. O sistema verifica as credenciais:
   - Se válidas: usuário é redirecionado para o menu principal.
   - Se inválidas: mensagem de erro e possibilidade de tentar novamente.
   - Caso o usuário deseje, é possível registrar um novo usuário através do botão "Registrar".

---

## 2. Menu Principal
Após login bem-sucedido, o usuário visualiza as opções do menu:

1. **Cadastrar**
   - Registrar novas pessoas (donatários) ✔️ implementado.
   - Registrar novas doações ❌ pendente.
   - Os dados são salvos na pasta `data/` (arquivos JSON ou CSV).

2. **Pesquisar**
   - Buscar informações sobre pessoas cadastradas ou doações ❌ pendente.
   - O sistema lê os dados persistidos em `data/`.

3. **Doar**
   - Associar uma doação a um beneficiário específico ❌ pendente.
   - Atualiza os arquivos de persistência na pasta `data/`.

4. **Logout / Sair**
   - Finaliza a sessão do usuário.
   - Retorna à tela de login.

---

## 3. Persistência de Dados
- Todos os registros (pessoas e doações) são salvos em arquivos dentro da pasta `data/`.
- As operações de cadastro, doação e pesquisa acessam esses arquivos para garantir **persistência entre sessões**.
- Testes unitários foram implementados para verificar a correta leitura e escrita dos dados de donatários e usuários.

---

## 4. Observações
- O fluxo é sequencial: login → menu → ação → persistência.
- Funcionalidades atuais implementadas: login, cadastro de donatário e persistência.
- Funcionalidades futuras: cadastro de doações, pesquisa de donatários, associar doações a beneficiários, relatórios e autenticação mais robusta.
- O sistema foi projetado para ser expandido facilmente, mantendo a persistência em JSON e a interface em Tkinter.
