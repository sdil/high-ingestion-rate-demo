# High-ingestion-rate-demo

This demo is inspired by an article by Papercups.io on [how Genserver works based on Plausible source code](https://papercups.io/blog/genserver).

## Architecture Diagram

![Agnostic Architecture](agnostic-architecture.png)

![Elixir Architecture](elixir-architecture.png)

## Goals

### Non-Goals

## Types of Consumers

### Continuous Worker

Perform the operation on each message. The message will be blocked and performed sequentially.

### Batching Worker

Insert the data into a buffer queue, then at every interval perform a batch operation.

