==============================
🌐 SWOW Enhancement Pipeline
==============================

Introduction
============

The **Small World of Words (SWOW) dataset** captures **word associations** through a **cue-response paradigm**. Each cue word elicits **three responses** (R1, R2, R3) from participants, revealing semantic relationships between words.

**Input CSV Example:**

.. list-table::
   :header-rows: 1

   * - cue
     - R1
     - R2
     - R3
   * - music
     - notes
     - band
     - rhythm
   * - book
     - pages
     - author
     - story

**Goal:** Enhance SWOW by adding **linguistic dimensions** to both cues and associations:

1. **POS:** Part of Speech (e.g., NOUN, VERB)
2. **Relations:** Lexical relations (e.g., synonym, hypernym)
3. **Sense:** BabelNet sense (ID and gloss description)

---

Core Classes
============

The enhancement pipeline relies on three core classes: **Dimension**, **Association**, and **Cue**.

1. **Dimension Class:** Represents metadata (POS, Relation, Sense).
2. **Association Class:** Represents words associated with cues.
3. **Cue Class:** Represents the main word with associations.

---

📏 **1. Dimension Class**
-------------------------

**File:** `swow_pipeline/models/dimension.py`

**Purpose:** Represents metadata associated with a word (POS, Relation, Sense).

**Key Code:**

.. code-block:: python

    class Dimension:
        """Base class for linguistic dimensions like POS, Relation, and Sense."""
        def __init__(self, name: str, value: str):
            self.name = name
            self.value = value

        def to_dict(self):
            return {"name": self.name, "value": self.value}


    class POS(Dimension):
        """Part-of-Speech Dimension."""
        def __init__(self, value: str):
            super().__init__("POS", value)


    class Relation(Dimension):
        """Lexical Relation Dimension."""
        def __init__(self, value: str):
            super().__init__("Relation", value)


    class Sense(Dimension):
        """Sense Mapping Dimension (BabelNet ID and gloss)."""
        def __init__(self, value: str):
            super().__init__("Sense", value)

**Example Output for "music":**

.. code-block:: json

    [
      { "name": "POS", "value": "NOUN" },
      { "name": "Relation", "value": "has_part" },
      { "name": "Sense", "value": "bn:00060282n: sound art form" }
    ]

---

🔗 **2. Association Class**
---------------------------

**File:** `swow_pipeline/models/association.py`

**Purpose:** Represents an **association** word linked to a cue, along with its **frequency** and **dimensions**.

**Key Code:**

.. code-block:: python

    from .dimension import Dimension

    class Association:
        """Association class representing word associations with dimensions."""
        def __init__(self, word: str, frequency: int):
            self.word = word
            self.frequency = frequency
            self.dimensions = []

        def add_dimension(self, dimension: Dimension):
            if dimension not in self.dimensions:
                self.dimensions.append(dimension)

        def to_dict(self):
            return {
                "word": self.word,
                "frequency": self.frequency,
                "dimensions": [dim.to_dict() for dim in self.dimensions]
            }

**Example Output for `"band"` (association of `"music"`):**

.. code-block:: json

    {
      "word": "band",
      "frequency": 7,
      "dimensions": [
        { "name": "POS", "value": "NOUN" },
        { "name": "Relation", "value": "member_of" },
        { "name": "Sense", "value": "bn:00010774n: musical group" }
      ]
    }

---

🎵 **3. Cue Class**
-------------------

**File:** `swow_pipeline/models/cue.py`

**Purpose:** Represents a **cue word**, its **associations**, and enriched **dimensions**.

**Key Code:**

.. code-block:: python

    from .association import Association
    from .dimension import Dimension

    class Cue:
        """Cue class representing a cue word with associations and dimensions."""
        def __init__(self, word: str):
            self.word = word
            self.associations = {}
            self.dimensions = []

        def add_association(self, word: str, frequency: int):
            if word not in self.associations:
                self.associations[word] = Association(word, frequency)

        def add_dimension(self, dimension: Dimension):
            if dimension not in self.dimensions:
                self.dimensions.append(dimension)

        def to_dict(self):
            return {
                "word": self.word,
                "associations": {word: assoc.to_dict() for word, assoc in self.associations.items()},
                "dimensions": [dim.to_dict() for dim in self.dimensions]
            }

**Example Output for Cue `"music"`:**

.. code-block:: json

    {
      "word": "music",
      "associations": {
        "notes": { "word": "notes", "frequency": 10, "dimensions": [...] },
        "band": { "word": "band", "frequency": 7, "dimensions": [...] }
      },
      "dimensions": [
        { "name": "POS", "value": "NOUN" },
        { "name": "Sense", "value": "bn:00060282n: sound art form" }
      ]
    }

---

Data Aggregation
================

**File:** `swow_pipeline/aggregator.py`

**Purpose:** Parses the input **SWOW CSV** into `Cue` and `Association` objects.

**Algorithm:**

1. Read the input CSV using `pandas`.
2. For each row:
   - Create a `Cue` object.
   - For `R1`, `R2`, `R3` responses:
     - Create `Association` objects with word and frequency.
3. Store each `Cue` and its `Associations` in a dictionary.

**Key Code:**

.. code-block:: python

    import pandas as pd
    from swow_pipeline.models.cue import Cue

    def aggregate_csv(input_path):
        df = pd.read_csv(input_path)
        cue_dict = {}

        for _, row in df.iterrows():
            cue_word = row['cue']
            if cue_word not in cue_dict:
                cue_dict[cue_word] = Cue(cue_word)

            for response in ['R1', 'R2', 'R3']:
                association = row[response]
                if pd.notnull(association):
                    cue_dict[cue_word].add_association(association, 1)

        return cue_dict

---

BabelNet Enhancement
====================

**File:** `swow_pipeline/enhancer.py`

**Purpose:** Enhances each **cue** and **association** with **POS**, **Relations**, and **Sense Mapping** using the BabelNet API.

**Algorithm:**

1. Query BabelNet for:
   - **POS:** Part of speech for the word.
   - **Relations:** Semantic connections (synonyms, hypernyms).
   - **Sense:** Synset ID and gloss.
2. Filter out duplicates.
3. Attach the enriched dimensions.

**Key Code:**

.. code-block:: python

    import babelnet as bn
    from babelnet.language import Language
    from swow_pipeline.models.dimension import POS, Relation, Sense

    def enhance_word(word: str):
        """Enhance word with POS, Relation, and Sense dimensions using BabelNet."""
        dimensions = []

        try:
            # 1. Part-of-Speech (POS)
            senses = bn.get_senses(word, from_langs=[Language.EN])
            if senses:
                dimensions.append(POS(senses[0].pos.name))

            # 2. Synset Relations (First Synset)
            synsets = bn.get_synsets(word, from_langs=[Language.EN])
            if synsets:
                for edge in synsets[0].outgoing_edges():
                    relation_name = edge.pointer.name
                    if relation_name not in [dim.value for dim in dimensions if isinstance(dim, Relation)]:
                        dimensions.append(Relation(relation_name))

            # 3. Sense Mapping
            for synset in synsets:
                gloss = synset.main_gloss(Language.EN).gloss if synset.main_gloss(Language.EN) else "No gloss"
                dimensions.append(Sense(f"{synset.id}: {gloss}"))

        except Exception as e:
            print(f"Error enhancing '{word}': {e}")

        return dimensions

---

Output Generation
=================

**File:** `swow_pipeline/output.py`

**Purpose:** Exports the enriched dataset as **JSON** and **JSON with Metadata**.

**Key Code:**

.. code-block:: python

    import json

    def export_to_json(cue_dict, output_path):
        """Export to clean JSON without metadata."""
        data = {cue: obj.to_dict() for cue, obj in cue_dict.items()}
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def export_to_json_with_metadata(cue_dict, output_path):
        """Export JSON with metadata."""
        def object_to_dict(obj):
            if hasattr(obj, '__dict__'):
                return {
                    "__class__": obj.__class__.__name__,
                    "__module__": obj.__module__,
                    **obj.__dict__
                }
            return obj

        data = {cue: object_to_dict(cue_obj) for cue, cue_obj in cue_dict.items()}
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

---

Pipeline Execution
==================

**File:** `main.py`

**Purpose:** Orchestrates the **aggregation**, **enhancement**, and **export** process.

**Algorithm:**

1. Aggregate `Cue` and `Association` objects.
2. Enhance with `POS`, `Relations`, and `Senses`.
3. Export to JSON.

**Key Code:**

.. code-block:: python

    import argparse
    from swow_pipeline.aggregator import aggregate_csv
    from swow_pipeline.enhancer import enhance_word
    from swow_pipeline.output import export_to_json, export_to_json_with_metadata
    import random

    def main(input_csv, output_json=None, output_json_with_metadata=None, sample_size=None):
        cue_dict = aggregate_csv(input_csv)

        # Sample if specified
        if sample_size:
            sample_cues = random.sample(list(cue_dict.values()), min(sample_size, len(cue_dict)))
        else:
            sample_cues = cue_dict.values()

        # Enhance sample cues and associations
        for cue in sample_cues:
            cue.dimensions.extend(enhance_word(cue.word))
            for assoc in cue.associations.values():
                assoc.dimensions.extend(enhance_word(assoc.word))

        # Export results
        if output_json:
            export_to_json(cue_dict, output_json)
        if output_json_with_metadata:
            export_to_json_with_metadata(cue_dict, output_json_with_metadata)

    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description="Enhance SWOW dataset with BabelNet dimensions.")
        parser.add_argument("--input", required=True, help="Path to the input CSV file")
        parser.add_argument("--output_json", required=False, help="Path to clean JSON output")
        parser.add_argument("--output_json_with_metadata", required=False, help="Path to metadata JSON output")
        parser.add_argument("--sample_size", type=int, required=False, help="Number of sample cues to enhance")

        args = parser.parse_args()
        main(args.input, args.output_json, args.output_json_with_metadata, args.sample_size)

---

Expected Output
===============

**Example Output for Cue `"music"`:**

.. code-block:: json

    {
      "word": "music",
      "associations": {
        "notes": { "word": "notes", "frequency": 10, "dimensions": [...] },
        "band": { "word": "band", "frequency": 7, "dimensions": [...] }
      },
      "dimensions": [
        { "name": "POS", "value": "NOUN" },
        { "name": "Relation", "value": "has_part" },
        { "name": "Sense", "value": "bn:00060282n: sound art form" }
      ]
    }

---

Running the Pipeline
====================

**Command:**

.. code-block:: bash

    python main.py --input data/swow_sample.csv --output_json output/clean_swow.json --output_json_with_metadata output/enhanced_swow.json --sample_size 100

---

🎯 **Outcome:**  
1. **Enhanced SWOW Dataset:** Cues and associations with POS, Relations, and Sense.  
2. **Cross-lingual Insights:** Understand how word associations vary across languages.  
3. **Interpretability:** Semantically aligned datasets for downstream NLP tasks.  
