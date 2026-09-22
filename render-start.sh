#!/bin/sh
# Render's dockerCommand field does not reliably parse shell operators
# like "&&" when passed as a single inline string (seen failing two
# different ways: "&&" as a literal arg to alembic, and the whole
# compound string treated as one unresolvable command). A script file
# sidesteps that entirely — Render just runs it via `sh render-start.sh`.
set -e
alembic upgrade head
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
