# HACS Integration Conversion Process

## Overview

This document provides PlantUML and Mermaid diagrams to illustrate the step-by-step process of converting a Home Assistant custom component into a HACS (Home Assistant Community Store) integration.

## 1. High-Level Conversion Workflow (Mermaid)

```mermaid
flowchart TD
    A[Start: Custom Component] --> B[Assess Current Structure]
    B --> C{Repository Public?}
    C -->|No| D[Make Repository Public]
    C -->|Yes| E[Check File Structure]
    D --> E
    E --> F[Create HACS Manifest]
    F --> G[Update Component Manifest]
    G --> H[Add Documentation]
    H --> I[Create Validation Workflows]
    I --> J[Test with HACS Custom Repository]
    J --> K{Validation Passes?}
    K -->|No| L[Fix Issues]
    L --> J
    K -->|Yes| M[Submit to HACS Default]
    M --> N[Community Review]
    N --> O{Approved?}
    O -->|No| P[Address Feedback]
    P --> N
    O -->|Yes| Q[✅ HACS Integration Complete]
    
    style A fill:#e1f5fe
    style Q fill:#c8e6c9
    style K fill:#fff3e0
    style O fill:#fff3e0
```

## 2. Repository Structure Transformation (PlantUML)

```plantuml
@startuml
!define FOLDER_COLOR #FFE4B5
!define FILE_COLOR #E6E6FA
!define NEW_COLOR #90EE90
!define MODIFIED_COLOR #FFB6C1

package "BEFORE: Basic Custom Component" {
  folder "custom_components" FOLDER_COLOR {
    folder "nodered_conversation_agent" FOLDER_COLOR {
      file "__init__.py" FILE_COLOR
      file "conversation.py" FILE_COLOR
      file "manifest.json" FILE_COLOR
    }
  }
  file "README.md" FILE_COLOR
}

package "AFTER: HACS-Ready Integration" {
  folder "custom_components" FOLDER_COLOR {
    folder "nodered_conversation_agent" FOLDER_COLOR {
      file "__init__.py" FILE_COLOR
      file "conversation.py" FILE_COLOR
      file "manifest.json" MODIFIED_COLOR
    }
  }
  file "README.md" MODIFIED_COLOR
  file "hacs.json" NEW_COLOR
  file "info.md" NEW_COLOR
  folder ".github" NEW_COLOR {
    folder "workflows" NEW_COLOR {
      file "hacs.yml" NEW_COLOR
      file "hassfest.yml" NEW_COLOR
    }
  }
}

legend
|Color|Meaning|
|NEW_COLOR|New Files|
|MODIFIED_COLOR|Modified Files|
|FILE_COLOR|Unchanged Files|
endlegend

@enduml
```

## 3. HACS Validation Sequence (Mermaid)

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Repo as GitHub Repository
    participant HACS as HACS Validation
    participant HA as Home Assistant
    participant Community as HACS Community

    Dev->>Repo: Push changes with HACS files
    Repo->>HACS: Trigger validation workflow
    HACS->>HACS: Check hacs.json format
    HACS->>HACS: Validate manifest.json
    HACS->>HACS: Check file structure
    HACS->>HA: Run Hassfest validation
    HA-->>HACS: Return validation results
    
    alt Validation Passes
        HACS->>Repo: ✅ Validation successful
        Repo->>Dev: Workflow passes
        Dev->>Community: Submit for HACS inclusion
        Community->>Community: Review integration
        Community-->>Dev: Approval/Feedback
    else Validation Fails
        HACS->>Repo: ❌ Validation failed
        Repo->>Dev: Workflow fails with errors
        Dev->>Dev: Fix issues
        Dev->>Repo: Push fixes
    end
```

## 4. HACS Integration Architecture (PlantUML)

```plantuml
@startuml
!theme plain
skinparam backgroundColor #FFFFFF
skinparam componentStyle rectangle

title HACS Integration Architecture

package "Home Assistant Core" {
  [Integration Manager] as IM
  [Entity Registry] as ER
  [Config Flow] as CF
}

package "HACS Integration" {
  [HACS Store] as HS
  [Repository Manager] as RM
  [Download Manager] as DM
  [Validation Engine] as VE
}

package "GitHub Repository" {
  [Integration Code] as IC
  [HACS Manifest] as HM
  [Component Manifest] as CM
  [Documentation] as DOC
}

package "Node-RED Conversation Agent" {
  [Conversation Platform] as CP
  [Node-RED Communication] as NRC
  [Intent Processing] as IP
}

HS --> RM : manages repositories
RM --> DM : downloads integrations
DM --> VE : validates downloads
VE --> IM : registers integration
IM --> CF : configuration flow
CF --> ER : entity registration

RM --> IC : fetches code
RM --> HM : reads metadata
RM --> CM : validates manifest
RM --> DOC : displays info

IC --> CP : implements platform
CP --> NRC : communicates with Node-RED
NRC --> IP : processes intents

@enduml
```

## 5. File Content Requirements (Mermaid)

```mermaid
graph TB
    subgraph "Required Files"
        A[hacs.json] --> A1[Domain specification]
        A --> A2[Name and description]
        A --> A3[Minimum HA version]
        
        B[manifest.json] --> B1[Version field]
        B --> B2[Documentation URL]
        B --> B3[Issue tracker URL]
        B --> B4[Codeowners list]
        
        C[README.md] --> C1[Installation instructions]
        C --> C2[Configuration examples]
        C --> C3[Feature descriptions]
        
        D[info.md] --> D1[HACS display content]
        D --> D2[Rich formatting]
        D --> D3[Screenshots/examples]
    end
    
    subgraph "Optional Files"
        E[.github/workflows/] --> E1[HACS validation]
        E --> E2[Hassfest validation]
        E --> E3[CI/CD automation]
        
        F[Brand assets] --> F1[Icon files]
        F --> F2[Logo files]
        F --> F3[128x128 PNG format]
    end
    
    style A fill:#ffcccb
    style B fill:#ffcccb
    style C fill:#ffcccb
    style D fill:#ffe4b5
    style E fill:#e6ffe6
    style F fill:#e6ffe6
```

## 6. Testing and Deployment Process (PlantUML)

```plantuml
@startuml
!theme plain
skinparam activityBackgroundColor #F0F8FF
skinparam activityBorderColor #4169E1
skinparam activityFontColor #000080

title HACS Integration Testing and Deployment

start
:Create HACS-compatible repository;
:Add custom repository to HACS;
:Test installation process;
:Verify integration loads correctly;
:Test configuration flow;
:Validate entity creation;
:Check automation compatibility;

if (All tests pass?) then (yes)
  :Create GitHub release;
  :Tag version in repository;
  :Submit to HACS default;
  
  if (Community review approved?) then (yes)
    :Integration added to HACS;
    :Users can install via HACS UI;
    stop
  else (no)
    :Address reviewer feedback;
    :Update repository;
  endif
else (no)
  :Debug and fix issues;
  :Update code/configuration;
endif

@enduml
```

## Key Benefits of Visual Documentation

1. **Clear Process Understanding**: Diagrams show the exact steps and decision points
2. **File Structure Clarity**: Before/after comparisons highlight required changes
3. **Workflow Validation**: Sequence diagrams show the validation and approval process
4. **Architecture Overview**: Component relationships and data flow visualization
5. **Testing Guidance**: Step-by-step testing and deployment procedures

These diagrams serve as a complete visual guide for converting any Home Assistant custom component into a HACS-compatible integration.
