# Hundred Crayfish Legion · 百龙虾军团

**Canonical repository:** [`liu-hui-ming/hundred-crayfish-legion`](https://github.com/liu-hui-ming/hundred-crayfish-legion) · Affiliated with the **Carbon–Silicon Alliance** initiative.

## What this is

**Hundred Crayfish Legion** is a **high-concurrency multi-agent cluster orchestration** stack: it coordinates large swarms of specialized agents so they can run complex, long-horizon work together. The project is meant to provide **compute and coordination backbone** for **Carbon–Silicon Alliance**–class, **full-domain collaboration**—not a single chatbot, but the **machinery of swarm intelligence**.

**Core manifest — Computing Power Singularity:** we treat the end of the “move bits through copper in 3D forever” era as a first-class design constraint. The public line is simple: *end the century-long reign of von Neumann–style bottlenecks for serious AI engineering*; see the **[Manifesto](https://github.com/liu-hui-ming/hundred-crayfish-legion/issues)**-tagged issues on this repo for the full narrative.

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
git clone https://github.com/liu-hui-ming/hundred-crayfish-legion.git
cd hundred-crayfish-legion
python examples/swarm_demo.py
```

More demo agents, e.g. 16:

```bash
python examples/swarm_demo.py -n 16
```

## Rust core (scaffold)

```bash
cd core
cargo test
```

## License

This project is released under the **[MIT License](LICENSE)**.

## Issue title conventions (for maintainers & contributors)

All **official** front-page–style issues on this repository use a **fixed English prefix** in the **title** so visitors can scan by category:

| Prefix | Use for |
|--------|--------|
| `[Announcement]` | Project news, releases, and community-facing notices |
| `[Manifesto]` | Foundational vision and position statements (e.g. compute singularity, architecture philosophy) |
| `[P1-Roadmap]` | Phased engineering roadmaps and milestone plans (P1…Pn and related “detonate”/rollout tracks) |

**Format:** `Prefix` + space + short descriptive title, e.g.  
`[Manifesto] Computing Power Singularity: End Von Neumann’s Century-Long Reign`  
`[P1-Roadmap] XIAN & Axium Dual-Core Awakening: P1–P6 Open Roadmap`

Do not drop the bracketed prefix on new issues in these categories so the issue list stays consistent and machine- and human-readable.
