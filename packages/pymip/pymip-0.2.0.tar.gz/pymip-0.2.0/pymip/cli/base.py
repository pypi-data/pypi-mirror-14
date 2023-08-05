# -*- coding: utf-8 -*-
import codecs
import logging

import click
from path import path
import yaml

import pymip
from .log import LEVELS, setup_logging
from .archive import archive
from .prepare import prepare

logger = logging.getLogger(__name__)


@click.group()
@click.option('-c', '--config', show_default=True,
              type=click.Path(exists=True), help='path to config file')
@click.option('-l', '--log', type=click.Path(), help='path to log file')
@click.option('-v', '--level', default='INFO', type=click.Choice(LEVELS))
@click.version_option(pymip.__version__)
@click.pass_context
def base(context, config, log, level):
    """MIP and downstream processing of data at Clinical Genomics."""
    # read in config values
    config_file = config or path('~/.pymip.yaml').expanduser()
    if path(config_file).exists():
        with codecs.open(config_file, 'r') as stream:
            context.obj = yaml.load(stream)
    else:
        context.obj = {}

    # setup logging handlers
    setup_logging(log, stderr_level=level)
    logger.debug("Running v%s", pymip.__version__)


base.add_command(archive)
base.add_command(prepare)
