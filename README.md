<!-- BANNER -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0a1a0a,50:0d2a0d,100:103a10&fontColor=22c55e&descColor=a3e635&height=220&section=header&text=Autonomous%20Organism&fontSize=55&desc=Self-Evolving%20Digital%20Entity&animation=fadeIn" />

<!-- TYPING SVG -->
<div align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=22C55E&center=true&vCenter=true&width=600&lines=Parameter+Self-Adjustment+System;Digital+Evolution+Simulation;Experimental+Research+Project;Not+AGI+%7C+Not+Sentient+%7C+Bounded+Evolution" alt="Typing SVG" />
  </a>
</div>

<br/>

<!-- BADGES -->
<div align="center">

[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/Node.js-20+-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Research](https://img.shields.io/badge/Type-Research-22C55E?style=for-the-badge)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

</div>

---

## Overview

**Autonomous Organism** is an experimental research project exploring the concept of a self-evolving digital entity. Built in TypeScript, it implements a system where a software "organism" can adjust its own operational parameters — behavior patterns, response strategies, resource allocation — within defined bounds, simulating a form of digital adaptation and evolution.

This is a research artifact, not a product. It investigates questions about self-modifying systems, emergent behavior from simple rules, and the boundaries between programmed adaptation and genuine autonomy.

## Features

### Self-Adjustment Engine
- Parameter mutation within defined bounds
- Fitness-based selection of parameter configurations
- Environmental feedback integration
- Historical adaptation logging and analysis

### Organism Architecture
- Modular "cell" system with specialized functions
- Inter-cell communication protocols
- Resource allocation and energy management
- Lifecycle management (growth, adaptation, reproduction)

### Environmental System
- Simulated environment with variable conditions
- Stimulus generation and event scheduling
- Resource distribution modeling
- Ecosystem interaction simulation

### Evolution Mechanics
- Population-level evolution across organism instances
- Crossover and mutation operators
- Niching and speciation detection
- Convergence monitoring and diversity maintenance

### Observability
- Real-time parameter visualization
- Evolution timeline and lineage tracking
- Behavioral pattern analysis dashboards
- Export of evolution data for offline analysis

## Honest Notes

> **Clearing up misconceptions:**

- **Experimental Research Project** — This is a research prototype for studying self-modifying systems. It is not a product, service, or tool for general use.
- **"Self-Evolving" is Limited** — The self-evolution in this project refers to **parameter adjustment within pre-defined bounds**. The organism can tweak its own settings, not rewrite its fundamental code or create entirely new capabilities. This is bounded, constrained adaptation — not open-ended evolution.
- **Not AGI** — This project does not implement artificial general intelligence. The "organism" follows programmed rules with adjustable parameters. There is no understanding, consciousness, or general reasoning capability.
- **Not Sentient** — Despite the biological metaphor, the digital organism has no awareness, feelings, or subjective experience. Terms like "organism," "evolution," and "lifecycle" are metaphors for software patterns.
- **Emergent Behavior is Simple** — While the system can produce interesting emergent patterns, these emerge from the interaction of simple rules, not from any form of intelligence or intentionality.

## Quick Start

### Prerequisites
- Node.js 18+
- TypeScript 5.x

### Installation

```bash
git clone https://github.com/mulkymalikuldhrs/autonomous-organism.git
cd autonomous-organism
npm install
```

### Running

```bash
# Start with default configuration

<!-- AUTO-PACKAGE-BADGES:START -->

<!-- AUTO-PACKAGE-BADGES:END -->
npm run start

# Start with custom environment config
npm run start -- --config ./configs/complex-env.json

# Start observation dashboard
npm run observe

# Run evolution simulation
npm run simulate -- --generations 100 --population 50
```

### Configuration

```json
{
  "organism": {
    "initialParameters": {
      "adaptationRate": 0.1,
      "mutationRate": 0.05,
      "explorationFactor": 0.3
    },
    "bounds": {
      "adaptationRate": [0.01, 0.5],
      "mutationRate": [0.001, 0.2],
      "explorationFactor": [0.1, 0.9]
    }
  },
  "environment": {
    "resourceAbundance": 0.6,
    "volatility": 0.3,
    "stimulusFrequency": 1000
  }
}
```

## Project Structure

```
autonomous-organism/
├── src/
│   ├── organism/        # Core organism implementation
│   │   ├── cells/       # Specialized cell modules
│   │   ├── genome/      # Parameter & configuration management
│   │   └── lifecycle/   # Growth & adaptation phases
│   ├── environment/     # Simulated world
│   │   ├── stimuli/     # Environmental events
│   │   ├── resources/   # Resource modeling
│   │   └── ecosystem/   # Multi-organism interactions
│   ├── evolution/       # Population-level evolution
│   │   ├── selection/   # Fitness evaluation
│   │   ├── operators/   # Crossover & mutation
│   │   └── tracking/    # Lineage & history
│   ├── observation/     # Monitoring & visualization
│   └── types/           # TypeScript definitions
├── configs/             # Environment configurations
├── data/                # Evolution data exports
└── tests/               # Test suites
```

## Visual Architecture

> Interactive Mermaid diagrams showing organism lifecycle, cell interactions, and honest project limitations.

### 1. Organism Lifecycle — Biological Metaphor Pipeline

The digital organism follows a biological metaphor from sensing the environment to producing a response:

```mermaid
flowchart LR
    subgraph ENV["🌐 Environment"]
        STIM["Stimuli · Events<br/>Resource Signals<br/>Ecosystem Interactions"]
    end

    subgraph SENSE["👁️ Sense Cell"]
        S1["Perceive Stimuli"]
        S2["Filter Noise"]
        S3["Classify Input"]
        S1 --> S2 --> S3
    end

    subgraph DECISION["🧠 Decision Cell"]
        D1["Evaluate Options"]
        D2["Select Strategy"]
        D3["Allocate Resources"]
        D1 --> D2 --> D3
    end

    subgraph MEMORY["💾 Memory Cell"]
        M1["Store Experience"]
        M2["Recall Patterns"]
        M3["Update Weights"]
        M1 --> M2 --> M3
    end

    subgraph FACTORY["⚙️ Factory Cell"]
        F1["Execute Strategy"]
        F2["Generate Response"]
        F3["Apply Mutations"]
        F1 --> F2 --> F3
    end

    subgraph IMMUNE["🛡️ Immune Cell"]
        I1["Detect Anomalies"]
        I2["Quarantine Defects"]
        I3["Repair State"]
        I1 --> I2 --> I3
    end

    subgraph SCHED["⏰ Scheduler Cell"]
        T1["Queue Tasks"]
        T2["Prioritize Actions"]
        T3["Cycle Lifeclock"]
        T1 --> T2 --> T3
    end

    ENV --> SENSE --> DECISION
    DECISION --> MEMORY
    DECISION --> FACTORY
    FACTORY --> IMMUNE
    IMMUNE --> SCHED
    SCHED -->|Next Cycle| SENSE
    MEMORY -.->|Historical Context| DECISION

    style ENV fill:#0a1a0a,stroke:#22c55e,color:#fff
    style SENSE fill:#103a10,stroke:#a3e635,color:#fff
    style DECISION fill:#103a10,stroke:#22c55e,color:#fff
    style MEMORY fill:#103a10,stroke:#3b82f6,color:#fff
    style FACTORY fill:#103a10,stroke:#f59e0b,color:#fff
    style IMMUNE fill:#103a10,stroke:#ef4444,color:#fff
    style SCHED fill:#103a10,stroke:#8b5cf6,color:#fff
```

### 2. Cell System Architecture

Six specialized cell modules interact like biological cells — each with a defined role, communicating through inter-cell protocols:

```mermaid
flowchart TB
    subgraph ORGANISM["🧬 Digital Organism"]
        direction TB

        subgraph CELLS["Cell Modules"]
            SENSE["👁️ Sense Cell<br/><i>Perception Layer</i><br/>Stimulus Detection<br/>Input Classification<br/>Noise Filtering"]
            DECIDE["🧠 Decision Cell<br/><i>Cognitive Layer</i><br/>Strategy Selection<br/>Resource Allocation<br/>Option Evaluation"]
            MEM["💾 Memory Cell<br/><i>Storage Layer</i><br/>Experience Storage<br/>Pattern Recall<br/>Weight Updates"]
            FACT["⚙️ Factory Cell<br/><i>Execution Layer</i><br/>Strategy Execution<br/>Response Generation<br/>Mutation Application"]
            IMMUNE["🛡️ Immune Cell<br/><i>Protection Layer</i><br/>Anomaly Detection<br/>Defect Quarantine<br/>State Repair"]
            SCHED["⏰ Scheduler Cell<br/><i>Timing Layer</i><br/>Task Queuing<br/>Action Prioritization<br/>Lifecycle Clock"]
        end

        subgraph COMMS["🔀 Inter-Cell Communication"]
            BUS["Message Bus<br/>Structured Protocols<br/>Event-Driven Architecture"]
        end
    end

    subgraph GENOME["🧬 Genome — Parameter Configuration"]
        GEN["adaptationRate: 0.01–0.5<br/>mutationRate: 0.001–0.2<br/>explorationFactor: 0.1–0.9<br/><i>All mutations bounded</i>"]
    end

    SENSE & DECIDE & MEM & FACT & IMMUNE & SCHED <--> BUS
    BUS <--> GENOME

    style ORGANISM fill:#0a1a0a,stroke:#22c55e,color:#fff
    style CELLS fill:#0d2a0d,stroke:#22c55e,color:#fff
    style COMMS fill:#103a10,stroke:#a3e635,color:#fff
    style GENOME fill:#0d2a0d,stroke:#8b5cf6,color:#fff
    style SENSE fill:#14532d,stroke:#a3e635,color:#dcfce7
    style DECIDE fill:#14532d,stroke:#22c55e,color:#dcfce7
    style MEM fill:#14532d,stroke:#3b82f6,color:#dcfce7
    style FACT fill:#14532d,stroke:#f59e0b,color:#dcfce7
    style IMMUNE fill:#14532d,stroke:#ef4444,color:#dcfce7
    style SCHED fill:#14532d,stroke:#8b5cf6,color:#dcfce7
    style BUS fill:#166534,stroke:#a3e635,color:#fff
    style GEN fill:#1e1b4b,stroke:#8b5cf6,color:#e2e8f0
```

### 3. Evolution Mechanics

Fitness-based selection with bounded mutation — the organism adapts within defined constraints:

```mermaid
flowchart TD
    subgraph POP["🧬 Population"]
        P1["Organism A<br/><i>params: α=0.12, μ=0.04</i>"]
        P2["Organism B<br/><i>params: α=0.08, μ=0.07</i>"]
        P3["Organism C<br/><i>params: α=0.25, μ=0.02</i>"]
        P4["Organism D<br/><i>params: α=0.15, μ=0.09</i>"]
    end

    subgraph FIT["📊 Fitness Evaluation"]
        F1["Environmental<br/>Feedback Score"]
        F2["Resource Efficiency<br/>Measurement"]
        F3["Survival Metrics<br/>Assessment"]
        F1 --> F2 --> F3
    end

    subgraph SELECT["🎯 Selection"]
        S1["Rank by Fitness"]
        S2["Tournament / Roulette<br/>Selection"]
        S3["Niching and Speciation<br/>Diversity Maintenance"]
        S1 --> S2 --> S3
    end

    subgraph MUTATE["🧪 Mutation — Bounded"]
        M1["Parameter Tweak<br/><i>Within Pre-Defined Bounds</i>"]
        M2["Crossover<br/><i>Blend Two Organisms</i>"]
        M3["Diversity Check<br/><i>Convergence Monitor</i>"]
        M1 --> M2 --> M3
    end

    subgraph NEW["🐣 New Generation"]
        N1["Offspring Organisms<br/><i>Bounded Parameters Only</i>"]
        N2["Insert into Population"]
        N3["Repeat Evolution Cycle"]
        N1 --> N2 --> N3
    end

    POP --> FIT --> SELECT --> MUTATE --> NEW
    NEW -->|Next Generation| POP

    M1 -.->|Bounds Enforced| BOUNDS["⚠️ adaptationRate in 0.01 to 0.5<br/>mutationRate in 0.001 to 0.2<br/>explorationFactor in 0.1 to 0.9<br/><i>Cannot exceed bounds</i>"]

    style POP fill:#0a1a0a,stroke:#22c55e,color:#fff
    style FIT fill:#0d2a0d,stroke:#f59e0b,color:#fff
    style SELECT fill:#0d2a0d,stroke:#a855f7,color:#fff
    style MUTATE fill:#0d2a0d,stroke:#ef4444,color:#fff
    style NEW fill:#0a1a0a,stroke:#22c55e,color:#fff
    style BOUNDS fill:#7f1d1d,stroke:#ef4444,color:#fff
    style P1 fill:#166534,stroke:#4ade80,color:#dcfce7
    style P2 fill:#166534,stroke:#4ade80,color:#dcfce7
    style P3 fill:#166534,stroke:#4ade80,color:#dcfce7
    style P4 fill:#166534,stroke:#4ade80,color:#dcfce7
```

### 4. Real vs Simulation Mode

Two operating modes — simulation is the default, real mode requires explicit opt-in:

```mermaid
flowchart LR
    subgraph SIM["🎮 Simulation Mode — Default"]
        direction TB
        S1["🌐 Simulated Environment<br/><i>Programmed Stimuli</i>"]
        S2["📊 Synthetic Metrics<br/><i>Controlled Feedback</i>"]
        S3["🔄 Deterministic Bounds<br/><i>Reproducible Runs</i>"]
        S4["📈 Observable Evolution<br/><i>Safe Experimentation</i>"]
        S1 --> S2 --> S3 --> S4
    end

    subgraph REAL["🔬 Real Mode — Opt-In"]
        direction TB
        R1["🌍 Live Environment<br/><i>External Data Feeds</i>"]
        R2["📏 Actual Metrics<br/><i>Ground Truth Feedback</i>"]
        R3["🎲 Stochastic Bounds<br/><i>Non-Deterministic</i>"]
        R4["⚠️ Bounded Adaptation<br/><i>Still Constrained</i>"]
        R1 --> R2 --> R3 --> R4
    end

    subgraph COMMON["⚡ Shared Core"]
        CC1["Genome Bounds<br/><i>Enforced in Both Modes</i>"]
        CC2["Immune Cell<br/><i>Anomaly Detection</i>"]
        CC3["Observation Dashboard<br/><i>Real-Time Visualization</i>"]
        CC4["Evolution Logging<br/><i>Full History Export</i>"]
    end

    SIM --> COMMON
    REAL --> COMMON

    style SIM fill:#1e3a5f,stroke:#3b82f6,color:#fff
    style REAL fill:#7f1d1d,stroke:#ef4444,color:#fff
    style COMMON fill:#0d2a0d,stroke:#22c55e,color:#fff
    style S1 fill:#1e40af,stroke:#60a5fa,color:#dbeafe
    style S2 fill:#1e40af,stroke:#60a5fa,color:#dbeafe
    style S3 fill:#1e40af,stroke:#60a5fa,color:#dbeafe
    style S4 fill:#1e40af,stroke:#60a5fa,color:#dbeafe
    style R1 fill:#991b1b,stroke:#f87171,color:#fecaca
    style R2 fill:#991b1b,stroke:#f87171,color:#fecaca
    style R3 fill:#991b1b,stroke:#f87171,color:#fecaca
    style R4 fill:#991b1b,stroke:#f87171,color:#fecaca
    style CC1 fill:#166534,stroke:#4ade80,color:#dcfce7
    style CC2 fill:#166534,stroke:#4ade80,color:#dcfce7
    style CC3 fill:#166534,stroke:#4ade80,color:#dcfce7
    style CC4 fill:#166534,stroke:#4ade80,color:#dcfce7
```

### 5. Honest Limitations — What It Can and Cannot Do

Full transparency about the boundaries of this research project:

```mermaid
flowchart LR
    subgraph CAN["✅ What It CAN Do"]
        direction TB
        C1["🔧 Adjust operational<br/>parameters within bounds<br/><i>Bounded adaptation</i>"]
        C2["📊 Produce emergent patterns<br/>from simple rule interactions<br/><i>Non-intelligent emergence</i>"]
        C3["🔄 Run population-level<br/>evolution simulations<br/><i>Parameter optimization</i>"]
        C4["📈 Visualize adaptation<br/>in real-time<br/><i>Research observability</i>"]
        C5["💾 Log evolution history<br/>for offline analysis<br/><i>Full lineage tracking</i>"]
    end

    subgraph CANNOT["❌ What It CANNOT Do"]
        direction TB
        N1["🧠 General reasoning<br/>or understanding<br/><i>Not AGI</i>"]
        N2["💭 Feel, be aware,<br/>or have experiences<br/><i>Not Sentient</i>"]
        N3["🚀 Create entirely new<br/>capabilities or rewrite<br/>its own code<br/><i>Not Open-Ended</i>"]
        N4["🎯 Pursue goals or<br/>have intentions<br/><i>No Agency</i>"]
        N5["🧬 Evolve beyond<br/>pre-defined parameter<br/>bounds<br/><i>Bounded Only</i>"]
    end

    CAN ~~~ CANNOT

    style CAN fill:#14532d,stroke:#22c55e,color:#fff
    style CANNOT fill:#7f1d1d,stroke:#ef4444,color:#fff
    style C1 fill:#166534,stroke:#4ade80,color:#dcfce7
    style C2 fill:#166534,stroke:#4ade80,color:#dcfce7
    style C3 fill:#166534,stroke:#4ade80,color:#dcfce7
    style C4 fill:#166534,stroke:#4ade80,color:#dcfce7
    style C5 fill:#166534,stroke:#4ade80,color:#dcfce7
    style N1 fill:#991b1b,stroke:#f87171,color:#fecaca
    style N2 fill:#991b1b,stroke:#f87171,color:#fecaca
    style N3 fill:#991b1b,stroke:#f87171,color:#fecaca
    style N4 fill:#991b1b,stroke:#f87171,color:#fecaca
    style N5 fill:#991b1b,stroke:#f87171,color:#fecaca
```

> **Bottom line**: This is a research prototype for studying self-modifying systems. It adjusts parameters within bounds — it does not reason, feel, or evolve beyond its constraints. Biological terminology is metaphorical.

---

## Contributing

Contributions from researchers, students, and the curious are welcome:

1. Fork the repository
2. Create a research branch
3. Document your hypothesis and methodology
4. Submit a pull request with findings

Interesting contribution areas:
- New cell types and specializations
- More sophisticated environment models
- Better visualization and analysis tools
- Cross-organism communication protocols

## Disclaimer

This is an experimental research project for educational and academic exploration. The biological terminology used (organism, evolution, lifecycle) are metaphors for software patterns and do not imply biological properties. The project does not create sentient or conscious entities. The authors are not responsible for misinterpretation of the project's capabilities.

## License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

## Author

<div align="center">

**Mulky Malikul Dhaher**

[![GitHub](https://img.shields.io/badge/GitHub-mulkymalikuldhrs-181717?style=flat-square&logo=github)](https://github.com/mulkymalikuldhrs)
[![Email](https://img.shields.io/badge/Email-mulkymalikudhr@mail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:mulkymalikudhr@mail.com)

</div>

---

<!-- FOOTER BANNER -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0a1a0a,50:0d2a0d,100:103a10&fontColor=22c55e&descColor=a3e635&height=120&section=footer&text=&fontSize=0" />
