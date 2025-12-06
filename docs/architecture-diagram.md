# Architecture diagram — Metrics Collection System

This Mermaid diagram visualizes the CALM architecture defined in `architectures/my-first-architecture.json`.

```mermaid
%% Mermaid flowchart showing actor, service (time-series DB), and blob storage
graph LR
  %% Nodes
  user_actor["End User\n(actor)"]
  metrics_store[("Metrics Store\n(database — time-series)")]
  metrics_blob_storage[("Metrics Blob Storage\n(object storage)")]
  metrics_service["Metrics Ingestion Service\n(service)"]
  metrics_system["Metrics Collection System\n(system)"]

  %% Relationships (labels show CALM relationship types)
  user_actor -->|interacts| metrics_store
  metrics_store -->|connects - archives - HTTPS| metrics_blob_storage
  metrics_system -->|composed-of| metrics_service
  metrics_system -->|composed-of| metrics_store

  %% Styling
  classDef actor fill:#fef3c7,stroke:#b45309,stroke-width:1px;
  classDef database fill:#bfdbfe,stroke:#1e3a8a,stroke-width:1px;
  classDef storage fill:#d1fae5,stroke:#065f46,stroke-width:1px;
  classDef service fill:#fee2e2,stroke:#9f1239,stroke-width:1px;
  classDef system fill:#eef2ff,stroke:#4338ca,stroke-width:1px;

  class user_actor actor;
  class metrics_store database;
  class metrics_blob_storage storage;
  class metrics_service service;
  class metrics_system system;

  %% Legend
  subgraph legend [Legend]
    L1["actor — user/customer"]
    L2["database — time-series store"]
    L3["object storage — blob archive"]
    L4["service — ingestion/processing component"]
    L5["system — top-level system boundary"]
  end
```

---

Notes:
- Node IDs in the CALM file: `metrics-store`, `metrics-blob-storage`, `end-user`.
- Relationships shown: `end-user-interacts-with-metrics-store` (interacts), `metrics-store-to-blob-storage` (connects).
 - Node IDs in the CALM file: `metrics-store`, `metrics-blob-storage`, `end-user`, `metrics-service`, `metrics-system`.
 - Relationships shown: `end-user-interacts-with-metrics-store` (interacts), `metrics-store-to-blob-storage` (connects), `metrics-system-composed-of` (composed-of).
- To render this diagram locally you can open this Markdown in editors that support Mermaid (VS Code with Mermaid Preview, GitHub README rendering, or Mermaid Live Editor).
