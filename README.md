# golden/env-names

A fixture for end-to-end checks, not a sample to copy.

The branch root is a Python app with no dependencies that serves on `$PORT` (3000 when it isn't set). It answers one question: did the running app start with these environment variables?

- `GET /` answers `golden/env-names fixture`.
- `GET /env-names?names=A,B,C` answers `{"present": [...], "missing": [...]}` (JSON, `nosniff`, `no-store`) for the asked names only: 1 to 10 names like `DATABASE_URL`. Anything else is a 400 with a fixed sentence that never repeats the input.

It never shows a value, a length or a hash, and never a name it wasn't asked about. A check links secrets to a service, then asks for exactly those names, so it sees what the app got and not only what the console lists.

Changes go through a pull request. Checks pin this branch's commit, so a change here shows up as "fixture changed", not as a product failure. `python3 -m unittest test_server` runs the tests.

The other fixtures are on `main`.
