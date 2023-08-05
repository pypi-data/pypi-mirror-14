# PyMIP [![PyPI version][fury-image]][fury-url] [![Build Status][travis-image]][travis-url]
Provides a Python API to manipulate the [MIP][mip] analysis pipeline: setup, starting, monitoring, and parsing output.


## Features

* TODO

### Archive analysis
After a case has been solved or abandoned it is necessary to wrap up the analysis and archive the results. Pymip will handle this task by bundling the most vital assets from the output and deleting the rest.

Assets that are kept:

- CRAM file as a source of the raw (aligned) reads
- BCF file as a source of all (unannotated) variants
- QC metrics as a source for quality metrics

Pymip will not touch any of the files under "exomes/genomes" only "analysis". Physically the files will be collected in a folder under "exomes/genomes" names "archive". The script will also update the `AnalysisRunStatus` in the QC sample info file to `Archived`.


## Install for development

```bash
$ pip install --editable .
```


## Contributing
Anyone can help make this project better - read [CONTRIBUTING](CONTRIBUTING.md) to get started!


## License
MIT. See the [LICENSE](LICENSE) file for more details.


[fury-url]: http://badge.fury.io/py/pymip
[fury-image]: https://badge.fury.io/py/pymip.png

[travis-url]: https://travis-ci.org/Clinical-Genomics/pymip
[travis-image]: https://img.shields.io/travis/Clinical-Genomics/pymip.svg?style=flat

[mip]: http://mip-api.readthedocs.org/en/latest/
