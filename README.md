# DropGuard Lite

A minimal drop-style e-commerce API for detecting reseller bots using log-based risk scoring. This repo starts with product and cart endpoints plus session handling.


## Feature Calendar

| **Issue** | **Due date** | |
| --------- | ------------ | -- |
| [Product page + inventory model](https://github.com/gt63dd/juniorIS/issues/1) | 2/19/26 | |
| [Cart endpoints (add, remove, update)](https://github.com/gt63dd/juniorIS/issues/2) | 2/26/26 | |
| [Checkout + simulated purchase](https://github.com/gt63dd/juniorIS/issues/3) | 3/4/26 | |
| [Session management (session ID cookie)](https://github.com/gt63dd/juniorIS/issues/4) | 3/11/26 | |
| [Structured event logging to SQLite](https://github.com/gt63dd/juniorIS/issues/5) | 3/18/26 | |
| [Navigation-feature extraction from event logs](https://github.com/gt63dd/juniorIS/issues/6) | 3/25/26 | |
| [Risk scoring function (0–1 bot likelihood)](https://github.com/gt63dd/juniorIS/issues/7) | 4/1/26 | |
| [Mitigation policy gates (allow, delay, throttle, challenge)](https://github.com/gt63dd/juniorIS/issues/8) | 4/8/26 | |
| [Bot simulator (fast-path bot)](https://github.com/gt63dd/juniorIS/issues/9) | 4/15/26 | |
| [Bot simulator (burst/polling bot)](https://github.com/gt63dd/juniorIS/issues/10) | 4/22/26 | |
| [Bot simulator (stealth bot)](https://github.com/gt63dd/juniorIS/issues/11) | 4/29/26 | |
| [Human session simulator](https://github.com/gt63dd/juniorIS/issues/12) | 5/6/26 | |
| [Experiment runner for drop trials](https://github.com/gt63dd/juniorIS/issues/13) | 5/13/26 | |
| [Metrics + reporting (tables/plots)](https://github.com/gt63dd/juniorIS/issues/14) | 5/20/26 | |
| [Adaptive bot stress test (Stretch)](https://github.com/gt63dd/juniorIS/issues/15) | 5/27/26 | |
| [Admin dashboard for sessions and scores (Stretch)](https://github.com/gt63dd/juniorIS/issues/16) | 6/3/26 | |

## Quickstart

- Product listing and detail endpoints live under `/products`.
- Cart endpoints live under `/cart` and use a session cookie.

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn dropguard.app:app --reload --app-dir src
```

### Run tests

```bash
pytest
```
