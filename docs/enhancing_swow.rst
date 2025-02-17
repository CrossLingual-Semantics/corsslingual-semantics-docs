Enhancing SWOW
==============

### Why Enhance SWOW?

The **Small World of Words (SWOW) dataset** is a large-scale lexical association dataset collected through word association experiments in multiple languages. However, **raw SWOW data lacks explicit linguistic relationships**, making **cross-lingual alignment challenging**.

To address this, we **enhance SWOW with additional linguistic dimensions**:

1. **Parts of Speech (POS) Annotation**
   - Using **BabelNet mappings** to categorize each word's POS tag.
   - Helps in filtering associations based on grammatical constraints.

2. **Lexical Relations**
   - Defining **semantic relations** (e.g., synonymy, antonymy, hypernymy) between words.
   - Improves **context-aware word similarity computation**.

3. **Sense Mapping**
   - Resolving word ambiguities by mapping SWOW responses to **BabelNet senses**.
   - Helps align semantically equivalent words across languages.

### Implementation Approach

1. **Extracting Word Associations**
   - Filtering **top 10-15 associations** per cue word.
   - Grouping responses by **thematic dimensions (e.g., emotion, objects, verbs)**.

2. **Integrating BabelNet Data**
   - Using BabelNet’s API to retrieve **POS, lexical relations, and senses**.
   - Annotating SWOW associations with **semantic tags**.

3. **Computing Cross-Lingual Similarity**
   - Using a **hybrid approach**:  
     - **Direct word association comparison.**  
     - **Embedding similarity based on enriched SWOW data.**  
   - Provides **an interpretable alternative** to deep learning models.

### Expected Outcome

- **A multilingual SWOW dataset with linguistic annotations**.
- **Cross-lingual similarity computations** that are explainable.
- **A public repository hosting the enhanced dataset for future research**.

In the next section, we cover how to install and use this framework.
