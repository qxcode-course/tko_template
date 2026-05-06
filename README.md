---
nomeAluno: "Seu nome"
matricula: "Digite sua matrícula aqui por obséquio"
---

# Instalando o TKO e configurando o repositório

## Vou programar no meu setup local

- Se for a primeira configuração
  - Instale git, python, ide(vscode), compiladores
  - Configure sua chave git ssh
  - Configure o pipx
    - `pipx ensurepath`
    - Reinicie o terminal
  - Instale o tko
    - `pipx install tko`

## Vou programar no Codespace

```bash
# instalando o tko e extensões úteis
# Escolha se quer usar python ou typescript
# As outras linguagens c, c++, java, etc, já vem automaticamente na máquina virtual
./setup.sh

```

