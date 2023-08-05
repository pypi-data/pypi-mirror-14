# -*- coding: utf-8 -*-
import itertools
import logging
import shutil

from path import path

from .prepare import convert_bcf, bam2cram_script, submit_sbatch

logger = logging.getLogger(__name__)


def prepare_archive(vcf_file, bam_files, hum_ref, project, jobname=None,
                    email=None, std_dir='/tmp', dry_run=False):
    """Prepare for archiving an OLD case."""
    vcf_path = path(vcf_file)
    bcf_name = vcf_path.basename().replace('.vcf', '.bcf')
    bcf_out = vcf_path.dirname().joinpath(bcf_name)
    logger.debug("convert {} to {}".format(vcf_path, bcf_out))
    convert_bcf(vcf_path, bcf_out, dry_run=dry_run)

    logger.debug('convert BAM files to CRAM')
    files = [(bam_file, bam_file.replace('.bam', '.cram')) for bam_file
             in bam_files]
    script = bam2cram_script(files, hum_ref, project, email=email,
                             jobname=jobname, std_dir=std_dir)
    if not dry_run:
        submit_sbatch(script)
    return script


def archive(assets, bundle_dir, force=False, dry_run=False):
    """Archive the case by bundling the most relevant files."""
    bundle_path = path(bundle_dir)
    assets, assets_copy = itertools.tee(assets)

    # check if source files exists
    for asset in assets:
        if not path(asset.file).exists():
            if not force:
                raise OSError("can't locate file: %s", asset.file)
        else:
            logger.debug("file exists: %s", asset.file)

    # move files
    for asset in assets_copy:
        source_file = path(asset.file)
        dest_path = bundle_path.joinpath(asset.category)
        logger.debug("ensuring destination: %s", dest_path)
        if not dry_run:
            dest_path.makedirs_p()
        try:
            logger.debug("move %s -> %s", source_file, dest_path)
            if not dry_run:
                source_file.move(dest_path)
        except (IOError, shutil.Error) as error:
            logger.warn("couldn't move %s -> %s", source_file, dest_path)
            if not force:
                raise error
            else:
                continue
        logger.info("moved %s -> %s", source_file, dest_path)
