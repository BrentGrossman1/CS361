
# Multiplayer Chess Component Diagram

```mermaid
flowchart LR
  subgraph Client["Client (player's machine)"]
    UI[Game UI<br/>board, lobby, chat views]
    ClientNet[Client Networking]
  end

  subgraph Server["Server"]
    Gateway[Connection Gateway]
    Accounts[Accounts / Auth]
    Lobby[Lobby]
    Matchmaker[Matchmaking]
    Game[Game Session<br/>rules + move validation]
    Observers[Observer Broadcast]
    Chat[Chat]
    Stats[Statistics]
    DB[(Database)]
  end

  UI <-->|user actions / screen updates| ClientNet
  ClientNet <-->|network messages| Gateway
  Gateway -->|login| Accounts
  Gateway <-->|lobby events| Lobby
  Gateway <-->|moves / board state| Game
  Gateway <-->|chat messages| Chat
  Lobby -->|match requests| Matchmaker
  Matchmaker -->|reads skill ratings| Stats
  Matchmaker -->|starts game| Game
  Game -->|state updates| Observers
  Observers -->|board updates| Gateway
  Game -->|game results| Stats
  Accounts <-->|player records| DB
  Stats <-->|SQL| DB
```

**Assumptions**
- Players need accounts so stats and skill ratings persist between games.
- All client traffic goes through one gateway that routes it to the right component.
- The server owns game state and validates moves, so the client is just display and input.
