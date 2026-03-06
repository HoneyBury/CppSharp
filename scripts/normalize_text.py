import argparse
from pathlib import Path

TEXT_SUFFIXES_BOM = {
    ".h", ".hpp", ".c", ".cc", ".cpp", ".inl",
    ".cmake", ".md", ".txt", ".yml", ".yaml",
}

TEXT_SUFFIXES_NO_BOM = {".py", ".sh", ".bat", ".ps1", ".json"}

SPECIAL_BOM_NAMES = {"CMakeLists.txt"}

SKIP_DIRS = {
    ".git", ".idea", ".vscode", ".direnv", "build", "cmake-build-debug",
    ".conan2",
}

SKIP_FILES = {"CMakeUserPresets.json", "CMakePresets.json"}


def is_binary(data: bytes) -> bool:
    return b"\x00" in data


def normalize_newlines(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text and not text.endswith("\n"):
        text += "\n"
    return text


def target_mode(path: Path):
    if path.name in SPECIAL_BOM_NAMES or path.suffix in TEXT_SUFFIXES_BOM:
        return "bom"
    if path.suffix in TEXT_SUFFIXES_NO_BOM:
        return "utf8"
    return None


def process_file(path: Path, check_only: bool) -> bool:
    raw = path.read_bytes()
    if is_binary(raw):
        return False

    mode = target_mode(path)
    if mode is None:
        return False

    text = raw.decode("utf-8-sig")
    normalized = normalize_newlines(text)

    if mode == "bom":
        expected = normalized.encode("utf-8-sig")
    else:
        expected = normalized.encode("utf-8")

    if expected != raw:
        if check_only:
            return True
        path.write_bytes(expected)
        return True
    return False


def iter_files(root: Path):
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SKIP_FILES:
            continue
        yield p


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize text files encoding and line endings.")
    parser.add_argument("--check", action="store_true", help="Check only, do not modify files.")
    args = parser.parse_args()

    changed = []
    for file_path in iter_files(Path(".")):
        if process_file(file_path, args.check):
            changed.append(str(file_path))

    if args.check and changed:
        print("Files need normalization:")
        for item in changed:
            print(f"  {item}")
        return 1

    if not args.check:
        print(f"Normalized {len(changed)} file(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
