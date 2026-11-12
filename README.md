# golden/fixed-port

A fixture for end-to-end checks, not a sample to copy.

The branch root is a Node app with no dependencies that listens on port 3000 only. It ignores `PORT` on purpose, so a service deployed from it with any other port fails its health check. A check uses that to walk through deploy, fail, fix the port, redeploy.

Changes go through a pull request. Checks pin this branch's commit, so a change here shows up as "fixture changed", not as a product failure.

The other fixtures are on `main`.
