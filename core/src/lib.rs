//! Hundred Crayfish Legion – **P1** cluster orchestration kernel.
//!
//! Provides version metadata and a **Tokio**-based bounded-parallel *crayfish* swarm
//! for agent-style workloads; gRPC and distributed state are later phases.

pub mod scheduler;

pub use scheduler::{CrayfishResult, CrayfishSwarm, DEFAULT_CRAYFISH_MAX_SLOTS};

/// Library version (see `Cargo.toml`).
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Reports the configured maximum crayfish *slots* (separate from per-run in-flight).
#[must_use]
pub fn max_crayfish_slots() -> u32 {
    DEFAULT_CRAYFISH_MAX_SLOTS
}

/// Back-compat name used by early demos: default slot ceiling.
#[must_use]
pub fn demo_agent_capacity() -> u32 {
    max_crayfish_slots()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn version_nonempty() {
        assert!(!VERSION.is_empty());
    }
}
