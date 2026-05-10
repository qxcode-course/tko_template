#!/usr/bin/env bash
set -euo pipefail

# =========================================================
# CONFIG
# =========================================================
readonly DEFAULT_COMMIT_MESSAGE="sync update"

# =========================================================
# COLORS
# =========================================================
readonly RED='\033[31m'
readonly GREEN='\033[32m'
readonly YELLOW='\033[33m'
readonly BLUE='\033[34m'
readonly BOLD='\033[1m'
readonly RESET='\033[0m'

# =========================================================
# UI
# =========================================================
step() {
  printf "\n%b\n" "${BLUE}${BOLD}==>${RESET} ${BOLD}$1${RESET}"
}

success() {
  printf "%b\n" "${GREEN}[OK]${RESET} $1"
}

warn() {
  printf "%b\n" "${YELLOW}[AVISO]${RESET} $1"
}

error() {
  printf "%b\n" "${RED}[ERRO]${RESET} $1"
}

run() {
  printf "%b\n" "${GREEN}-> $*${RESET}"
  "$@"
}

ask() {
  local prompt="$1"
  local answer

  read -r -p "$prompt" answer
  echo "$answer"
}

confirm() {
  local prompt="$1"
  local answer

  read -r -p "$prompt [s/N]: " answer

  case "${answer,,}" in
    s|sim|y|yes)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

# =========================================================
# GIT HELPERS
# =========================================================
is_merge_in_progress() {
  git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1
}

has_merge_conflicts() {
  git diff --name-only --diff-filter=U | grep -q .
}

has_local_changes() {
  ! git diff --quiet || ! git diff --cached --quiet
}

has_remote() {
  git remote get-url origin >/dev/null 2>&1
}

has_upstream() {
  git rev-parse --abbrev-ref --symbolic-full-name "@{u}" \
    >/dev/null 2>&1
}

# =========================================================
# VALIDATION
# =========================================================
validate_environment() {
  step "Validando ambiente"

  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    error "Esse diretório não é um repositório git."
    exit 1
  fi

  success "Repositório git detectado"
}

validate_remote() {
  step "Verificando conexão com o servidor"

  if ! has_remote; then
    error "Remote 'origin' não configurado."
    exit 1
  fi

  if ! git ls-remote origin >/dev/null 2>&1; then
    error "Não foi possível conectar ao servidor remoto."
    warn "Verifique sua internet ou permissões."
    exit 1
  fi

  success "Conexão com servidor OK"
}

get_current_branch() {
  local branch

  branch="$(git rev-parse --abbrev-ref HEAD)"

  if [[ "$branch" == "HEAD" ]]; then
    error "Você está em HEAD destacado."
    warn "Volte para uma branch antes de continuar."
    exit 1
  fi

  echo "$branch"
}

# =========================================================
# GIT IDENTITY
# =========================================================
setup_git_identity() {
  step "Verificando identidade do git"

  local git_user_name
  local git_user_email

  git_user_name="$(git config --get user.name || true)"
  git_user_email="$(git config --get user.email || true)"

  if [[ -z "$git_user_name" ]]; then
    local name

    warn "Seu nome não está configurado no git."
    name="$(ask "Digite seu nome: ")"

    if [[ -z "$name" ]]; then
      error "Nome não pode ser vazio."
      exit 1
    fi

    run git config user.name "$name"
  fi

  if [[ -z "$git_user_email" ]]; then
    local email

    warn "Seu email não está configurado no git."
    email="$(ask "Digite seu email: ")"

    if [[ -z "$email" ]]; then
      error "Email não pode ser vazio."
      exit 1
    fi

    run git config user.email "$email"
  fi

  success "Identidade git configurada"
}

# =========================================================
# STATUS
# =========================================================
show_status() {
  step "Resumo do repositório"

  echo
  run git status --short || true
}

# =========================================================
# COMMIT
# =========================================================
commit_local_changes() {
  step "Verificando alterações locais"

  if ! has_local_changes; then
    success "Nenhuma alteração local encontrada"
    return
  fi

  echo
  warn "Arquivos alterados encontrados:"
  echo

  git status --short

  echo

  if ! confirm "Deseja salvar essas alterações agora?"; then
    warn "Operação cancelada pelo usuário."
    exit 0
  fi

  run git add -A

  local changed_files
  changed_files="$(git diff --cached --name-only | wc -l | tr -d ' ')"

  echo
  echo "Quantidade de arquivos alterados: $changed_files"

  local msg
  msg="$(ask "Mensagem do commit: ")"

  msg="${msg:-$DEFAULT_COMMIT_MESSAGE}"

  run git commit -m "$msg"

  success "Alterações salvas"
}

# =========================================================
# MERGE CONFLICTS
# =========================================================
resolve_merge_conflict() {
  step "Conflitos detectados"

  echo
  warn "Os mesmos arquivos foram alterados localmente e no servidor."
  echo

  git diff --name-only --diff-filter=U

  echo

  while true; do
    echo "Escolha uma opção:"
    echo
    echo "  1) Manter MINHA versão"
    echo "  2) Manter versão do SERVIDOR"
    echo "  3) Resolver manualmente"
    echo

    local choice
    choice="$(ask "> ")"

    case "$choice" in
      1)
        warn "Sua versão será mantida."
        warn "As alterações do servidor nesses arquivos serão descartadas."

        if ! confirm "Deseja continuar?"; then
          continue
        fi

        run git checkout --ours .
        run git add -A
        run git commit -m "merge: keep local version"

        success "Conflitos resolvidos usando sua versão"
        break
        ;;

      2)
        warn "A versão do servidor será mantida."
        warn "Suas alterações locais nesses arquivos serão descartadas."

        if ! confirm "Deseja continuar?"; then
          continue
        fi

        run git checkout --theirs .
        run git add -A
        run git commit -m "merge: keep remote version"

        success "Conflitos resolvidos usando versão do servidor"
        break
        ;;

      3)
        echo
        warn "Resolva os conflitos manualmente."
        warn "Depois execute o script novamente."

        exit 0
        ;;

      *)
        error "Opção inválida"
        ;;
    esac
  done
}

handle_pending_merge() {
  if ! is_merge_in_progress; then
    return
  fi

  step "Merge pendente detectado"

  if has_merge_conflicts; then
    resolve_merge_conflict
    return
  fi

  warn "Finalizando merge pendente"

  run git add -A
  run git commit --no-edit

  success "Merge finalizado"
}

# =========================================================
# SYNC
# =========================================================
sync_with_remote() {
  local branch="$1"

  step "Baixando atualizações do servidor"

  run git fetch origin

  if git diff --quiet HEAD "origin/$branch"; then
    success "Seu repositório já está atualizado"
    return
  fi

  warn "Atualizações encontradas no servidor"

  echo
  echo "As atualizações serão integradas ao seu repositório."
  echo

  if ! confirm "Deseja continuar?"; then
    warn "Operação cancelada."
    exit 0
  fi

  set +e
  run git pull --no-rebase origin "$branch"
  local pull_status=$?
  set -e

  if [[ $pull_status -ne 0 ]]; then
    if is_merge_in_progress; then
      resolve_merge_conflict
      return
    fi

    error "Erro ao atualizar repositório"
    exit "$pull_status"
  fi

  success "Atualizações recebidas"
}

# =========================================================
# PUSH
# =========================================================
push_changes() {
  local branch="$1"

  step "Enviando alterações para o servidor"

  if has_upstream; then
    run git push
  else
    run git push -u origin "$branch"
  fi

  success "Alterações enviadas"
}

# =========================================================
# MAIN
# =========================================================
main() {
  echo
  printf "%b\n" "${BOLD}========================================${RESET}"
  printf "%b\n" "${BOLD}SYNC EDUCACIONAL GIT${RESET}"
  printf "%b\n" "${BOLD}========================================${RESET}"

  validate_environment
  validate_remote
  setup_git_identity

  local branch
  branch="$(get_current_branch)"

  printf "\nBranch atual: %b\n" "${BOLD}$branch${RESET}"

  show_status

  handle_pending_merge
  commit_local_changes
  sync_with_remote "$branch"
  push_changes "$branch"

  echo
  printf "%b\n" "${GREEN}${BOLD}Sync concluído com sucesso.${RESET}"
  echo
}

main "$@"
