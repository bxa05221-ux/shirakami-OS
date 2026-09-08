# R0044 — CI Gate Status

## Current state

The experiment branch contains the R0044 CI Gate workflow and records. The next verification authority is the GitHub Actions pull-request run.

## Rule

Do not claim `success` until the dependent `gate` job has actually executed after `verify` and completed successfully.
