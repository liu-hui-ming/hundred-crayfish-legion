//! Concurrent crayfish (agent) execution with bounded in-flight work (Tokio).
//!
//! P1 foundation: a testable kernel primitive mirroring the Python `swarm_demo` shape.

use std::sync::Arc;
use std::time::{Duration, Instant};

use tokio::sync::Semaphore;
use tokio::time::sleep;

/// One completed crayfish result.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CrayfishResult {
    pub id: u32,
    pub label: String,
}

/// Output of [`CrayfishSwarm::run_demo_swarm_timed`]: results plus wall-clock duration.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SwarmRunTiming {
    pub results: Vec<CrayfishResult>,
    pub elapsed: Duration,
}

/// P1 Crayfish swarm: bounded-parallel async execution of agent "ticks".
#[derive(Debug, Clone)]
pub struct CrayfishSwarm {
    sem: Arc<Semaphore>,
    cap: usize,
}

impl CrayfishSwarm {
    /// `max_in_flight` is the Tokio semaphore capacity (at least 1).
    pub fn new(max_in_flight: usize) -> Self {
        let n = max_in_flight.max(1);
        Self {
            sem: Arc::new(Semaphore::new(n)),
            cap: n,
        }
    }

    /// Maximum concurrent agent tasks.
    pub fn in_flight_capacity(&self) -> usize {
        self.cap
    }

    /// Run agents `0..count` with a small async delay per agent; results sorted by `id`.
    pub async fn run_demo_swarm(&self, count: u32) -> Vec<CrayfishResult> {
        let mut handles = Vec::with_capacity(count as usize);
        for id in 0..count {
            let sem = self.sem.clone();
            let h = tokio::spawn(async move {
                let _permit = sem
                    .acquire()
                    .await
                    .expect("semaphore is never closed in demo swarm");
                let ms = 20 + (id as u64 % 6) * 20;
                sleep(Duration::from_millis(ms)).await;
                CrayfishResult {
                    id,
                    label: format!("crayfish-{id}"),
                }
            });
            handles.push(h);
        }
        let mut out: Vec<CrayfishResult> = Vec::with_capacity(count as usize);
        for h in handles {
            out.push(h.await.expect("crayfish task join"));
        }
        out.sort_by_key(|r| r.id);
        out
    }

    /// Same as [`Self::run_demo_swarm`], plus monotonic elapsed time (for metrics / parity with HTTP API).
    pub async fn run_demo_swarm_timed(&self, count: u32) -> SwarmRunTiming {
        let t0 = Instant::now();
        let results = self.run_demo_swarm(count).await;
        SwarmRunTiming {
            results,
            elapsed: t0.elapsed(),
        }
    }
}

/// Policy upper bound: max crayfish *slots* the product stack targets (P1).
pub const DEFAULT_CRAYFISH_MAX_SLOTS: u32 = 9_999;

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};

    #[tokio::test]
    async fn bounded_swarm_runs_all_ids() {
        let swarm = CrayfishSwarm::new(4);
        let r = swarm.run_demo_swarm(16).await;
        assert_eq!(r.len(), 16);
        assert_eq!(r[0].label, "crayfish-0");
        assert_eq!(r[15].label, "crayfish-15");
    }

    #[tokio::test]
    async fn empty_swarm_returns_no_results() {
        let swarm = CrayfishSwarm::new(4);
        let r = swarm.run_demo_swarm(0).await;
        assert!(r.is_empty());
    }

    #[tokio::test]
    async fn swarm_respects_in_flight_cap() {
        let max_in_flight = 3_usize;
        let task_count = 12_usize;
        let sem = Arc::new(Semaphore::new(max_in_flight));
        let current = Arc::new(AtomicUsize::new(0));
        let peak = Arc::new(AtomicUsize::new(0));
        let mut handles = Vec::with_capacity(task_count);
        for _ in 0..task_count {
            let sem = sem.clone();
            let current = current.clone();
            let peak = peak.clone();
            handles.push(tokio::spawn(async move {
                let _permit = sem.acquire().await.expect("semaphore open");
                let n = current.fetch_add(1, Ordering::SeqCst) + 1;
                peak.fetch_max(n, Ordering::SeqCst);
                sleep(Duration::from_millis(8)).await;
                current.fetch_sub(1, Ordering::SeqCst);
            }));
        }
        for h in handles {
            h.await.expect("task join");
        }
        assert_eq!(
            peak.load(Ordering::SeqCst),
            max_in_flight,
            "peak concurrent tasks should hit the semaphore capacity"
        );
    }

    #[tokio::test]
    async fn timed_swarm_reports_nonzero_elapsed() {
        let swarm = CrayfishSwarm::new(8);
        let t = swarm.run_demo_swarm_timed(4).await;
        assert_eq!(t.results.len(), 4);
        assert!(!t.elapsed.is_zero());
    }
}
