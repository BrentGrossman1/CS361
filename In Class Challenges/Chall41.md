````text
``` mermaid
flowchart LR
    A([Web Server]) -->|HTML| B[Web Front End]
    B <--> C[API]
    D[User Applications] <--> C
    C <--> E[(GIS Database)]
```

``` mermaid
flowchart LR
    A[User Applications]
    B[API]
    E[Web Front End]

    subgraph backend [Back End]
        C[(GIS database)]
        D([Web Server])
    end

    A <-->|API calls| B
    B <-->|API calls| E
    B <-->|GIS info| C
    D -->|HTML| E

    style backend fill:#fdf2fd,stroke:#f0a0f0
```
````