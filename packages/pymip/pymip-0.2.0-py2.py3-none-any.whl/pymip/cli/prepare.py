# -*- coding: utf-8 -*-
import logging

import click

from pymip.api import load_analysis
from pymip.archive import family_args, prepare_archive

logger = logging.getLogger(__name__)


@click.command()
@click.option('-r', '--hum-ref', type=click.File('r'))
@click.option('-p', '--project')
@click.option('-e', '--email')
@click.option('--dry-run', is_flag=True)
@click.argument('family_dir')
@click.pass_context
def prepare(context, hum_ref, project, email, family_dir, dry_run):
    """Prepare an old analysis to be archived."""
    try:
        analysis = load_analysis(family_dir)
        args = family_args(analysis)
    except ValueError as error:
        logger.warn(error.message)
        context.abort()

    hum_ref = hum_ref or context.obj['hum_ref']
    email = email or context.obj['email']
    project = project or context.obj['project']
    if (hum_ref is None) or (project is None):
        logger.error("you must supply reference and project")
        context.abort()

    logger.debug("launch archive for an analysis")
    std_dir = context.obj['log_dir']
    script = prepare_archive(args.vcf_file, args.bam_files, hum_ref, project,
                             jobname=args.jobname, email=email,
                             dry_run=dry_run, std_dir=std_dir)
    if dry_run:
        click.echo(script)
