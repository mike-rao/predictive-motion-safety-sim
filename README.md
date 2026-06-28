# predictive-motion-safety-sim

Prediction-aware safety validation in CARLA: train a trajectory predictor, compare **prediction-aware** vs **reactive** planning on a fixed scenario set, and report collision/TTC metrics.

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

