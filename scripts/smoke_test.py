#!/usr/bin/env python3
"""Phase 0 smoke test: connect to CARLA, spawn ego, read telemetry."""

from __future__ import annotations

import argparse
import sys
import time

try:
    import carla
except ImportError:
    print(
        "ERROR: carla Python package not found.\n"
        "Install from your CARLA release wheel, e.g.:\n"
        "  pip install /path/to/CARLA/PythonAPI/carla/dist/carla-0.9.15-*.whl\n"
        "See docs/SETUP.md for full instructions.",
        file=sys.stderr,
    )
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=2000)
    parser.add_argument("--town", default="Town03")
    parser.add_argument("--steps", type=int, default=50, help="sim ticks to run")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    client = carla.Client(args.host, args.port)
    client.set_timeout(10.0)

    print(f"Connecting to CARLA at {args.host}:{args.port} ...")
    world = client.load_world(args.town)
    print(f"Loaded map: {world.get_map().name}")

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.1
    world.apply_settings(settings)

    blueprint_library = world.get_blueprint_library()
    ego_bp = blueprint_library.filter("vehicle.tesla.model3")[0]
    spawn_points = world.get_map().get_spawn_points()
    if not spawn_points:
        print("ERROR: no spawn points on this map", file=sys.stderr)
        return 1

    ego = world.spawn_actor(ego_bp, spawn_points[0])
    print(f"Spawned ego actor id={ego.id}")

    ego.apply_control(carla.VehicleControl(throttle=0.4, steer=0.0, brake=0.0))

    for step in range(args.steps):
        world.tick()
        transform = ego.get_transform()
        velocity = ego.get_velocity()
        loc = transform.location
        speed = (velocity.x**2 + velocity.y**2 + velocity.z**2) ** 0.5
        print(
            f"step={step:03d} "
            f"pos=({loc.x:.2f}, {loc.y:.2f}, {loc.z:.2f}) "
            f"speed={speed:.2f} m/s"
        )
        time.sleep(0.05)

    ego.destroy()
    world.tick()

    settings.synchronous_mode = False
    world.apply_settings(settings)

    print("Smoke test PASSED — telemetry readable, ego spawned and destroyed cleanly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
