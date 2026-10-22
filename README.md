# 🎯 AdaptiveCorpusScout (GenLayer Intelligent Contract)

![GenLayer](https://img.shields.io/badge/Network-GenLayer_Studio-blueviolet?style=for-the-badge)
![Smart Contract](https://img.shields.io/badge/Contract-Python_GenVM-blue?style=for-the-badge&logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Pytest-Passing-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

**AdaptiveCorpusScout** is an autonomous GenLayer Intelligent Contract that performs multi-stream semantic corpus scouting using a Laplace-smoothed Multi-Armed Bandit allocation strategy.

Instead of blindly evaluating every document in a large repository, the contract dynamically allocates limited AI evaluation budget toward data streams yielding the highest rate of semantic `MATCH` verdicts while maintaining exploration bonuses across under-sampled streams.

---

## ✨ Key Architectural Features

* **Laplace-Smoothed Bandit Allocation (`select_stream`):** Balances exploitation of high-signal document streams with exploration of unprobed streams using purely deterministic integer arithmetic.
* **Cryptographic Corpus Anchoring (`_fetch_corpus`):** Fetches pinned GitHub raw JSON datasets via `gl.nondet.web.get` and verifies the exact SHA-256 payload digest and per-record content hashes before executing LLM prompts.
* **Equivalence Principle Consensus:** Uses `gl.vm.run_nondet_unsafe` so both Leader and Validator nodes independently verify external dataset integrity and semantic classification (`MATCH`, `REJECT`, `UNCERTAIN`).
* **Immutable Audit Chain:** Every probe step generates a cryptographic `proof_hash` chained to the previous step's state hash (`latest_hash`).

---

## 📂 Dataset Schema Format

Datasets pinned on GitHub must conform to the following strict JSON structure (2 to 4 streams, 2 to 8 records per stream):

```json
{
  "streams": [
    {
      "id": "defi_research",
      "records": [
        {
          "id": "doc_01",
          "text": "Detailed passage text between 20 and 1000 characters..."
        },
        {
          "id": "doc_02",
          "text": "Second passage text evaluated against campaign objective..."
        }
      ]
    }
  ]
}
```

---

## 🚀 Contract Lifecycle & Methods

1. **`create_campaign`**: Register a scouting campaign with a semantic `objective`, pinned GitHub dataset coordinates (`gh_owner`, `gh_repo`, `commit_sha`, `file_path`, `expected_sha256`), `max_probes` budget, and `expires_at` deadline.
2. **`initialize_campaign(cid)`**: Fetches the remote corpus, validates the SHA-256 digest, builds the on-chain record catalog, and transitions status to `RUNNING`.
3. **`probe_next(cid, step_num)`**: Selects the optimal stream via the bandit policy, evaluates the next unprobed passage via GenVM LLM consensus, updates stream metrics, and logs an immutable audit record.
4. **`preview_next_probe(cid)` / `get_campaign(cid)` / `get_audit_log(cid, step_num)`**: View methods for inspecting campaign progress and cryptographic proofs.

---

## 🧪 Running Local Tests

```bash
pip install -r requirements.txt
pytest test_corpus_scout.py -v
```

---

<div align="center">
  <h3>Architected by Andrii (@dorinalunar)</h3>
  <p><i>Decentralized AI & GenLayer Intelligent Contract Engineering</i></p>
</div>
