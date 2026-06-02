# Neo4j GraphRAG Compliance Copilot

A hybrid GraphRAG-based compliance intelligence system that combines Knowledge Graphs, Vector Search, and Large Language Models to deliver explainable, citation-backed regulatory reasoning across enterprise compliance artifacts.

---

## Overview

This project implements an end-to-end Retrieval-Augmented Generation (RAG) pipeline for enterprise compliance workflows. The system leverages a Neo4j Knowledge Graph for relationship-aware retrieval and FAISS vector search for semantic retrieval, enabling grounded responses supported by regulatory evidence, internal policies, and procedural documentation.

Unlike traditional vector-only RAG systems, this solution incorporates graph traversal and multi-hop reasoning to establish traceable links between regulations, policies, procedures, and compliance controls.

---

## Architecture

```text
Compliance Documents
        │
        ▼
Document Processing & Chunking
        │
        ▼
Embedding Generation
        │
        ▼
FAISS Vector Index

Compliance Documents
        │
        ▼
Knowledge Graph Construction
        │
        ▼
Neo4j Graph Database

────────────────────────────────────

User Query
        │
        ▼
Hybrid Retrieval Layer
 ┌──────────────┬──────────────┐
 │              │              │
 ▼              ▼              ▼
Neo4j      Graph Traversal   FAISS
Entities   & Multi-Hop       Search
            Retrieval
 └──────────────┬──────────────┘
                ▼
          Context Fusion
                ▼
       Prompt Construction
                ▼
          OpenAI GPT
                ▼
      Compliance Response
                ▼
     Reasoning Paths + Citations
```

---

## Core Implementations

### Knowledge Graph Layer

Implemented a Neo4j property graph representing compliance knowledge across:

* Regulatory Articles
* Policies
* Procedures
* Controls
* Risks
* Business Functions

Relationships are modeled using Cypher-based graph structures to support multi-hop reasoning and policy traceability.

#### Example Graph Relationships

```cypher
(:Policy)-[:IMPLEMENTS]->(:Regulation)

(:Procedure)-[:SUPPORTS]->(:Policy)

(:Control)-[:ENFORCES]->(:Requirement)

(:Department)-[:OWNS]->(:Procedure)

(:Risk)-[:MITIGATED_BY]->(:Control)
```

---

### Vector Retrieval Layer

Implemented semantic retrieval using FAISS.

#### Capabilities

* Document Chunking
* Embedding Generation
* Dense Vector Indexing
* Similarity Search
* Top-K Retrieval
* Context Expansion

The vector retrieval layer enables semantic matching of compliance content even when explicit graph relationships are unavailable.

---

### Hybrid GraphRAG Pipeline

Built a dual retrieval architecture combining symbolic graph reasoning with semantic vector search.

#### Graph Retrieval

* Entity Extraction
* Cypher-Based Graph Traversal
* Relationship Discovery
* Multi-Hop Reasoning

#### Vector Retrieval

* Dense Embedding Search
* Similarity Matching
* Context Expansion
* Evidence Retrieval

#### Context Fusion

* Retrieval Result Aggregation
* Duplicate Elimination
* Evidence Ranking
* Unified Context Generation

This architecture improves answer grounding and reduces hallucination compared to traditional vector-only RAG implementations.

---

### Retrieval-Augmented Generation (RAG)

Implemented a retrieval-constrained generation workflow:

1. User Query Processing
2. Entity Identification
3. Graph-Based Retrieval
4. Semantic Retrieval
5. Context Fusion
6. Prompt Construction
7. OpenAI Response Generation

---

### Prompt Engineering & Reasoning

Designed structured prompts to enforce:

* Context Grounding
* Regulatory Reasoning
* Evidence Attribution
* Citation Generation
* Response Consistency

Generated outputs include:

* Direct Answers
* Compliance Explanations
* Reasoning Paths
* Source Citations

---

### Explainability Framework

To improve transparency and auditability, the system generates graph-derived reasoning chains that expose how conclusions are reached.

#### Example Reasoning Path

```text
GDPR Article 17
      ↓
Customer Privacy Policy
      ↓
Data Deletion Procedure
```

#### Explainability Components

* Graph Traceability
* Source Attribution
* Evidence Grounding
* Relationship-Based Reasoning
* Citation-Backed Responses

---

### Frontend Layer

Developed an interactive compliance intelligence interface using Streamlit.

#### Features

* Compliance Question Answering
* Real-Time Response Generation
* Reasoning Path Visualization
* Citation Display
* Compliance Explanation Generation

---

### Containerization & Deployment

Containerized the application using Docker for reproducible deployment and environment isolation.

#### Deployment Components

* Docker
* Environment Variable Configuration
* OpenAI API Integration
* Neo4j Connectivity
* Streamlit Deployment

---

## Technology Stack

### Backend & Application Layer

* Python 3.11
* Streamlit

### Knowledge Graph Layer

* Neo4j
* Cypher Query Language

### Retrieval Layer

* FAISS
* OpenAI Embeddings
* Hybrid GraphRAG

### LLM Layer

* OpenAI GPT Models
* Retrieval-Augmented Generation (RAG)

### Infrastructure

* Docker
* Virtual Environments
* Environment Variable Management

---

## AI/ML Concepts Implemented

* GraphRAG
* Retrieval-Augmented Generation (RAG)
* Knowledge Graphs
* Semantic Search
* Dense Vector Embeddings
* Similarity Search
* Multi-Hop Reasoning
* Context Fusion
* Explainable AI (XAI)
* Evidence Grounding
* Regulatory Intelligence Systems
* Hybrid Retrieval Architectures

---

## End-to-End Workflow

```text
Enterprise Policies & Regulations
                │
                ▼
      Document Processing
                │
                ▼
      Knowledge Graph Creation
                │
                ▼
         Neo4j Graph Store

Enterprise Policies & Regulations
                │
                ▼
      Embedding Generation
                │
                ▼
         FAISS Index

────────────────────────────────────

            User Query
                │
                ▼
      Graph-Based Retrieval
                │
                ▼
      Semantic Retrieval
                │
                ▼
          Context Fusion
                │
                ▼
       Prompt Construction
                │
                ▼
          OpenAI GPT
                │
                ▼
      Compliance Response
                │
                ▼
    Reasoning Paths & Citations
```

---

## Key Outcomes

* Implemented a hybrid GraphRAG architecture for enterprise compliance intelligence.
* Enabled policy-to-regulation traceability through knowledge graph traversal.
* Combined symbolic reasoning with semantic retrieval for enhanced answer grounding.
* Delivered explainable, citation-backed compliance responses.
* Reduced hallucination risk through retrieval-constrained LLM generation.
* Demonstrated multi-hop reasoning across interconnected compliance artifacts.
