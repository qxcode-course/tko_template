#!/usr/bin/env bash
set -Eeuo pipefail

# =========================================================
# CONFIG
# =========================================================
readonly DEFAULT_COMMIT_MESSAGE="sync update"
readonly ALLOWED_BRANCH="main"
readonly GIT="git"

# =========================================================
# LOGGING
# =========================================================

readonly LOG_DIR=".synclogs"
readonly LOG_TIMESTAMP="$(date +"%Y-%m-%d_%H-%M-%S")"
readonly LOG_FILE="$LOG_DIR/$LOG_TIMESTAMP.log"

mkdir -p "$LOG_DIR"

exec > >(tee -a "$LOG_FILE") 2>&1

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
# ERROR HANDLING
# =========================================================
trap 'error "Falha inesperada."' ERR
trap 'echo; warn "Operação cancelada pelo usuário."' INT

# =========================================================
# UI
# =========================================================
step() {
  printf "%b\n" "${BLUE}${BOLD}==>${RESET} ${BOLD}$1${RESET}"
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
  local default_yes="${2:-true}"
  local answer

  if [[ "$default_yes" == "true" ]]; then
    read -r -p "$prompt [Y/n] (Enter confirma): " answer

    case "${answer,,}" in
      ""|y|yes|s|sim)
        return 0
        ;;
      *)
        return 1
        ;;
    esac
  else
    read -r -p "$prompt [y/N]: " answer

    case "${answer,,}" in
      y|yes|s|sim)
        return 0
        ;;
      *)
        return 1
        ;;
    esac
  fi
}

# =========================================================
# GIT HELPERS
# =========================================================
is_merge_in_progress() {
  $GIT rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1
}

has_merge_conflicts() {
  $GIT diff --name-only --diff-filter=U | grep -q .
}

has_local_changes() {
  ! $GIT diff --quiet || ! $GIT diff --cached --quiet
}

has_remote() {
  $GIT remote get-url origin >/dev/null 2>&1
}

has_upstream() {
  $GIT rev-parse --abbrev-ref --symbolic-full-name "@{u}" \
    >/dev/null 2>&1
}

has_commits_to_push() {
  if ! has_upstream; then
    return 0
  fi

  [[ "$($GIT rev-list --count "@{u}..HEAD")" -gt 0 ]]
}

remote_has_updates() {
  local branch="$1"

  local ahead_behind
  ahead_behind="$(
    $GIT rev-list --left-right --count HEAD..."origin/$branch"
  )"

  local behind
  behind="$(echo "$ahead_behind" | awk '{print $2}')"

  [[ "$behind" -gt 0 ]]
}

safe_ls_remote() {
  if command -v timeout >/dev/null 2>&1; then
    timeout 15 $GIT ls-remote origin >/dev/null 2>&1
  else
    $GIT ls-remote origin >/dev/null 2>&1
  fi
}

# =========================================================
# VALIDATION
# =========================================================
validate_environment() {
  step "Validando ambiente"

  if ! $GIT rev-parse --is-inside-work-tree >/dev/null 2>&1; then
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

  if ! safe_ls_remote; then
    error "Não foi possível conectar ao servidor remoto."
    warn "Verifique sua internet ou permissões."
    exit 1
  fi

  success "Conexão com servidor OK"
}

get_current_branch() {
  local branch

  branch="$($GIT rev-parse --abbrev-ref HEAD)"

  if [[ "$branch" == "HEAD" ]]; then
    error "Você está em HEAD destacado."
    warn "Volte para uma branch antes de continuar."
    exit 1
  fi

  if [[ "$branch" != "$ALLOWED_BRANCH" ]]; then
    error "Branch inválida: $branch"
    warn "Esse script deve ser executado apenas na branch '$ALLOWED_BRANCH'."
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

  git_user_name="$($GIT config --get user.name || true)"
  git_user_email="$($GIT config --get user.email || true)"

  if [[ -z "$git_user_name" ]]; then
    local name

    warn "Seu nome não está configurado no git."
    name="$(ask "Digite seu nome: ")"

    if [[ -z "$name" ]]; then
      error "Nome não pode ser vazio."
      exit 1
    fi

    run $GIT config user.name "$name"
  fi

  if [[ -z "$git_user_email" ]]; then
    local email

    warn "Seu email não está configurado no git."
    email="$(ask "Digite seu email: ")"

    if [[ -z "$email" ]]; then
      error "Email não pode ser vazio."
      exit 1
    fi

    run $GIT config user.email "$email"
  fi

  success "Identidade git configurada"
}

# =========================================================
# STATUS
# =========================================================
show_status() {
  step "Resumo do repositório (?? = arquivo novo, M = modificado, D = deletado, UU = conflito)"
  run $GIT status --short || true
}

# =========================================================
# COMMIT
# =========================================================
git_commit_changes() {
  local msg="$1"
  run $GIT commit -m "$msg"
}

commit_local_changes() {
  step "Verificando alterações locais"

  if ! has_local_changes; then
    success "Nenhuma alteração local encontrada"
    return
  fi

  if ! confirm "Deseja salvar essas alterações agora?"; then
    warn "Operação cancelada pelo usuário."
    exit 0
  fi

  run $GIT add -A

  if $GIT diff --cached --quiet; then
    warn "Nenhuma alteração pronta para commit."
    return
  fi

  warn "Resumo das alterações:"
  run $GIT diff --cached --stat

  local changed_files
  changed_files="$($GIT diff --cached --name-only | wc -l | tr -d ' ')"

  echo "Quantidade de arquivos alterados: $changed_files"
  warn "Escreva uma mensagem curta descrevendo o que mudou."

  local msg

  while true; do
    msg="$(ask "Mensagem do commit: ")"

    msg="${msg#"${msg%%[![:space:]]*}"}"
    msg="${msg%"${msg##*[![:space:]]}"}"

    if [[ -z "$msg" ]]; then
      error "A mensagem de commit não pode ser vazia."
      continue
    fi

    break
  done

  git_commit_changes "$msg"

  success "Alterações salvas"
}

# =========================================================
# MERGE CONFLICTS
# =========================================================
resolve_merge_conflict() {
  step "Conflitos detectados"

  echo
  warn "Você e o servidor modificaram os mesmos arquivos."
  warn "O Git precisa saber qual versão deve ser mantida."
  echo

  local conflicts
  conflicts="$($GIT diff --name-only --diff-filter=U)"

  echo "$conflicts"

  while read -r file; do
    [[ -z "$file" ]] && continue

    echo
    echo "Arquivo em conflito:"
    echo "  $file"

    while true; do
      echo
      echo "  1) Manter MINHA versão"
      echo "  2) Manter versão do SERVIDOR"
      echo "  3) Resolver manualmente"
      echo

      local choice
      choice="$(ask "> ")"

      case "$choice" in
        1)
          run $GIT checkout --ours -- "$file"
          run $GIT add "$file"
          break
          ;;

        2)
          run $GIT checkout --theirs -- "$file"
          run $GIT add "$file"
          break
          ;;

        3)
          warn "Resolva manualmente e execute novamente."
          exit 0
          ;;

        *)
          error "Opção inválida"
          ;;
      esac
    done

  done <<< "$conflicts"

  if ! $GIT diff --cached --quiet; then
    run $GIT commit -m "resolve merge conflicts"
  fi

  success "Conflitos resolvidos"
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

  run $GIT add -A
  run $GIT commit --no-edit

  success "Merge finalizado"
}

# =========================================================
# SYNC
# =========================================================
sync_with_remote() {
  local branch="$1"

  step "Baixando atualizações do servidor"

  run $GIT fetch origin

  if ! remote_has_updates "$branch"; then
    success "Seu repositório já está atualizado"
    return
  fi

  warn "Atualizações encontradas no servidor"

  echo
  warn "Pressione Ctrl+C para cancelar."
  echo

  if ! confirm "Deseja continuar?"; then
    warn "Operação cancelada."
    exit 0
  fi

  set +e

  # Primeiro tenta fast-forward puro
  run $GIT merge --ff-only "origin/$branch"
  local merge_status=$?

  # Se não conseguir fast-forward, tenta merge normal
  if [[ $merge_status -ne 0 ]]; then
    warn "Fast-forward não foi possível."
    warn "Tentando merge automático."

    run $GIT merge "origin/$branch"
    merge_status=$?
  fi

  set -e

  if [[ $merge_status -ne 0 ]]; then
    if is_merge_in_progress; then
      resolve_merge_conflict
      return
    fi

    error "Erro ao atualizar repositório"
    exit "$merge_status"
  fi

  success "Atualizações recebidas"
}

# =========================================================
# PUSH
# =========================================================
push_changes() {
  local branch="$1"

  step "Enviando alterações para o servidor"

  if ! has_commits_to_push; then
    success "Nenhum commit novo para enviar"
    return
  fi

  if has_upstream; then
    if ! $GIT push --dry-run >/dev/null 2>&1; then
      error "Push rejeitado pelo servidor."
      exit 1
    fi

    run $GIT push
  else
    run $GIT push -u origin "$branch"
  fi

  success "Alterações enviadas"
}

# =========================================================
# SUMMARY
# =========================================================
show_final_summary() {
  step "Resumo final"

  printf "%b\n" "${GREEN}✓${RESET} alterações salvas"
  printf "%b\n" "${GREEN}✓${RESET} repositório atualizado"
  printf "%b\n" "${GREEN}✓${RESET} alterações enviadas"
  step "Log salvo em:  $LOG_FILE"
}

# =========================================================
# MAIN
# =========================================================
main() {
  echo
  printf "%b\n" "${BOLD}========================================${RESET}"
  printf "%b\n" "${BOLD}SYNC EDUCACIONAL GIT${RESET}"
  printf "%b\n" "${BOLD}========================================${RESET}"

  warn "Esse script executa comandos git automaticamente."
  warn "Leia as mensagens antes de confirmar operações."
  warn "Pressione Ctrl+C para cancelar."
  step "Log salvo em:  $LOG_FILE"

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

  show_final_summary

  printf "%b\n" "${GREEN}${BOLD}Sync concluído com sucesso.${RESET}"
}

main "$@"
