# golden/crash-loop

A fixture for end-to-end checks, not a sample to copy.

The branch root is a `busybox` image whose start command prints `starting`, waits two seconds, prints `boom` and exits with status 1. It does that on every start, so a service deployed from it never runs: it fails to start, again and again. A check uses that to watch how a start failure with an unrecognized log line is reported.

Changes go through a pull request. Checks pin this branch's commit, so a change here shows up as "fixture changed", not as a product failure.

The other fixtures are on `main`.
