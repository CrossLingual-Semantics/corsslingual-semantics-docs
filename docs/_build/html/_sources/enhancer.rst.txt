Enhancer Module — Detailed Walk-through
=======================================

This document explains in detail how each function in ``enhance_swow.enhancer`` works, what data it consumes and produces, and why certain design choices (TF-IDF ranking, CSV handling, SME annotation capping) were made.

.. contents::
   :local:
   :depth: 2

Overview
--------

The ``enhancer`` module performs three major tasks:

1. **Synset ranking & disambiguation**  
   Choose the most relevant BabelNet synsets for a cue or association using TF-IDF on glosses.

2. **Relation extraction**  
   Traverse outgoing edges of each chosen cue-synset to build:  
   - Per-synset maps (``synset_relation_map``, ``synset_edge_map``)  
   - Global maps (``Relation_Map``, ``Edge_Sense_Map``)

3. **SME annotation & association capping**  
   Load expert macro/micro-codes from CSV, apply them, and limit to 20 associations per cue, always keeping annotated ones.

---

TF-IDF Synset Ranking
---------------------

.. autofunction:: enhance_swow.enhancer.rank_synsets_by_gloss_similarity_tfidf

**How it works**:

1. **Collect glosses**  
   ::

     glosses = [
       s.main_gloss().gloss if s.main_gloss() else ""
       for s in synsets
     ]

2. **Build “context string”** from the cue word + its association list:  
   ::

     context_string = " ".join(context_words).lower()

3. **Fit a TF-IDF vectorizer** on all glosses + the context:  
   ::

     vectorizer = TfidfVectorizer().fit([context_string] + glosses)

4. **Compute cosine similarities** between the context vector and each gloss vector.

5. **Sort descending** by similarity score and return the top 5 synset objects.

**Why TF-IDF?**  
- Glosses vary in length and terminology; TF-IDF captures which gloss contains the most context-relevant keywords.  
- Faster and deterministic compared to LLM prompting.  
- Leverages association responses as disambiguating context.

---

Text & Translation Helpers
--------------------------

.. autofunction:: enhance_swow.enhancer.clean_sense_text

- **Purpose:** Normalize sense lemmas for JSON keys.  
- **Steps:**  
  1. Remove parenthetical qualifiers: ``"(subject)"``, ``"(general)"``  
  2. Convert underscores to spaces  
  3. Lowercase and trim

.. autofunction:: enhance_swow.enhancer.get_filtered_translations

- **Purpose:** Pull only those translations in our target languages (e.g. EN, ZH, NL, ES).  
- **Logic:**  
  1. BabelNet returns keys like ``"WIKI:ZH:Some_Title"`` → split on ``":"``  
  2. Keep only those matching our ``target_langs``  
  3. Return a dict, e.g.:  

  .. code-block:: json

     { "ZH": ["丈夫", "大丈夫"], "EN": ["husband"] }

---

Main Enhancer Function
-----------------------

.. autofunction:: enhance_swow.enhancer.enhance_cue_with_relations

**Inputs**:

- **cue_word**: e.g. ``"apple"``  
- **associations**: a list of strings, e.g. ``["fruit","red","juice"]``  
- **cue_dict**: original ``Cue`` object  
- **languages**: list of ``babelnet.language.Language`` enums  

**Output**: a nested dict:

.. code-block:: json

   {
     "cue_word": {
       "word": "...",
       "Synsets": [ { id, gloss, pos, …, synset_relation_map, synset_edge_map }, … ],
       "Relation_Map": { "targetID|||lemma": "RelationType", … },
       "Edge_Sense_Map": { "RelationType": [ "targetID|||lemma", … ] }
     },
     "associations": {
       "fruit": {
         "Synsets": [ { id, gloss, pos, …, cue_synset_links }, … ]
       },
       …
     }
   }

**Step-by-step**:

1. Fetch all BabelNet synsets for the cue (`bn.get_synsets`).
2. Rank & select top 5 via TF-IDF (`rank_synsets_by_gloss_similarity_tfidf`).
3. Initialize empty global maps.
4. **For each selected cue synset**:  
   - Extract POS, main gloss, translations.  
   - Filter outgoing edges by language.  
   - For each edge → target synset → its senses:  
     - Build a **sense_key**: ``"synsetID|||cleanedLemma"``  
     - Populate local & global relation maps.  
   - Append per-synset dict to ``result["cue_word"]["Synsets"]``.
5. Assign global maps into ``result["cue_word"]``.
6. **Process up to 20 associations**:  
   - TF-IDF rank each association’s synsets in its own context.  
   - For each assoc synset, build metadata and trace back any matching cue synset via its ``synset_relation_map``.  
   - Record links in ``cue_synset_links``.  
   - Add to ``result["associations"]`` if any synsets selected.

---

CSV & SME Annotation
---------------------

.. autofunction:: enhance_swow.enhancer.safe_read_csv

- Tries multiple encodings: ``utf-8``, ``utf-8-sig``, ``gb18030``, ``utf-16``, ``ISO-8859-1``.

.. autofunction:: enhance_swow.enhancer.add_sme_annotations

1. Read CSV into DataFrame.  
2. Normalize “cue.<lang>” and “response.<lang>” columns.  
3. Build a lookup:  
   ``{ (cue, response) → { macroCode, microCode } }``  
4. Apply codes to matching associations.  
5. For each cue, select up to 20 associations:  
   - Include all annotated first, then highest-frequency others.

---

BabelNet Synset Background
---------------------------

Our code uses these Synset primitives:

- **ID** (`synset.id`), **POS** (`synset.pos`)  
- **Gloss** (`synset.main_gloss()`) and list of glosses  
- **Senses** (`synset.senses(language)`) with lemma, source, etc.  
- **Outgoing edges** (`synset.outgoing_edges()`) for graph navigation  
- **Translations** (`synset.translations`)  

We combine them to produce:

- Disambiguated, TF-IDF-ranked synsets  
- Detailed relation maps (per-synset & global)  
- Multilingual coverage for cultural analysis

---

With this detailed breakdown, collaborators can:

- Reproduce or tweak each step  
- Extend to new languages or ranking strategies  
- Understand how cue–association context drives disambiguation  
