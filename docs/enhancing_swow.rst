🌐 Enhancing SWOW
=================

### 🔍 Why Enhance SWOW?

The **Small World of Words (SWOW) dataset** is a large-scale lexical association dataset used to understand **semantic alignment across languages**. However, it lacks:
- **Explicit linguistic relationships** (e.g., part of speech)
- **Context-aware cross-lingual mappings**

💡 **Our Solution:** We enhance SWOW with additional linguistic dimensions:

📌 **1️⃣ Parts of Speech (POS) Annotation**
   - Uses **BabelNet mappings** to categorize POS tags.
   - Helps filter **associations based on grammar**.

📌 **2️⃣ Lexical Relations**
   - Adds **synonyms, antonyms, hypernyms**.
   - Improves **context-aware word similarity computation**.

📌 **3️⃣ Sense Mapping**
   - Resolves **word ambiguities** by mapping SWOW responses to **BabelNet senses**.
   - Aligns **semantically equivalent words** across languages.

### 🛠️ Implementation Steps

📌 **1️⃣ Extracting Word Associations**
   - Filtering **top 10-15 associations** per cue word.
   - Grouping responses by **thematic categories**.

📌 **2️⃣ Integrating BabelNet Data**
   - Using BabelNet API to retrieve **POS, lexical relations, and senses**.
   - Annotating SWOW with **semantic metadata**.

📌 **3️⃣ Computing Cross-Lingual Similarity**
   - **Direct word association comparison**
   - **Embedding similarity using enriched SWOW**
   - Provides **a more interpretable alternative** to deep-learning-only approaches.

---

### 🎯 Expected Outcome
- ✅ A **multilingual SWOW dataset** with enhanced linguistic annotations.
- ✅ More **interpretable** cross-lingual word similarity.
- ✅ A **public repository** for further research and development.
