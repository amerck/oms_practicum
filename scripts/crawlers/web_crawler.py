import os
import argparse
import configparser
from itso_ai.utils.web_crawler import WebCrawler


def main():
    parser = argparse.ArgumentParser(description='Crawls Microsoft Graph API for Teams messages.')
    parser.add_argument('-c', '--config', required=True, help='Configuration file')
    args = parser.parse_args()

    # Load settings
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(args.config))
    crawler_settings = config['crawler']

    domain = crawler_settings['domain']
    auth_url = crawler_settings['auth_url']
    auth_verification_url = crawler_settings['auth_verification_url']
    state_path = crawler_settings['state_path']
    output_dir = crawler_settings['output_dir']

    crawler = WebCrawler(domain=domain, state_path=state_path, output_dir=output_dir)
    crawler.authenticate(auth_url=auth_url, auth_verification_url=auth_verification_url)
    crawler.start_crawling()


if __name__ == "__main__":
    main()
