# NEAT-ALGO FOR STOCK TRADING

## HA-NEAT

### Data Structures:

#### Node format:
Each networks nodes are stored in a node array with each node represented in the following manner

| Name          | Data type     |
| ------------- |:-------------:|
| nodeID        | int           |
| nodeType      | int           |
| nodeLayer     | int           |
| activationFunction | str      |
| sumInputs     | float         |
| sumOutputs    | float         |



#### Connections format:
{
    innovationID: int,
    inNodeID: int,
    outNodeID: int,
    weight: float,
    enabled: bool,
    isRecurrent: bool
}

#### Activation functions:
{
    LIN: Linear activation
    SIN: Sinusoidal activation
}

