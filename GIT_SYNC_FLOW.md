# 📚 Fluxo do Script `git-sync.sh`

> **Objetivo**: Sincronizar seu repositório local com o repositório remoto, automatizando os passos mais comuns e resolvendo conflitos de forma segura.

---

## 🎯 O Que o Script Faz

O `git-sync.sh` realiza 5 operações principais em sequência:

```
┌─────────────────────────────────────────────┐
│  1. Validação do Ambiente                   │
│  2. Configuração de Identidade (user/email) │
│  3. Tratamento de Merge Pendente            │
│  4. Sincronização com Remoto (fetch/merge)  │
│  5. Commit Local + Push                     │
└─────────────────────────────────────────────┘
```

---

## 📖 Detalhamento de Cada Etapa

### 1️⃣ Validação do Ambiente

```bash
validate_environment()
get_current_branch()
```

**O que faz:**
- ✅ Verifica se você está dentro de um repositório git
- ✅ Obtém o nome do branch atual (ex: `main`, `develop`)
- ❌ Aborta se não estiver em um repositório ou se estiver em `HEAD` destacado

**Problema comum que resolve:**
```
❌ "fatal: not a git repository"
❌ "fatal: HEAD detached"
```

**Dica para iniciante:** Se você vê esses erros, significa que:
- Você executou o script em uma pasta que não é um repositório git
- Ou você está em um estado especial do git (HEAD destacado) onde não pode committar

---

### 2️⃣ Configuração de Identidade

```bash
setup_git_identity()
```

**O que faz:**
- ✅ Verifica se `user.name` e `user.email` estão configurados
- ✅ Se não estiverem, pergunta interativamente e salva localmente no repositório
- ❌ Aborta se você tentar deixar vazios

**Exemplo de interação:**
```
Seu nome (git user.name): João Silva
user.name configurado localmente.
Seu email (git user.email): joao@example.com
user.email configurado localmente.
```

**Problema comum que resolve:**
```
❌ "Author identity unknown"
❌ Commits aparecendo com nome "Unknown"
```

**Dica para iniciante:** Git precisa saber quem você é para poder assinar os commits. Essa configuração é feita por repositório, não é global.

---

### 3️⃣ Tratamento de Merge Pendente

```bash
handle_pending_merge()
```

**Situação:** Você executou o script antes, teve um conflito, e o deixou pendente.

**O que faz:**
- ✅ Detecta se há um merge em progresso (`MERGE_HEAD`)
- ✅ Se não há conflitos, finaliza automaticamente
- ✅ Se há conflitos, oferece 3 opções para resolver

```
Merge em andamento detectado

Há conflitos? 
  ├─ NÃO → Finaliza com: git add -A && git commit --no-edit
  └─ SIM → Menu de opções:
            1) Manter LOCAL (ours)
            2) Manter REMOTO (theirs)
            3) Resolver manualmente
```

**Problema comum que resolve:**
```
❌ "error: your local changes to 'arquivo.txt' would be overwritten by merge"
❌ "fatal: cannot continue because you have unmerged files"
```

**Dica para iniciante:** Um merge incompleto bloqueia você. Este script detecta e ajuda a resolver antes de continuar.

---

### 4️⃣ Sincronização com Remoto

```bash
sync_with_remote()
```

**O que faz em sequência:**

#### a) **Fetch** (Baixar informações do remoto)
```bash
git fetch origin
```
- ✅ Busca atualizações do repositório remoto sem modificar seus arquivos
- ✅ Atualiza referências de branches remotos
- 🔒 **Seguro**: Não altera nada localmente

#### b) **Merge** (Integrar mudanças remotas)
```bash
git merge origin/$branch
```
- ✅ Traz as mudanças baixadas para seu branch local
- ⚠️ Pode gerar conflitos se você e outra pessoa editaram o mesmo arquivo

**Conflito? O script oferece 3 opções:**

| Opção | Resultado | Quando usar |
|-------|-----------|-----------|
| 1️⃣ LOCAL (ours) | Mantém seu código, descarta remoto | Você tem certeza que está certo |
| 2️⃣ REMOTO (theirs) | Mantém remoto, descarta seu | Você quer aceitar as mudanças |
| 3️⃣ MANUAL | Lista arquivos em conflito e pausa | Você quer revisar e decidir arquivo por arquivo |

**Problema comum que resolve:**
```
❌ "CONFLICT (content): Merge conflict in arquivo.txt"
❌ "Unmerged paths: arquivo.txt"
```

**Dica para iniciante:**
- **Conflito** = Git não consegue decidir qual versão manter automaticamente
- O script permite resolver de forma segura sem usar `git` manualmente
- Opção 3 é a mais educativa: você aprende escolhendo manualmente

---

### 5️⃣ Commit Local + Push

```bash
commit_local_changes()
push_changes()
```

#### a) **Commit** (Registrar suas mudanças)
```bash
git add -A            # Marca todos os arquivos para commitar
git commit -m "..."   # Cria um snapshot com mensagem
```
- ✅ Pede uma mensagem de commit (padrão: "sync update")
- ✅ Se não houver mudanças, apenas notifica e continua

#### b) **Push** (Enviar para o remoto)
```bash
git push              # Se branch já tem tracking
git push -u origin $branch  # Se é a primeira vez
```
- ✅ Envia seus commits para o repositório remoto
- ✅ Detecta se é a primeira vez neste branch e configura tracking

**Problema comum que resolve:**
```
❌ "fatal: The current branch main has no upstream branch"
❌ Commits locais que ninguém vê
```

**Dica para iniciante:** Push é essencial para colaboração. Se você não fizer push, outras pessoas não veem suas mudanças.

---

## 🔄 Fluxo Completo com Exemplos

### Cenário 1: Sem Conflitos ✅

```
$ ./git-sync.sh

user.name configurado localmente.
user.email configurado localmente.

==> Fetching origin/main
==> Merging origin/main
Nada para commitar.
Sync concluído.
```

**O que aconteceu:**
1. Configurou identidade
2. Fez fetch e merge (sem conflitos)
3. Não havia mudanças locais, apenas sincronizou

---

### Cenário 2: Com Conflito (Opção 1 - LOCAL) ⚠️

```
$ ./git-sync.sh

==> Fetching origin/main
==> Merging origin/main
Conflitos detectados.

Escolha como resolver:
  1) Manter LOCAL (ours)
  2) Manter REMOTO (theirs)
  3) Resolver manualmente
> 1

merge: keep local version

Mensagem de commit: sincronizando com remoto
Sync concluído.
```

**O que aconteceu:**
1. Fez fetch
2. Tentou merge, mas teve conflito
3. Você escolheu manter sua versão local
4. Script commitou automaticamente com mensagem descritiva
5. Push enviou para o remoto

---

### Cenário 3: Merge Pendente (Retomando) 🔙

```
$ ./git-sync.sh

==> Merge em andamento detectado
==> Finalizando merge pendente

Mensagem de commit: merge finalizado
Sync concluído.
```

**O que aconteceu:**
1. Script detectou que havia um merge incompleto mas sem conflitos
2. Finalizou o merge automaticamente
3. Continuou normalmente com commit e push

---

## 🎓 Conceitos para Iniciantes

### Branch
- É uma "linha de desenvolvimento" do seu projeto
- Padrão: `main` ou `master`
- Você trabalha em um branch por vez

### Fetch vs Pull
| Comando | O que faz | Equivalente |
|---------|----------|-----------|
| `fetch` | Baixa mudanças, não modifica local | Limpar a caixa de correio |
| `pull` | Fetch + merge em um comando | Limpar e processar |
| `git-sync.sh` | Fetch + merge + commit + push | Sincronização completa |

### Conflito
- Acontece quando você e outra pessoa modificam a mesma linha de código
- Git não sabe qual versão guardar
- Você decide: sua versão, remota ou uma mistura

### Upstream (Tracking)
- É a "conexão" entre seu branch local e o remoto
- Primeira vez: `git push -u origin main`
- Próximas: `git push` (sem repetir `-u`)

---

## ✅ Checklist: Quando usar `git-sync.sh`

- ✅ Antes de começar a trabalhar (pega atualizações)
- ✅ No final do dia (envia suas mudanças)
- ✅ Quando colaboradores atualizaram o código
- ✅ Para resolver conflitos de forma segura
- ✅ Quando está com "HEAD detached" (não recomendado, mas o script avisa)

---

## ⚠️ Limitações e Recursos Avançados

**Este script é ideal para:**
- ✅ Sincronizar um único branch
- ✅ Workflow simples (sem cherry-pick, rebase, etc)
- ✅ Aprender git com segurança

**Para coisas avançadas, use git diretamente:**
- ❌ Rebase interativo: `git rebase -i`
- ❌ Cherry-pick: `git cherry-pick`
- ❌ Stash: `git stash`
- ❌ Bisect: `git bisect`

---

## 🚀 Próximos Passos

1. **Entenda cada passo:** Execute com `bash -x git-sync.sh` (modo debug)
2. **Pratique conflitos:** Crie um conflito propositalmente, resolva com opção 3
3. **Explore git:** Depois, aprenda comandos git avançados
4. **Customize:** Adapte o script para seu workflow

---

## 📝 Sumário do Fluxo

```
entrada
   ↓
✓ Está em repositório git?
   ↓
✓ Tem identidade configurada?
   ↓
✓ Há merge pendente? 
   ├─ SIM → resolver/finalizar
   └─ NÃO → continuar
   ↓
✓ Fetch origin/$branch
   ↓
✓ Merge origin/$branch
   ├─ CONFLITO → resolver (3 opções)
   └─ OK → continuar
   ↓
✓ Há mudanças locais?
   ├─ SIM → commit
   └─ NÃO → notificar
   ↓
✓ Push para remoto
   ↓
✓ "Sync concluído"
```

---

**Feito para aprender!** 🎉 Este script encapsula as melhores práticas de sincronização git para iniciantes.
