# Contributing

Contributions that improve reproducibility, metadata, portability, or error
handling are welcome.

1. Open an issue describing the scientific or technical problem.
2. Create a focused branch and avoid modifying numerical source data unless the
   change is documented and justified.
3. Run `python tools/validate_repository.py`.
4. Regenerate affected figures and record any numerical or visual differences.
5. Rebuild `MANIFEST.tsv` with `python tools/build_manifest.py`.
6. In the pull request, identify the manuscript figures, tables, or methods
   affected by the change.

Do not commit full trajectories, credentials, proprietary software, or files
without redistribution permission. Scientific corrections must preserve the
original file in release history and explain why a new version is needed.

