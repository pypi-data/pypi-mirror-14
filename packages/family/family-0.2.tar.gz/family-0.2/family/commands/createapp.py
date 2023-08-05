# coding=utf8

import click
import subprocess

@click.command()
@click.argument('project_name')
def create(project_name):
    cmd = 'paster create -t falcon %s' % project_name
    p = subprocess.Popen(cmd, shell=True)
    p.communicate()
