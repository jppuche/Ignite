# Step 1.0: Platform Detection

Detect the operating system from the environment context (platform field).

> **Adaptive:** If `USER_LEVEL == "guided"`, auto-configure silently without AskUserQuestion. Report result as a single line. If auto-configuration fails, display a warning and continue (do not ask). If `USER_LEVEL == "advanced"`, use the full interactive flow below. See [ref-adaptive-ux.md](ref-adaptive-ux.md) (Phase Behavior Table).

```
If platform == "win32":
  1. Check if environment variable CLAUDE_CODE_GIT_BASH_PATH is set:
     - Run: echo $CLAUDE_CODE_GIT_BASH_PATH (or check environment context)
  2. If NOT set:
     - [Advanced] Warn user and use AskUserQuestion:
       "Windows detectado. Los hooks Python del workflow (lorekeeper-commit-gate,
        lorekeeper-session-end) necesitan Git Bash para ejecutar validate-docs.sh.
        Sin Git Bash configurado, la validacion de documentacion NO funcionara."
       "Configurar CLAUDE_CODE_GIT_BASH_PATH automaticamente?"
         1. Si — buscar git bash y configurar (Recomendado)
         2. No — continuar sin hooks funcionales
     - [Guided] Auto-search for Git Bash (skip AskUserQuestion):
       Log: "Configuring Git Bash..." → search → if found, configure → report result.
       If not found: warn "Git Bash not found — doc validation hooks won't work. Install Git for Windows to enable them."
     - If configuring (Advanced Si, or Guided auto):
       a. Search for Git Bash: check common paths
          - "C:\Program Files\Git\bin\bash.exe"
          - "C:\Program Files (x86)\Git\bin\bash.exe"
          - Run: where git (extract parent path)
       b. If found: set in .claude/settings.json env section:
          {
            "env": {
              "CLAUDE_CODE_GIT_BASH_PATH": "<detected_path>"
            }
          }
          Note: merge with existing settings.json if it exists (e.g., Agent Teams config).
       c. If NOT found: inform user to install Git for Windows and set manually.
  3. If set: report "Git Bash configurado: {path}" and continue.
  4. PYTHON_CMD = "python"

If platform == "darwin":
  1. Verify Python 3: run python3 --version
     - If available: report "macOS detectado. Python 3: {version}. Hooks funcionaran correctamente."
     - If NOT available:
       - [Advanced] Warn and use AskUserQuestion:
         "macOS detectado. Los hooks del workflow requieren Python 3.
          Sin Python 3, los hooks de documentacion y seguridad NO funcionaran."
         "Instalar Python 3?"
           1. Instalar con xcode-select --install (Recomendado)
           2. Continuar sin hooks funcionales
           3. Ya esta instalado (en otra ruta)
         - If option 1: run xcode-select --install, then re-check python3 --version
         - If option 3: ask for the path, verify it works
       - [Guided] Auto-attempt xcode-select --install (skip AskUserQuestion):
         Log: "Installing Python 3 via Xcode tools..." → attempt → report result.
         If fails: warn "Python 3 not available — hooks won't work. Install Python 3 manually to enable them."
  2. PYTHON_CMD = "python3"

If platform == "linux":
  1. Verify Python 3: run python3 --version
     - If available: report "Linux detectado. Python 3: {version}. Hooks funcionaran correctamente."
     - If NOT available:
       Warn user:
         "Linux detectado. Los hooks del workflow requieren Python 3.
          Instalar con el gestor de paquetes de tu distribucion:
          Ubuntu/Debian: sudo apt install python3
          Fedora: sudo dnf install python3
          Arch: sudo pacman -S python"
  2. PYTHON_CMD = "python3"
```

Store PYTHON_CMD for Step 3.2 and Step 4.4 (hook command configuration).

> **Nota cross-platform:** `CLAUDE_CODE_GIT_BASH_PATH` es usado por los hooks Python `lorekeeper-commit-gate.py` y `lorekeeper-session-end.py` para invocar `bash` como subproceso al ejecutar `validate-docs.sh`. Los comandos de hooks en `settings.local.json` usan paths relativos (no `$CLAUDE_PROJECT_DIR`) para compatibilidad cross-platform. El comando Python (`python` en Windows, `python3` en macOS/Linux) se determina en este paso y se usa en Step 3.2 y Step 4.4.
