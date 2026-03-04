from colorama import Fore, Style, init

init(autoreset=True)

def success(text: str) -> str:
    return Fore.GREEN + text + Style.RESET_ALL

def warning(text: str) -> str:
    return Fore.YELLOW + text + Style.RESET_ALL

def danger(text: str) -> str:
    return Fore.RED + text + Style.RESET_ALL

def info(text: str) -> str:
    return Fore.CYAN + text + Style.RESET_ALL