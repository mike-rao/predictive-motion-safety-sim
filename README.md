# predictive-motion-safety-sim

Prediction-aware safety validation in CARLA: train a trajectory predictor, compare **prediction-aware** vs **reactive** planning on a fixed scenario set, and report collision/TTC metrics.

**Start here:** [TODO.md](TODO.md) (step-by-step build checklist)  
**CARLA install:** [docs/SETUP.md](docs/SETUP.md)

---

## Repo layout

```
predictive-motion-safety-sim/
├── configs/           # YAML configs (default + per-scenario)
├── control/           # ego vehicle control
├── data/              # trajectory datasets (raw + processed)
├── docs/              # setup guides
├── eval/              # batch eval, metrics, plots
├── logs/              # run logs (gitignored)
├── planning/          # safety check + state machine
├── predictor/         # model, training, inference
├── scenarios/         # scenario definitions + generated configs
├── scripts/           # one-off utilities (smoke test, etc.)
├── requirements.txt
├── TODO.md            # master build checklist
└── README.md
```

---

## Quick start (Phase 0)

1. Follow [docs/SETUP.md](docs/SETUP.md) to install CARLA 0.9.15 + Python API + Scenario Runner
2. Create venv and install deps: `pip install -r requirements.txt`
3. Start CARLA server, then run: `python scripts/smoke_test.py --town Town03`
4. Check off Phase 0 items in [TODO.md](TODO.md), then proceed to Phase 1

---

## Default settings

- **Map:** `Town03` (see `configs/default.yaml`)
- **Sim rate:** 10 Hz (`fixed_delta_seconds: 0.1`)
- **Comparison:** `planning.mode: prediction_aware` vs `reactive`

---

## Architecture (target end state)

```
CARLA World
    ↓
Perception (ground truth + optional noise)
    ↓
Predictor (LSTM) ──→ future agent trajectories
    ↓
Planning (occupancy check + state machine)
    ↓
Control (throttle / brake / steer)
    ↓
Eval harness (batch runs + metrics)
```

Full wiring happens in Phases 5–7. See TODO.md for file-level deliverables per phase.
