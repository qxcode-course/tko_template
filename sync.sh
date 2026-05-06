#!/usr/bin/env bash
set -euo pipefail

# ---------- helpers ----------
ask() {
  local prompt="$1"
  read -r -p "$prompt" answer
  echo "$answer"
}

# ---------- checks ----------
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Erro: não está em um repositório git"
  exit 1
fi

# ---------- git identity (interativo, salva local) ----------
git_user_name="$(git config --get user.name || true)"
git_user_email="$(git config --get user.email || true)"

if [[ -z "${git_user_name}" ]]; then
  name="$(ask "Seu nome (git user.name): ")"
  [[ -z "$name" ]] && { echo "Nome não pode ser vazio"; exit 1; }
  git config user.name "$name"
  echo "user.name configurado localmente."
fi

if [[ -z "${git_user_email}" ]]; then
  email="$(ask "Seu email (git user.email): ")"
  [[ -z "$email" ]] && { echo "Email não pode ser vazio"; exit 1; }
  git config user.email "$email"
  echo "user.email configurado localmente."
fi

branch="$(git rev-parse --abbrev-ref HEAD)"

if [[ "$branch" == "HEAD" ]]; then
  echo "Erro: HEAD destacado"
  exit 1
fi

# ---------- pull ----------
echo "==> Fetching origin/$branch"
git fetch origin

echo "==> Merging origin/$branch"
set +e
git merge "origin/$branch"
merge_status=$?
set -e

# ---------- conflito ----------
if [[ $merge_status -ne 0 ]]; then
  echo "Conflitos detectados."

  while true; do
    echo "Escolha como resolver:"
    echo "  1) Manter LOCAL (ours)"
    echo "  2) Manter REMOTO (theirs)"
    echo "  3) Resolver manualmente"
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
        echo "Resolva os conflitos manualmente, depois pressione ENTER..."
        read -r
        if git diff --name-only --diff-filter=U | grep .; then
          echo "Ainda há conflitos não resolvidos."
        else
          git add -A
          git commit -m "merge: manual resolution"
          break
        fi
        ;;
      *)
        echo "Opção inválida"
        ;;
    esac
  done
fi

# ---------- mudanças locais ----------
git add -A

if ! git diff --cached --quiet; then
  msg="$(ask "Mensagem de commit: ")"
  msg="${msg:-sync update}"
  git commit -m "$msg"
else
  echo "Nada para commitar."
fi

# ---------- push ----------
if git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >/dev/null 2>&1; then
  git push
else
  git push -u origin "$branch"
fi

echo "Sync concluído."
