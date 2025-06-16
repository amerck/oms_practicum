import os
from pathlib import Path
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright


BINARY_EXTS = {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".zip", ".docx", ".xlsx"}


class WebCrawler:

    def __init__(self, domain, state_path, output_dir):
        """
        Initialize Playwright Web Crawler

        :param domain: base domain for site to crawl
        :param state_path: directory for Playwright state file
        :param output_dir: directory to write scraped HTML data to
        """
        base_url = 'https://%s' % domain
        self.domain = domain
        self.output_dir = output_dir
        self.visited = set()
        self.queue = [base_url]
        self.base_url = base_url

        # Initialize Playwright instance
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.context.storage_state(path=state_path)


    def authenticate(self, auth_url, auth_verification_url):
        """
        Authenticate to website prior to crawling

        :param auth_url: URL to authenticate against
        :param auth_verification_url: URL to verify authentication success
        :return: None
        """
        page = self.fetch_page(url=auth_url)
        page.wait_for_url(auth_verification_url)
        print('Authenticated')


    def fetch_page(self, url):
        """
        Fetch page from URL

        :param url: URL of page to fetch
        :return: Playwright Page() instance
        """
        page = self.context.new_page()
        try:
            page.goto(url)
        except Exception as e:
            print(f"Could not load page {url}: {e}")
        return page


    def start_crawling(self):
        """
        Crawl website for all identified URLs

        :return: None
        """
        while self.queue:
            # Fetch next URL from queue, and check if it's already been visited
            url = self.queue.pop(0)
            if url in self.visited:
                continue
            self.visited.add(url)

            print(f"Crawling: {url}")
            parsed = urlparse(url)
            ext = Path(parsed.path).suffix.lower()

            # If the fetched page is a binary file, write the binary to archive
            if ext in BINARY_EXTS:
                self.save_binary(self.context, url)
            # Otherwise, handle as an HTML file
            else:
                page = self.fetch_page(url)
                self.save_html(page, url)

                # Fetch all links on page and store in queue
                for a in page.query_selector_all("a[href]"):
                    href = a.get_attribute("href")
                    if not href or href.startswith("mailto:"):
                        continue

                    next_url = urljoin(self.base_url, href.split("#")[0])
                    parsed2 = urlparse(next_url)
                    hostname = parsed2.hostname or ""

                    if hostname.endswith(self.domain) and next_url not in self.visited:
                        self.queue.append(next_url)
                page.close()


    @staticmethod
    def validate_dir(path):
        """
        Ensure directory exists, and create directory if it doesn't exist

        :param path: Path to verify
        :return: None
        """
        p = os.path.dirname(path)
        if p and not os.path.exists(p):
            os.makedirs(p, exist_ok=True)


    def save_html(self, page, url):
        """
        Save HTML page to archive

        :param page: Playwright Page() instance
        :param url: URL of page to save
        :return: None
        """
        try:
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Could not load page {url}: {page.url}, {e}")
        parsed = urlparse(url)
        path = parsed.path
        if not path or path.endswith("/"):
            path = (path or "/") + "index.html"
        elif not Path(path).suffix:
            path += ".html"

        local_path = os.path.join(self.output_dir, path.lstrip("/"))
        self.validate_dir(local_path)
        with open(local_path, "w", encoding='utf-8') as f:
            f.write(page.content())


    def save_binary(self, context, url):
        """
        Save binary file to archive

        :param context: Playwright Context() instance
        :param url: URL of binary file to save
        :return: None
        """
        parsed = urlparse(url)
        local_path = os.path.join(self.output_dir, parsed.path.lstrip("/"))
        self.validate_dir(local_path)
        response = context.request.get(url)
        if response.ok:
            with open(local_path, "wb") as f:
                f.write(response.body())
        else:
            print(f"Could not save binary file {url}: {response.status}")