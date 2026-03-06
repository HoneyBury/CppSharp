set -euo pipefail

MODE="fix"
if [[ "${1:-}" == "--check" ]]; then
  MODE="check"
fi

mapfile -t files < <(git ls-files '*.h' '*.hpp' '*.c' '*.cc' '*.cpp' '*.inl')
if [[ "${#files[@]}" -eq 0 ]]; then
  echo "No C/C++ files found."
  exit 0
fi

CLANG_FORMAT_BIN="${CLANG_FORMAT_BIN:-}"
if [[ -z "${CLANG_FORMAT_BIN}" ]]; then
  if command -v clang-format >/dev/null 2>&1; then
    CLANG_FORMAT_BIN="clang-format"
  elif [[ -x "/opt/homebrew/opt/llvm/bin/clang-format" ]]; then
    CLANG_FORMAT_BIN="/opt/homebrew/opt/llvm/bin/clang-format"
  else
    echo "clang-format not found. Set CLANG_FORMAT_BIN or add it to PATH."
    exit 127
  fi
fi

if [[ "${MODE}" == "check" ]]; then
  "${CLANG_FORMAT_BIN}" --dry-run --Werror "${files[@]}"
  echo "clang-format check passed."
else
  "${CLANG_FORMAT_BIN}" -i "${files[@]}"
  echo "clang-format applied to ${#files[@]} files."
fi
