//! Run: `cargo run -p hcl-core --example swarm_tokio`
//! Demonstrates the P1 Rust kernel: bounded-parallel crayfish (same family as `examples/swarm_demo.py`).

use hcl_core::CrayfishSwarm;

#[tokio::main]
async fn main() {
    let n: u32 = std::env::args()
        .nth(1)
        .and_then(|s| s.parse().ok())
        .unwrap_or(8);
    let n = n.clamp(1, 256);
    let swarm = CrayfishSwarm::new(32);
    eprintln!("[HCL:rust] Spawning {n} concurrent agent tasks (kernel)…");
    let results = swarm.run_demo_swarm(n).await;
    let line: String = results
        .iter()
        .map(|r| r.label.as_str())
        .collect::<Vec<_>>()
        .join(", ");
    eprintln!("[HCL:rust] Done: {line}");
}
