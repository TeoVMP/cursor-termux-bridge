"""
Sistema de sincronización con Git para cambios bidireccionales.
"""
import subprocess
import os
from pathlib import Path
from typing import Optional, Tuple, List


class GitSync:
    def __init__(self, repo_path: str = "."):
        """Inicializa el sincronizador Git."""
        self.repo_path = Path(repo_path).resolve()
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
    
    def _run_git(self, *args, check: bool = True) -> Tuple[int, str, str]:
        """Ejecuta un comando git y retorna (exit_code, stdout, stderr)."""
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout.strip(), e.stderr.strip()
        except FileNotFoundError:
            raise RuntimeError("Git is not installed or not in PATH")
    
    def is_git_repo(self) -> bool:
        """Verifica si el directorio es un repositorio Git."""
        exit_code, _, _ = self._run_git("rev-parse", "--git-dir", check=False)
        return exit_code == 0
    
    def init_repo(self) -> bool:
        """Inicializa un nuevo repositorio Git si no existe."""
        if self.is_git_repo():
            return False
        
        exit_code, _, _ = self._run_git("init", check=False)
        return exit_code == 0
    
    def get_status(self) -> dict:
        """Obtiene el estado del repositorio."""
        if not self.is_git_repo():
            return {"is_repo": False}
        
        exit_code, stdout, stderr = self._run_git("status", "--porcelain", check=False)
        
        changes = []
        if stdout:
            for line in stdout.split("\n"):
                if line.strip():
                    status = line[:2]
                    file = line[3:]
                    changes.append({"status": status, "file": file})
        
        # Obtener información de branch
        exit_code_branch, branch, _ = self._run_git("branch", "--show-current", check=False)
        current_branch = branch if exit_code_branch == 0 else "unknown"
        
        # Verificar si hay commits
        exit_code_log, log, _ = self._run_git("log", "-1", "--oneline", check=False)
        has_commits = exit_code_log == 0
        
        return {
            "is_repo": True,
            "current_branch": current_branch,
            "has_commits": has_commits,
            "changes": changes,
            "has_changes": len(changes) > 0
        }
    
    def add(self, files: Optional[List[str]] = None) -> bool:
        """Añade archivos al staging area."""
        if files:
            args = ["add"] + files
        else:
            args = ["add", "."]
        
        exit_code, _, _ = self._run_git(*args, check=False)
        return exit_code == 0
    
    def commit(self, message: str = "Auto-sync from Termux") -> bool:
        """Hace commit de los cambios."""
        exit_code, _, _ = self._run_git("commit", "-m", message, check=False)
        return exit_code == 0
    
    def push(self, remote: str = "origin", branch: Optional[str] = None) -> Tuple[bool, str]:
        """Hace push de los cambios al repositorio remoto."""
        if branch is None:
            exit_code, branch, _ = self._run_git("branch", "--show-current", check=False)
            if exit_code != 0:
                return False, "Could not determine current branch"
            branch = branch.strip()
        
        exit_code, stdout, stderr = self._run_git("push", remote, branch, check=False)
        return exit_code == 0, stdout + "\n" + stderr if stderr else stdout
    
    def pull(self, remote: str = "origin", branch: Optional[str] = None) -> Tuple[bool, str]:
        """Hace pull de los cambios del repositorio remoto."""
        if branch is None:
            exit_code, branch, _ = self._run_git("branch", "--show-current", check=False)
            if exit_code != 0:
                return False, "Could not determine current branch"
            branch = branch.strip()
        
        exit_code, stdout, stderr = self._run_git("pull", remote, branch, check=False)
        return exit_code == 0, stdout + "\n" + stderr if stderr else stdout
    
    def sync_push(self, message: str = "Auto-sync from Termux") -> Tuple[bool, str]:
        """Sincroniza cambios haciendo add, commit y push."""
        status = self.get_status()
        if not status["is_repo"]:
            return False, "Not a git repository"
        
        if not status["has_changes"]:
            return True, "No changes to sync"
        
        # Add cambios
        if not self.add():
            return False, "Failed to add changes"
        
        # Commit
        if not self.commit(message):
            return False, "Failed to commit changes"
        
        # Push
        success, output = self.push()
        if not success:
            return False, f"Failed to push: {output}"
        
        return True, "Successfully synced changes"
    
    def sync_pull(self) -> Tuple[bool, str]:
        """Sincroniza cambios haciendo pull."""
        status = self.get_status()
        if not status["is_repo"]:
            return False, "Not a git repository"
        
        success, output = self.pull()
        if not success:
            return False, f"Failed to pull: {output}"
        
        return True, output or "Successfully pulled changes"
    
    def sync_bidirectional(self, message: str = "Auto-sync from Termux") -> Tuple[bool, str]:
        """Sincroniza bidireccionalmente: pull primero, luego push."""
        status = self.get_status()
        if not status["is_repo"]:
            return False, "Not a git repository"
        
        # Pull primero
        pull_success, pull_output = self.sync_pull()
        if not pull_success:
            return False, f"Pull failed: {pull_output}"
        
        # Luego push
        push_success, push_output = self.sync_push(message)
        if not push_success:
            return False, f"Push failed: {push_output}"
        
        return True, f"Pull: {pull_output}\nPush: {push_output}"


def sync_from_termux(repo_path: str = ".", message: str = "Auto-sync from Termux") -> Tuple[bool, str]:
    """Función helper para sincronizar desde Termux."""
    sync = GitSync(repo_path)
    return sync.sync_push(message)


def sync_to_termux(repo_path: str = ".") -> Tuple[bool, str]:
    """Función helper para sincronizar hacia Termux."""
    sync = GitSync(repo_path)
    return sync.sync_pull()
