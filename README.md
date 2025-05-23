---
nomeAluno: "Seu nome"
matricula: "Digite sua matrícula aqui por obséquio"
---

# Configurações iniciais no codespace

```bash
# instalando o tko
pipx install tko

cd scripts
# instale algum compilador que vocês precise
./install_go.sh # se voce for usar o go
./install_ts.sh # se você for usar typescript
```

- Agora instale alguns plugins úteis
  - Abra a aba de extensões ou Control - Shift - X
  - Procure por Error Lens e clique em instalar

- Abra as configurações do editor com control vírgula
  - Na opção de Auto Save escolha After Delay

- Mate o terminal com control D e reabra
- Quando abrir o primeiro código na linguagem sugerida, o codespace vai perguntar se você quer instalar o plugin, aceite.

## TKO

```bash
## Criando seu novo repositório
tko init --remote [fup|ed|poo]

## Interagindo com seu repositório
tko open <pasta>

## Rodando um código diretamente
tko test <arquivo_codigo>  # usando interface default
tko run  <arquivo_codigo>  # usando interface curses

## Atualizando o tko
pipx upgrade tko
```

## Configuração Inicial

- Após o primeiro setup
  - Aperte F1 e escolha: <Stop Current Workspace> para forçar um reboot completo
- Após reiniciar o codespace
- Crie sua pasta de atividades com o comando `tko init --remote [fup|ed|poo]`
- Abra seu repositório com `tko open <pasta>`
- Escolha a linguagem pretendida
- Baixe alguma atividade navegando e usando o <Enter>
- Entre na atividade com <Enter>
- Use o atalho <e> para abrir os arquivos da atividade selecionada
- O vscode vai sugerir instalar os plugins da linguagem. Aceite.

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
