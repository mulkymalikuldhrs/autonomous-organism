<img src="docs/banner.png" width="100%">

<a href="https://github.com/mulkymalikuldhrs/autonomous-organism">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0a1a0a,50:0d2a0d,100:103a10&fontColor=22c55e&descColor=a3e635&height=220&section=header&text=Autonomous%20Organism&fontSize=55&desc=Self-Evolving%20Digital%20Entity&animation=fadeIn" />
</a>

<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=22C55E&center=true&vCenter=true&width=600&lines=Parameter+Self-Adjustment+System;Digital+Evolution+Simulation;Experimental+Research+Project;Not+AGI+Not+Sentient+Bounded+Evolution)](https://git.io/typing-svg)

<br/>

[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://react.dev)
[![Node.js](https://img.shields.io/badge/Node.js-20+-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Backend-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Research](https://img.shields.io/badge/Type-Research-22C55E?style=for-the-badge)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

</div>

---

## Overview

**Autonomous Organism** is an experimental research project exploring the concept of a self-evolving digital entity. Built in TypeScript with React/Supabase, it implements a system where a software "organism" can adjust its own operational parameters — behavior patterns, response strategies, resource allocation — within defined bounds, simulating a form of digital adaptation and evolution.

This is a research artifact, not a product. It investigates questions about self-modifying systems, emergent behavior from simple rules, and the boundaries between programmed adaptation and genuine autonomy.

> **Honest Note**: "Self-evolving" here means **parameter adjustment within pre-defined bounds**. The organism can tweak its own settings — it cannot rewrite its fundamental code or create entirely new capabilities. This is bounded, constrained adaptation, not open-ended evolution. It is **not AGI**, **not sentient**, and has no awareness, feelings, or general reasoning capability.

---

## Visual Architecture

### 1. Organism Lifecycle — From Sensing to Acting

The digital organism follows a biological metaphor from sensing the environment to producing a response:

```mermaid
flowchart LR
    subgraph ENV["Environment"]
        STIM["Stimuli and Events<br/>Resource Signals<br/>Ecosystem Interactions"]
    end

    subgraph SENSE["Sense Cell"]
        S1["Perceive Stimuli"]
        S2["Filter Noise"]
        S3["Classify Input"]
        S1 --> S2 --> S3
    end

    subgraph DECISION["Decision Cell"]
        D1["Evaluate Options"]
        D2["Select Strategy"]
        D3["Allocate Resources"]
        D1 --> D2 --> D3
    end

    subgraph MEMORY["Memory Cell"]
        M1["Store Experience"]
        M2["Recall Patterns"]
        M3["Update Weights"]
        M1 --> M2 --> M3
    end

    subgraph FACTORY["Factory Cell"]
        F1["Execute Strategy"]
        F2["Generate Response"]
        F3["Apply Mutations"]
        F1 --> F2 --> F3
    end

    subgraph IMMUNE["Immune Cell"]
        I1["Detect Anomalies"]
        I2["Quarantine Defects"]
        I3["Repair State"]
        I1 --> I2 --> I3
    end

    subgraph SCHED["Scheduler Cell"]
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
    SCHED -->|"Next Cycle"| SENSE
    MEMORY -.->|"Historical Context"| DECISION

    style ENV fill:#0a1a0a,stroke:#22c55e,color:#fff
    style SENSE fill:#103a10,stroke:#a3e635,color:#fff
    style DECISION fill:#103a10,stroke:#22c55e,color:#fff
    style MEMORY fill:#103a10,stroke:#3b82f6,color:#fff
    style FACTORY fill:#103a10,stroke:#f59e0b,color:#fff
    style IMMUNE fill:#103a10,stroke:#ef4444,color:#fff
    style SCHED fill:#103a10,stroke:#8b5cf6,color:#fff
```

### 2. Cell System Architecture — Six Specialized Modules

Six specialized cell modules interact like biological cells — each with a defined role, communicating through inter-cell protocols:

```mermaid
flowchart TB
    subgraph ORGANISM["Digital Organism"]
        direction TB

        subgraph CELLS["Cell Modules"]
            SENSE["Sense Cell<br/>Perception Layer<br/>Stimulus Detection<br/>Input Classification<br/>Noise Filtering"]
            DECIDE["Decision Cell<br/>Cognitive Layer<br/>Strategy Selection<br/>Resource Allocation<br/>Option Evaluation"]
            MEM["Memory Cell<br/>Storage Layer<br/>Experience Storage<br/>Pattern Recall<br/>Weight Updates"]
            FACT["Factory Cell<br/>Execution Layer<br/>Strategy Execution<br/>Response Generation<br/>Mutation Application"]
            IMMUNE["Immune Cell<br/>Protection Layer<br/>Anomaly Detection<br/>Defect Quarantine<br/>State Repair"]
            SCHED["Scheduler Cell<br/>Timing Layer<br/>Task Queuing<br/>Action Prioritization<br/>Lifecycle Clock"]
        end

        subgraph COMMS["Inter-Cell Communication"]
            BUS["Message Bus<br/>Structured Protocols<br/>Event-Driven Architecture"]
        end
    end

    subgraph GENOME["Genome — Parameter Configuration"]
        GEN["adaptationRate: 0.01 - 0.5<br/>mutationRate: 0.001 - 0.2<br/>explorationFactor: 0.1 - 0.9<br/>All mutations bounded"]
    end

    SENSE --> BUS
    DECIDE --> BUS
    MEM --> BUS
    FACT --> BUS
    IMMUNE --> BUS
    SCHED --> BUS
    BUS --> GENOME

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

### 3. Evolution Mechanics — Fitness-Based Selection with Bounded Mutation

The organism adapts within defined constraints through a fitness-based selection loop:

```mermaid
flowchart TD
    subgraph POP["Population"]
        P1["Organism A<br/>params: a=0.12, m=0.04"]
        P2["Organism B<br/>params: a=0.08, m=0.07"]
        P3["Organism C<br/>params: a=0.25, m=0.02"]
        P4["Organism D<br/>params: a=0.15, m=0.09"]
    end

    subgraph FIT["Fitness Evaluation"]
        F1["Environmental<br/>Feedback Score"]
        F2["Resource Efficiency<br/>Measurement"]
        F3["Survival Metrics<br/>Assessment"]
        F1 --> F2 --> F3
    end

    subgraph SELECT["Selection"]
        S1["Rank by Fitness"]
        S2["Tournament / Roulette<br/>Selection"]
        S3["Niching and Speciation<br/>Diversity Maintenance"]
        S1 --> S2 --> S3
    end

    subgraph MUTATE["Mutation — Bounded"]
        M1["Parameter Tweak<br/>Within Pre-Defined Bounds"]
        M2["Crossover<br/>Blend Two Organisms"]
        M3["Diversity Check<br/>Convergence Monitor"]
        M1 --> M2 --> M3
    end

    subgraph NEW["New Generation"]
        N1["Offspring Organisms<br/>Bounded Parameters Only"]
        N2["Insert into Population"]
        N3["Repeat Evolution Cycle"]
        N1 --> N2 --> N3
    end

    POP --> FIT --> SELECT --> MUTATE --> NEW
    NEW -->|"Next Generation"| POP

    M1 -.->|"Bounds Enforced"| BOUNDS["adaptationRate in 0.01 to 0.5<br/>mutationRate in 0.001 to 0.2<br/>explorationFactor in 0.1 to 0.9<br/>Cannot exceed bounds"]

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

### 4. Real vs Simulation Mode — Two Operating Modes

Simulation is the default; real mode requires explicit opt-in. Both modes share the same bounded core:

```mermaid
flowchart LR
    subgraph SIM["Simulation Mode — Default"]
        direction TB
        S1["Simulated Environment<br/>Programmed Stimuli"]
        S2["Synthetic Metrics<br/>Controlled Feedback"]
        S3["Deterministic Bounds<br/>Reproducible Runs"]
        S4["Observable Evolution<br/>Safe Experimentation"]
        S1 --> S2 --> S3 --> S4
    end

    subgraph REAL["Real Mode — Opt-In"]
        direction TB
        R1["Live Environment<br/>External Data Feeds"]
        R2["Actual Metrics<br/>Ground Truth Feedback"]
        R3["Stochastic Bounds<br/>Non-Deterministic"]
        R4["Bounded Adaptation<br/>Still Constrained"]
        R1 --> R2 --> R3 --> R4
    end

    subgraph COMMON["Shared Core"]
        CC1["Genome Bounds<br/>Enforced in Both Modes"]
        CC2["Immune Cell<br/>Anomaly Detection"]
        CC3["Observation Dashboard<br/>Real-Time Visualization"]
        CC4["Evolution Logging<br/>Full History Export"]
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
    subgraph CAN["What It CAN Do"]
        direction TB
        C1["Adjust operational<br/>parameters within bounds<br/>Bounded adaptation"]
        C2["Produce emergent patterns<br/>from simple rule interactions<br/>Non-intelligent emergence"]
        C3["Run population-level<br/>evolution simulations<br/>Parameter optimization"]
        C4["Visualize adaptation<br/>in real-time<br/>Research observability"]
        C5["Log evolution history<br/>for offline analysis<br/>Full lineage tracking"]
    end

    subgraph CANNOT["What It CANNOT Do"]
        direction TB
        N1["General reasoning<br/>or understanding<br/>Not AGI"]
        N2["Feel, be aware,<br/>or have experiences<br/>Not Sentient"]
        N3["Create entirely new<br/>capabilities or rewrite<br/>its own code<br/>Not Open-Ended"]
        N4["Pursue goals or<br/>have intentions<br/>No Agency"]
        N5["Evolve beyond<br/>pre-defined parameter<br/>bounds<br/>Bounded Only"]
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

---

## Quick Start

### Prerequisites
- Node.js 18+
- TypeScript 5.x
- Supabase account (for persistence layer)

### Installation

```bash
git clone https://github.com/mulkymalikuldhrs/autonomous-organism.git
cd autonomous-organism
npm install
```

### Running

```bash
# Start with default configuration
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

---

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

---

## Honest Notes

> **Clearing up misconceptions:**

- **Experimental Research Project** — This is a research prototype for studying self-modifying systems. It is not a product, service, or tool for general use.
- **"Self-Evolving" is Limited** — The self-evolution in this project refers to **parameter adjustment within pre-defined bounds**. The organism can tweak its own settings, not rewrite its fundamental code or create entirely new capabilities. This is bounded, constrained adaptation — not open-ended evolution.
- **Not AGI** — This project does not implement artificial general intelligence. The "organism" follows programmed rules with adjustable parameters. There is no understanding, consciousness, or general reasoning capability.
- **Not Sentient** — Despite the biological metaphor, the digital organism has no awareness, feelings, or subjective experience. Terms like "organism," "evolution," and "lifecycle" are metaphors for software patterns.
- **Emergent Behavior is Simple** — While the system can produce interesting emergent patterns, these emerge from the interaction of simple rules, not from any form of intelligence or intentionality.

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

---

## Disclaimer

This is an experimental research project for educational and academic exploration. The biological terminology used (organism, evolution, lifecycle) are metaphors for software patterns and do not imply biological properties. The project does not create sentient or conscious entities. The authors are not responsible for misinterpretation of the project's capabilities.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

## Author

<div align="center">

**Mulky Malikul Dhaher**

[![GitHub](https://img.shields.io/badge/GitHub-mulkymalikuldhrs-181717?style=for-the-badge&logo=github)](https://github.com/mulkymalikuldhrs)
[![Email](https://img.shields.io/badge/Email-mulkymalikudhr@mail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mulkymalikudhr@mail.com)

</div>

---

<a href="https://github.com/mulkymalikuldhrs/autonomous-organism">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0a1a0a,50:0d2a0d,100:103a10&fontColor=22c55e&descColor=a3e635&height=120&section=footer&text=&fontSize=0" />
</a>
