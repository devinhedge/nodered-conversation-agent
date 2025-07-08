# PlantUML & Mermaid Examples for HACS Integration

## Example HACS Manifest Structure (PlantUML)

```plantuml
@startuml
!theme plain
skinparam note {
  BackgroundColor #FFFACD
  BorderColor #DAA520
}

class "hacs.json" {
  {field} name: "Node-RED Conversation Agent"
  {field} content_in_root: false
  {field} filename: "nodered_conversation_agent"
  {field} hacs: "1.6.0"
  {field} homeassistant: "2023.1.0"
  {field} render_readme: true
  {field} domains: ["conversation"]
  {field} iot_class: "Local Push"
}

note right of "hacs.json"
  Required fields for HACS compatibility:
  - name: Display name in HACS
  - content_in_root: Location of integration
  - hacs/homeassistant: Version requirements
  - domains: Supported HA domains
end note

@enduml
```

## Component Manifest Updates (Mermaid)

```mermaid
graph LR
    subgraph "Original manifest.json"
        A[domain: conversation]
        B[name: Node-RED Conversation Agent]
        C[dependencies: requests]
        D[requirements: []]
    end
    
    subgraph "HACS-Ready manifest.json"
        E[domain: conversation]
        F[name: Node-RED Conversation Agent]
        G[dependencies: requests]
        H[requirements: []]
        I[version: 1.0.0]
        J[documentation: https://github.com/user/repo]
        K[issue_tracker: https://github.com/user/repo/issues]
        L[codeowners: @username]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
    
    style I fill:#90EE90
    style J fill:#90EE90
    style K fill:#90EE90
    style L fill:#90EE90
```

## HACS Validation Workflow (PlantUML)

```plantuml
@startuml
!theme plain
skinparam activity {
  BackgroundColor #E6F3FF
  BorderColor #4169E1
  FontColor #000080
}

title GitHub Actions Workflow for HACS Validation

|Repository|
start
:Developer pushes changes;
:Trigger GitHub Actions;

|HACS Validation|
:Download HACS Action;
:Check repository structure;
:Validate hacs.json format;
:Verify manifest.json content;

|Home Assistant Validation|
:Download Hassfest Action;
:Check Home Assistant compliance;
:Validate integration structure;
:Test manifest dependencies;

|Results|
if (All validations pass?) then (✅ Yes)
  :Set commit status to success;
  :Ready for HACS submission;
  stop
else (❌ No)
  :Set commit status to failure;
  :Display error details;
  :Developer fixes issues;
  stop
endif

@enduml
```

## Integration Installation Flow (Mermaid)

```mermaid
sequenceDiagram
    participant User as Home Assistant User
    participant HACS as HACS Interface
    participant GitHub as GitHub Repository
    participant HA as Home Assistant Core
    participant Component as Integration Code

    User->>HACS: Browse integrations
    HACS->>GitHub: Fetch repository list
    GitHub-->>HACS: Return available integrations
    HACS-->>User: Display integration catalog
    
    User->>HACS: Select Node-RED Conversation Agent
    HACS->>GitHub: Download integration files
    GitHub-->>HACS: Return integration archive
    HACS->>HA: Install to custom_components/
    HA->>HA: Restart Home Assistant
    
    User->>HA: Add integration via UI
    HA->>Component: Load integration
    Component->>Component: Initialize conversation platform
    Component-->>HA: Registration complete
    HA-->>User: Integration ready for use
    
    Note over User,Component: Integration now available for automations and voice commands
```

## File Dependencies Hierarchy (PlantUML)

```plantuml
@startuml
!theme plain
skinparam package {
  BackgroundColor #F0F8FF
  BorderColor #4682B4
}

package "Repository Root" {
  file "hacs.json" as hacs
  file "README.md" as readme
  file "info.md" as info
  
  package "custom_components/nodered_conversation_agent" {
    file "__init__.py" as init
    file "manifest.json" as manifest
    file "conversation.py" as conversation
    file "config_flow.py" as config
  }
  
  package ".github/workflows" {
    file "hacs.yml" as hacs_workflow
    file "hassfest.yml" as hassfest_workflow
  }
}

hacs --> manifest : references
manifest --> init : loads
init --> conversation : imports
init --> config : imports
hacs_workflow --> hacs : validates
hassfest_workflow --> manifest : validates
readme --> info : supplements

note right of hacs
  HACS entry point
  Defines integration metadata
end note

note right of manifest
  Home Assistant manifest
  Required for all integrations
end note

@enduml
```

## Testing Strategy Overview (Mermaid)

```mermaid
flowchart TD
    A[Start Testing] --> B[Add Custom Repository]
    B --> C[Install via HACS]
    C --> D{Installation Success?}
    D -->|No| E[Check Logs & Fix Issues]
    E --> B
    D -->|Yes| F[Configure Integration]
    F --> G[Test Basic Functionality]
    G --> H[Test Node-RED Communication]
    H --> I[Test Voice Commands]
    I --> J[Test Automation Integration]
    J --> K{All Tests Pass?}
    K -->|No| L[Debug & Fix Issues]
    L --> F
    K -->|Yes| M[Create GitHub Release]
    M --> N[Submit to HACS Default]
    
    style A fill:#e1f5fe
    style M fill:#c8e6c9
    style N fill:#c8e6c9
    style D fill:#fff3e0
    style K fill:#fff3e0
```

## Error Handling Flow (PlantUML)

```plantuml
@startuml
!theme plain
skinparam activity {
  BackgroundColor #FFE4E1
  BorderColor #DC143C
}

title Common HACS Validation Errors and Solutions

start
:HACS validation fails;

if (Missing hacs.json?) then (yes)
  :Create hacs.json with required fields;
  :Add name, content_in_root, domains;
  :Specify minimum versions;
elseif (Invalid manifest.json?) then (yes)
  :Add version field;
  :Add documentation URL;
  :Add issue_tracker URL;
  :Add codeowners list;
elseif (Incorrect file structure?) then (yes)
  :Move files to correct locations;
  :Ensure custom_components/{domain}/;
  :Check content_in_root setting;
elseif (Missing documentation?) then (yes)
  :Update README.md;
  :Add installation instructions;
  :Create info.md for HACS display;
else (other error)
  :Check HACS validation logs;
  :Review HACS documentation;
  :Seek community help;
endif

:Test changes;
:Rerun validation;

if (Validation passes?) then (yes)
  :Proceed with submission;
  stop
else (no)
  :Review error messages;
endif

@enduml
```

## Integration Architecture (Mermaid)

```mermaid
graph TB
    subgraph "Home Assistant Core"
        HA[Home Assistant]
        CM[Component Manager]
        ER[Entity Registry]
        AM[Automation Manager]
    end
    
    subgraph "HACS Integration"
        HACS[HACS Store]
        RM[Repository Manager]
        DM[Download Manager]
    end
    
    subgraph "Node-RED Conversation Agent"
        CP[Conversation Platform]
        NRC[Node-RED Client]
        IP[Intent Processor]
        CF[Config Flow]
    end
    
    subgraph "External Systems"
        NR[Node-RED Server]
        API[REST API]
        WS[WebSocket]
    end
    
    HACS --> RM
    RM --> DM
    DM --> HA
    HA --> CM
    CM --> CP
    CP --> ER
    ER --> AM
    
    CP --> NRC
    NRC --> API
    NRC --> WS
    API --> NR
    WS --> NR
    
    CF --> CP
    IP --> CP
    
    style HA fill:#4CAF50
    style HACS fill:#2196F3
    style CP fill:#FF9800
    style NR fill:#9C27B0
```

These diagrams provide a comprehensive visual guide for understanding and implementing HACS integration conversion using PlantUML and Mermaid syntax.