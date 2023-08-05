# -*- coding: utf-8 -*-
from collections import namedtuple
import codecs
from datetime import date
import logging
from pkg_resources import resource_filename
import subprocess
import uuid

from jinja2 import Template
from path import path

import pymip

logger = logging.getLogger(__name__)
ArchiveArgs = namedtuple('ArchiveArgs', ['vcf_file', 'bam_files', 'jobname'])


def family_args(analysis):
    if not analysis.is_old:
        raise ValueError("new cases don't require preprocessing")

    vcf_file = analysis.ready_vcf
    bam_files = analysis.lane_bams
    jobname = "BAM2CRAM_{}".format(analysis.family_id)

    return ArchiveArgs(vcf_file=vcf_file, bam_files=bam_files, jobname=jobname)


def convert_bcf(vcf, out, exe='bcftools', dry_run=False):
    """Convert a VCF to BCF + index."""
    view_command = [exe, 'view', vcf, '-O', 'b', '-o', out]
    logger.info("running command: %s", ' '.join(view_command))
    if not dry_run:
        view_code = subprocess.call(view_command)
    else:
        view_code = 0
    idx_command = [exe, 'index', out]
    logger.info("running command: %s", ' '.join(idx_command))
    if not dry_run:
        idx_code = subprocess.call(idx_command)
    else:
        idx_code = 0
    return view_code, idx_code


def submit_sbatch(script):
    """Submit an sbatch script."""
    unique_filename = "/tmp/{}".format(uuid.uuid4())
    with codecs.open(unique_filename, 'w') as stream:
        stream.write(script)
    logger.debug("storing script: %s", unique_filename)
    command = ['sbatch', unique_filename]
    logger.info("running command: %s", ' '.join(command))
    return subprocess.call(command)


def bam2cram_script(files, hum_ref, project, jobname=None, exe='sambamba',
                    email=None, cores=16, std_dir='/tmp'):
    """Populate a template for a script to convert BAM to CRAM."""
    pkg_dir = pymip.__package__
    template_dir = path(resource_filename(pkg_dir, 'templates'))
    template_file = template_dir.joinpath('sbatch-sambamba.j2')
    template_content = template_file.open().read()
    template = Template(template_content)
    jobname = jobname or "BAM2CRAM_{}".format(date.today())
    stdout = path(std_dir).joinpath("{}.stdout.log".format(jobname))
    stderr = path(std_dir).joinpath("{}.stderr.log".format(jobname))

    content = template.render(project=project, name=jobname, email=email,
                              files=files, hum_ref=hum_ref, cores=cores,
                              stdout=stdout, stderr=stderr)
    return content
