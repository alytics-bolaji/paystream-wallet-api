# paystream-wallet-api

The Paystream Kenya wallet API (staging) and its systemd service unit.

Until this week, this code and its deploy config lived in one engineer's notes
and a zip on a shared drive. From now on, this repository is the single source
of truth: every change is a commit, and nothing reaches `main` except through a
reviewed pull request.

## What's here
- `wallet-api.js` -- the Node.js service (endpoints: `/health`, `/wallet/:id`)
- `paystream-wallet.service` -- the systemd unit that runs it (see Week 4)

## Run it locally
    node wallet-api.js
    curl http://localhost:3000/health
    # -> {"status":"ok","estate":"kenya-staging"}

## How we work here
- `main` is protected and always releasable.
- Do your work on a branch, then open a pull request.
- A teammate reviews before anything merges.
