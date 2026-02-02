"""
Display utilities for rich terminal output.

Provides consistent formatting for the CLI interface.
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style

console = Console()

# Styles
HEADER_STYLE = Style(color="cyan", bold=True)
SUCCESS_STYLE = Style(color="green")
WARNING_STYLE = Style(color="yellow")
ERROR_STYLE = Style(color="red", bold=True)
DIM_STYLE = Style(dim=True)


def print_header():
    """Print the application header."""
    header = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🔍  CRYPTO RESEARCH AGENT                                   ║
║                                                               ║
║   AI-powered cryptocurrency market research                   ║
║   Using Claude Agent SDK, Skills & Subagents                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    console.print(header, style=HEADER_STYLE)


def print_status(message: str):
    """Print a status message."""
    console.print(f"\n[bold blue]→[/bold blue] {message}")


def print_success(message: str):
    """Print a success message."""
    console.print(f"[green]✓[/green] {message}")


def print_warning(message: str):
    """Print a warning message."""
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_error(message: str):
    """Print an error message."""
    console.print(f"[red bold]✗ Error:[/red bold] {message}")


def print_subagent_dispatch(name: str, task: str):
    """Print subagent dispatch notification."""
    icons = {
        "price_analyst": "📊",
        "news_aggregator": "📰",
        "social_sentinel": "🌐",
    }
    icon = icons.get(name, "🤖")
    console.print(f"  {icon} [cyan]{name}[/cyan]: {task}")


def print_subagent_result(name: str, status: str, details: str = ""):
    """Print subagent completion status."""
    if status == "complete":
        console.print(f"  [green]✓[/green] [cyan]{name}[/cyan] complete {f'[dim]({details})[/dim]' if details else ''}")
    elif status == "failed":
        console.print(f"  [red]✗[/red] [cyan]{name}[/cyan] failed: [dim]{details}[/dim]")
    else:
        console.print(f"  [yellow]?[/yellow] [cyan]{name}[/cyan]: {status}")


def print_report(report: str):
    """Print the final research report."""
    console.print("\n")
    console.print(Panel(
        Markdown(report),
        title="[bold cyan]Research Report[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))


def print_section(title: str, content: str):
    """Print a collapsible section."""
    console.print(Panel(
        content,
        title=f"[bold]{title}[/bold]",
        border_style="blue",
    ))


def create_metrics_table(metrics: dict) -> Table:
    """Create a formatted metrics table."""
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Value", justify="right")
    
    for key, value in metrics.items():
        table.add_row(key, str(value))
    
    return table


def print_confidence(level: str):
    """Print confidence level with appropriate styling."""
    colors = {
        "high": "green",
        "medium": "yellow",
        "low": "red",
    }
    color = colors.get(level.lower(), "white")
    console.print(f"[bold]Confidence:[/bold] [{color}]{level.upper()}[/{color}]")


def create_progress() -> Progress:
    """Create a progress indicator for long operations."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    )


def print_debug(message: str):
    """Print debug message (only shown when DEBUG=true)."""
    console.print(f"[dim][DEBUG] {message}[/dim]")