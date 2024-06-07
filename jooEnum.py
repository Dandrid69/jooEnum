from enumerator import Enumerator
import sys
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

def print_ascii_art():
    art = """
    ██╗ ██████╗  ██████╗ ███╗   ███╗
    ██║██╔════╝ ██╔═══██╗████╗ ████║
    ██║██║  ███╗██║   ██║██╔████╔██║
    ██║██║   ██║██║   ██║██║╚██╔╝██║
    ██║╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
    ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
    """
    print(Fore.CYAN + art)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(Fore.RED + f"Uso: {sys.argv[0]} <URL del sitio Joomla>")
        sys.exit(1)

    print_ascii_art()

    url = sys.argv[1]
    enumerator = Enumerator(url)
    enumerator.enumerate_users()
