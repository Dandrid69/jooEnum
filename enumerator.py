from requester import Requester
from bs4 import BeautifulSoup, Comment
import re
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

class Enumerator:
    def __init__(self, url):
        self.url = url.rstrip('/')
        self.requester = Requester()
        self.users = set()
        self.errors = []

    def fetch(self, url):
        response = self.requester.get(url)
        if response:
            return response.text
        self.errors.append(f"Error al realizar la solicitud GET a {url}")
        return None

    def find_users_in_feed(self):
        print(Fore.CYAN + "Buscando usuarios en feed RSS...")
        feed_url = self.url + "/index.php?format=feed&type=rss"
        content = self.fetch(feed_url)
        if content:
            soup = BeautifulSoup(content, 'xml')
            for item in soup.find_all('item'):
                author = item.find('author')
                if author:
                    self.users.add(author.text.strip())

    def find_users_in_com_users_registration(self):
        print(Fore.CYAN + "Buscando usuarios a través de com_users&view=registration...")
        registration_url = self.url + "/index.php?option=com_users&view=registration"
        self._find_users_in_meta_tags(registration_url)

    def find_users_in_com_users_profile(self):
        print(Fore.CYAN + "Buscando usuarios a través de com_users&view=profile...")
        profile_url = self.url + "/index.php?option=com_users&view=profile"
        self._find_users_in_meta_tags(profile_url)

    def find_users_in_meta_tags(self):
        print(Fore.CYAN + "Buscando usuarios en los meta tags...")
        self._find_users_in_meta_tags(self.url)

    def _find_users_in_meta_tags(self, url):
        content = self.fetch(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                if 'author' in meta.get('name', '').lower():
                    self.users.add(meta['content'].strip())

    def find_users_in_com_content(self):
        print(Fore.CYAN + "Buscando usuarios a través de com_content...")
        for i in range(1, 10):
            content_url = self.url + f"/index.php?option=com_content&view=article&id={i}"
            content = self.fetch(content_url)
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                author_tag = soup.find('meta', attrs={'name': 'author'})
                if author_tag:
                    self.users.add(author_tag['content'].strip())

    def find_users_in_author_files(self):
        print(Fore.CYAN + "Buscando usuarios a través de archivos de autores...")
        for i in range(1, 10):
            author_url = self.url + f"/index.php?option=com_content&view=author&id={i}"
            content = self.fetch(author_url)
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                author_name = soup.find('h1')
                if author_name:
                    self.users.add(author_name.text.strip())

    def find_users_in_source_code(self):
        print(Fore.CYAN + "Buscando usuarios en el código fuente...")
        content = self.fetch(self.url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            comments = soup.findAll(text=lambda text: isinstance(text, Comment))
            for comment in comments:
                if 'usuario' in comment or 'user' in comment:
                    self.users.add(comment.strip())

    def find_users_in_config_files(self):
        print(Fore.CYAN + "Buscando usuarios en archivos de configuración y otros directorios expuestos...")
        possible_paths = ['/configuration.php', '/robots.txt', '/administrator/manifests/files/joomla.xml']
        for path in possible_paths:
            config_url = self.url + path
            content = self.fetch(config_url)
            if content:
                if 'user' in content or 'author' in content:
                    self.users.add(content.strip())

    def suggest_google_dorks(self):
        print(Fore.YELLOW + "\nSugerencias de Google Dorks para enumerar usuarios:")
        dorks = [
            "site:{} inurl:index.php?option=com_users&view=profile".format(self.url),
            "site:{} inurl:index.php?option=com_users&view=registration".format(self.url),
            "site:{} inurl:author".format(self.url),
            "site:{} inurl:feed&type=rss".format(self.url)
        ]
        for dork in dorks:
            print(Fore.GREEN + dork)

    def enumerate_users(self):
        self.find_users_in_feed()
        self.find_users_in_com_users_registration()
        self.find_users_in_com_users_profile()
        self.find_users_in_meta_tags()
        self.find_users_in_com_content()
        self.find_users_in_author_files()
        self.find_users_in_source_code()
        self.find_users_in_config_files()
        self.suggest_google_dorks()

        print(Fore.MAGENTA + "\nEnumeración de usuarios finalizada.")
        if self.users:
            print(Fore.GREEN + "Usuarios encontrados:")
            for user in self.users:
                print(Fore.RED + user)
        else:
            print(Fore.RED + "No se encontraron usuarios.")
