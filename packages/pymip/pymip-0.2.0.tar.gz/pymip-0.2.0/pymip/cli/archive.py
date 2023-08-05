# -*- coding: utf-8 -*-
import logging

import click
from path import path

from pymip.api import load_analysis
from pymip import archive as archive_mod

logger = logging.getLogger(__name__)


@click.command()
@click.option('-f', '--force', is_flag=True)
@click.option('-o', '--output', type=click.Path())
@click.option('-d', '--dry-run', is_flag=True)
@click.argument('family_dir')
@click.pass_context
def archive(context, force, output, dry_run, family_dir):
    """Archive an analysis."""
    analysis = load_analysis(family_dir)
    output_dir = output or path(analysis.family_dir).joinpath('archive')
    output_path = path(output_dir)

    if not force and output_path.exists() and output_path.listdir() != []:
        logger.warn("target directory not empty: %s", output_dir)
        context.abort()

    if force or click.confirm('Are you sure?'):
        logger.info("moving essential analysis files into: %s", output_dir)
        files = analysis.archive_files()
        archive_mod.analysis(files, output_dir, force=force, dry_run=dry_run)
    if force or click.confirm('Do you want to remove ALL analysis files?'):
        logger.info("removing directory tree: %s", analysis.analysis_dir)
        if not dry_run:
            path(analysis.analysis_dir).rmtree()

    if not dry_run:
        logger.info("updating status to 'Archived' with path: %s", output_dir)
        analysis.update_status('Archived', archive_path=output_dir)
