---
nomeAluno: "Seu nome"
matricula: "Digite sua matrícula aqui por obséquio"
---

# Configurações iniciais no codespace

```bash
# instalando o tko
pipx install tko

# Instalando algumas extensões úteis para todas as linguagens
code --install-extension usernamehw.errorlens
```

Para golang, java, cpp, c, basta você abrir um arquivo de linguagem e aceitar a instalação da extensão para vscode.

Para typescript:

```
cd scripts
./install_ts.sh # se você for usar typescript
```

Para python:

```bash
# Abra o arquivo de configurações do vscode para o projeto e adicione o seguinte parâmetro
code .vscode/settings.json
{
    "python.analysis.typeCheckingMode": "strict"
}
```

## TKO

```bash
## Se você precisar criar um repositório do zero, pode fazer com o seguinte comando

# para criando um repositório de atividades já definindo a fonte
tko init -f myrep -l py --remote poo --enable acesso simples

## Interagindo com seu repositório
tko open myrep

## Rodando um código diretamente
tko run <arquivo_codigo>  # usando interface default
tko gui  <arquivo_codigo>  # usando interface curses

## Atualizando o tko
pipx upgrade tko
```

## Comandos do bash

- `cd <pasta>` para mudar de pasta
- `cd ..` para subir um nível
- `code <arquivo>` para abrir um arquivo pelo terminal
- `control c` para matar um programa do terminal
- `control d` para matar o terminal

## Comandos do Git

- `git add <arquivo>`: Adiciona um arquivo ao stage
- `git add .`: Adiciona todos os arquivos ao stage
- `git commit -m "mensagem"`: Cria um commit com os arquivos no stage
- `git push`: Envia os commits para o repositório remoto
- `git pull`: Atualiza o repositório local com as mudanças do repositório remoto
- `git status`: Mostra o estado atual do repositório
- `git log`: Mostra o histórico de commits
- `git clone <url>`: Clona um repositório remoto para uma pasta local

## Git pela interface do vscode

- Escolha a aba do `Source Control` ou `Control Shift G`
- Clique no + para `stage all changes`, ou seja, marcar tudo pra ser salvo.
- Escreva a mensagem no campo do commit e clique em `Commit` para salvar a versão na máquina virtual.
- Clique em `Sync Changes` para enviar pro site.

## Resolvendo Conflitos

- Antes de trabalhar num respositório, lembre de fazer o pull.
- Se quando for fazer o push, der erro, tente as seguintes opções.
  - git pull --ff-only
  - git rebase
  - git pull --no-rebase
- Se não der certo, cole o erro no chatgpt e siga as instruções.
- Se não der certo, mande o erro no grupo do telegram.

## Lembre-se

- Sua consciência é a melhor ferramenta contra o plágio.
