//! Hundred Crayfish Legion – core cluster orchestration engine.
//!
//! This crate will host the high-concurrency agent scheduler, distributed
//! state memory, and gRPC service implementations as they land.

/// Library version (see `Cargo.toml`).
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Placeholder: reports how many “crayfish” slots the build supports (demo).
pub fn demo_agent_capacity() -> u32 {
    128
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn version_nonempty() {
        assert!(!VERSION.is_empty());
    }
}
