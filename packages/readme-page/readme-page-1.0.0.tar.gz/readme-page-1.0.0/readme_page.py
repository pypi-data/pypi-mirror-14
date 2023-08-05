#!/usr/bin/env python
'''
This script creates a simple readme GitHub Page for a repository.

The page is only based on the README.md of the master branch of your project
repository that is retrieved automatically by the remote origin url.

The building and deployment of a GitHub Page is done by mkdocs.
The following resources are created to build and deploy a page with mkdocs:

    * mkdocs.yml - mkdocs configuration file
    * docs - documentation folder
    * docs/index.md - Index page of the documentation

Author: Fernando Felix do Nascimento Junior
License: MIT License
Homepage: https://github.com/fernandojunior/readme-page
'''
import os
import re
import yaml
import subprocess
from six.moves.urllib.request import urlopen
from six.moves.urllib.request import urlretrieve
from bs4 import BeautifulSoup


def cmd(s):
    '''Execute the command (a string) in a subshell and return its output.'''
    return subprocess.check_output(s.split()).decode('utf-8').strip()


def create_configuration(repo_url):
    '''Create configuration with its settings based on the repository.'''
    soup = BeautifulSoup(urlopen(repo_url).read(), 'html.parser')

    site_name = str(soup.select('article h1')[0].contents[1])
    site_description = str(soup.select('meta[name=description]')[0]['content'])

    data = dict(
        repo_url=repo_url,
        site_name=site_name,
        site_description=site_description,
        theme='bootstrap'
    )

    with open('mkdocs.yml', 'w') as f:
        f.write(yaml.dump(data, default_flow_style=False))


def create_index(repo_url):
    '''Create the index of the documentation with the repository readme.'''
    readme_url = repo_url + '/raw/master/README.md'
    urlretrieve(readme_url, 'docs/index.md')


def create_docs():
    '''Create the documentation folder if it does not already exist.'''
    if not os.path.exists('docs'):
        os.makedirs('docs')


def credits():
    '''TODO Append readme-page credits in site/index.html.'''
    homepage = re.findall('[hH]omepage:\s*(.*)', __doc__)[0]
    brand = 'readme-page'
    with open('site/index.html') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    cred = ' and <a href="%s">%s</a>.' % (homepage, brand)
    soup.select('footer p')[0].contents[2].replace_with(BeautifulSoup(cred))
    html = str(soup)
    with open('site/index.html', "w") as f:
        f.write(html)


def resources():
    '''Create the resources needed to build and deploy a GitHub page.'''
    remote_url = cmd('git config --get remote.origin.url')
    protocol = 'https'
    domain, username, repo_name = re.split(r'[@:/]', remote_url)[1:]
    repo_name = repo_name.replace('.git', '')
    repo_url = '%s://%s/%s/%s' % (protocol, domain, username, repo_name)
    create_configuration(repo_url)
    create_docs()
    create_index(repo_url)


def build():
    '''Build a page/site with mkdocs. The resources must be created.'''
    cmd('mkdocs build --clean')


def deploy():
    '''Deploy a page/site with mkdocs to gh-pages branch of the repository.'''
    cmd('mkdocs gh-deploy --clean')


def main():
    resources()
    build()
    deploy()

if __name__ == '__main__':
    main()
