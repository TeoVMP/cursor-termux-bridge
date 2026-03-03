from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

console = Console()


def print_result(title: str, text: str) -> None:
    console.print(Panel.fit(text, title=title))


def print_kv(data: dict) -> None:
    for key, value in data.items():
        console.print(f"[bold]{key}[/bold]: {value}")
