====================
🌍 Overview
====================

Introduction
============

This project is part of the **CrossLingual Alignment Collaboration**, which explores **semantic equivalence across languages** using the **Small World of Words (SWOW)** dataset.

Unlike standard approaches that rely solely on multilingual embeddings from pretrained models, our work enhances **interpretable cross-lingual comparison** through **explicit word associations** and **linguistic annotations**.

---

✅ What Has Been Done So Far
============================

We have completed the **first major phase** of the project — enhancing the SWOW dataset with the following:

- **Cue–Association Aggregation:** Extracting and structuring cue→association mappings from raw CSV files.
- **BabelNet Augmentation:** Enriching words with:
  - Part-of-Speech (POS)
  - Lexical Relations
  - Sense mappings (BabelNet IDs & glosses)
- **SME Annotations:** Applying expert-labeled MacroCode and MicroCode dimensions.
- **Filtering:** Limiting associations per cue to the top 20 (preserving annotated items), and removing associations without dimensions.
- **Exporting JSON:** Final cue dictionaries saved in both clean and metadata-rich formats.

This enhanced dataset forms the basis for deeper **semantic alignment comparisons** between languages.

---

🚧 What We Are Doing Next
=========================

The **next phase** will focus on **comparing the enhanced outputs** for a given cue across multiple languages.

For example:
- Compare `"apple"` in English vs Chinese or Dutch
- Analyze which associations are shared, diverge, or align semantically
- Visualize these comparisons to uncover cultural and cognitive semantic shifts

We plan to develop a **Plotly-based interactive web application** for:
- Selecting a cue word
- Viewing its associated concepts across languages
- Highlighting dimension-level similarities and differences

Ultimately, this will help build interpretable, culturally aware semantic models — and form the foundation for academic dissemination.

---

🛠️ Technologies & Tools
========================

- **Datasets:** SWOW multilingual data
- **Lexical Resources:** BabelNet
- **Implementation:** Python
- **Documentation:** Sphinx
- **Planned Visualisation:** Plotly + university CMS (Squiz Matrix)
