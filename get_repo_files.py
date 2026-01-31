import subprocess
import os

def clone_repo(repo_url, target_dir="repos"):
    os.makedirs(target_dir, exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1]
    repo_path = os.path.join(target_dir, repo_name)

    if os.path.exists(repo_path):
        print("Repo already cloned")
        return repo_path

    subprocess.run(
        ["git", "clone", repo_url, repo_path],
        check=True
    )

    return repo_path




def get_all_files(repo_path):
    files = []

    # folders to completely skip
    EXCLUDED_DIRS = {"public", ".git", "node_modules"}

    # file extensions to ignore
    EXCLUDED_EXTENSIONS = {
        ".json",
        ".css",
        ".gif",
        ".png",
        ".jpg",
        ".jpeg",
        ".svg",
        ".ico"
    }

    # exact filenames to ignore
    EXCLUDED_FILES = {
        "package.json",
        "package-lock.json",
        "readme.md",
        ".gitignore"
    }

    for root, dirs, filenames in os.walk(repo_path):
        # remove excluded directories from traversal
        dirs[:] = [d for d in dirs if d.lower() not in EXCLUDED_DIRS]

        for filename in filenames:
            lower_name = filename.lower()

            # skip exact file matches
            if lower_name in EXCLUDED_FILES:
                continue

            # skip excluded extensions
            if os.path.splitext(lower_name)[1] in EXCLUDED_EXTENSIONS:
                continue

            full_path = os.path.join(root, filename)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    files.append((full_path, f.read()))
            except Exception:
                # fail-safe: skip unreadable files
                continue

    return files