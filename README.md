# Hundred Crayfish Legion

High-concurrency multi-agent cluster orchestration for autonomous task
execution, by the [Carbon-Silicon Alliance](https://github.com/CarbonSiliconAlliance).

## Project layout

```
/hundred-crayfish-legion
├── core/          # Cluster orchestration engine (Rust)
├── agents/        # Prebuilt agent roles ("crayfish")
├── protocols/     # Communication standards (gRPC; planned)
├── examples/      # Sample use cases
└── docs/          # Technical documentation
```

## Tech stack (direction)

- **Core:** Rust (orchestration, concurrency) + Python (AI integration)
- **Protocol:** gRPC (planned) for inter-agent communication

## Quick start (demo)

Requires **Python 3.10+** (no extra packages for the default demo).

```bash
cd hundred-crayfish-legion
python examples/swarm_demo.py
```

Optional: more demo agents, e.g. 16.

```bash
python examples/swarm_demo.py -n 16
```

## Rust core (scaffold)

```bash
cd core
cargo test
```

## License

See [LICENSE](LICENSE).
