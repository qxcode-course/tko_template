#!/usr/bin/env bash
set -euo pipefail

# ============ HELPERS ============
ask() {
  local prompt="$1"
  read -r -p "$prompt" answer
  echo "$answer"
}

is_merge_in_progress() {
  git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1
}

has_merge_conflicts() {
  git diff --name-only --diff-filter=U | grep -q .
}

# ============ VALIDATION ============
validate_environment() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Erro: não está em um repositório git"
    exit 1
  fi
}

get_current_branch() {
  local branch
  branch="$(git rev-parse --abbrev-ref HEAD)"

  if [[ "$branch" == "HEAD" ]]; then
    echo "Erro: HEAD destacado"
    exit 1
  fi

  echo "$branch"
}

# ============ IDENTITY SETUP ============
setup_git_identity() {
  local git_user_name
  local git_user_email

  git_user_name="$(git config --get user.name || true)"
  git_user_email="$(git config --get user.email || true)"

  if [[ -z "${git_user_name}" ]]; then
    local name
    name="$(ask "Seu nome (git user.name): ")"
    [[ -z "$name" ]] && { echo "Nome não pode ser vazio"; exit 1; }
    git config user.name "$name"
    echo "user.name configurado localmente."
  fi

  if [[ -z "${git_user_email}" ]]; then
    local email
    email="$(ask "Seu email (git user.email): ")"
    [[ -z "$email" ]] && { echo "Email não pode ser vazio"; exit 1; }
    git config user.email "$email"
    echo "user.email configurado localmente."
  fi
}

# ============ CONFLICT HANDLING ============
resolve_merge_conflict() {
  echo "Conflitos detectados."

  while true; do
    echo "Escolha como resolver:"
    echo "  1) Manter LOCAL (ours)"
    echo "  2) Manter REMOTO (theirs)"
    echo "  3) Resolver manualmente"
    local choice
    choice="$(ask "> ")"

    case "$choice" in
      1)
        git checkout --ours .
        git add -A
        git commit -m "merge: keep local version"
        break
        ;;
      2)
        git checkout --theirs .
        git add -A
        git commit -m "merge: keep remote version"
        break
        ;;
      3)
        echo "Resolva os conflitos manualmente."
        echo "Os seguintes arquivos estão em conflito:"
        git diff --name-only --diff-filter=U
        echo "Depois de resolver, execute esse script novamente para continuar o sync."
        exit 0
        ;;
      *)
        echo "Opção inválida"
        ;;
    esac
  done
}

handle_pending_merge() {
  if ! is_merge_in_progress; then
    return
  fi

  echo "==> Merge em andamento detectado"

  if has_merge_conflicts; then
    resolve_merge_conflict
  else
    echo "==> Finalizando merge pendente"
    git add -A
    git commit --no-edit
  fi
}

# ============ SYNC OPERATIONS ============
sync_with_remote() {
  local branch="$1"

  echo "==> Fetching origin/$branch"
  git fetch origin

  if git diff --quiet HEAD "origin/$branch"; then
    echo "Sem novidades no servidor remoto"
    return
  fi

  echo "==> Merging origin/$branch"
  set +e
  git merge "origin/$branch"
  local merge_status=$?
  set -e

  if [[ $merge_status -ne 0 ]]; then
    if is_merge_in_progress; then
      resolve_merge_conflict
    else
      echo "Erro ao executar merge de origin/$branch"
      exit "$merge_status"
    fi
  fi
}

commit_local_changes() {
  git add -A

  if ! git diff --cached --quiet; then
    local changed_files
    local msg
    changed_files="$(git diff --cached --name-only | wc -l | tr -d ' ')"
    msg="$(ask "Qtd arquivos alterados nesse commit: $changed_files, insira a mensagem de commit: ")"
    msg="${msg:-sync update}"
    git commit -m "$msg"
  else
    echo "Nada para commitar."
  fi
}

push_changes() {
  local branch="$1"

  if git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >/dev/null 2>&1; then
    git push
  else
    git push -u origin "$branch"
  fi
}

# ============ MAIN ============
main() {
  validate_environment
  setup_git_identity
  local branch
  branch="$(get_current_branch)"

  handle_pending_merge
  sync_with_remote "$branch"
  commit_local_changes
  push_changes "$branch"

  echo "Sync concluído."
}

main "$@"
