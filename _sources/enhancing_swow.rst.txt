🌐 Enhancing SWOW
=================

Overview
--------

The **Small World of Words (SWOW) dataset** is a large-scale lexical association dataset used to understand **semantic alignment across languages**. However, it lacks:
- **Explicit linguistic relationships** (e.g., part of speech)
- **Context-aware cross-lingual mappings**

💡 **Our Solution:** We enhance SWOW with additional linguistic dimensions using the BabelNet API:

1. **Parts of Speech (POS) Annotation:** Categorizes word associations grammatically.
2. **Lexical Relations:** Identifies synonyms, antonyms, and hypernyms.
3. **Sense Mapping:** Resolves word ambiguities through BabelNet synsets.

---

🛠️ Implementation Steps
------------------------

1️⃣ **Extracting Word Associations**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step involves parsing the SWOW dataset into cues and associations.

**File:** `swow_pipeline/aggregator.py`

.. code-block:: python

    import pandas as pd
    from swow_pipeline.models.cue import Cue

    def aggregate_csv(input_path):
        """Aggregate SWOW CSV into Cue objects with associations."""
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

2️⃣ **Integrating BabelNet Data**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the BabelNet API, we enrich each cue and association with dimensions such as **POS**, **Relations**, and **Senses**.

**File:** `swow_pipeline/enhancer.py`

.. code-block:: python

    import babelnet as bn
    from babelnet.language import Language
    from swow_pipeline.models.dimension import POS, Relation, Sense

    def enhance_word(word: str):
        """Enhance word with POS, Relation, and Sense dimensions using BabelNet."""
        dimensions = []

        try:
            # Part-of-Speech (POS)
            senses = bn.get_senses(word, from_langs=[Language.EN])
            if senses:
                dimensions.append(POS(senses[0].pos.name))

            # Synset Relations
            synsets = bn.get_synsets(word, from_langs=[Language.EN])
            if synsets:
                for edge in synsets[0].outgoing_edges():
                    dimensions.append(Relation(edge.pointer.name))

            # Sense Mapping
            if synsets:
                for synset in synsets:
                    gloss = synset.main_gloss(Language.EN).gloss if synset.main_gloss(Language.EN) else "No gloss available"
                    dimensions.append(Sense(f"{synset.id}: {gloss}"))

        except Exception as e:
            print(f"Error enhancing '{word}': {e}")

        return dimensions

---

3️⃣ **Enriching Cues and Associations**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We enrich the cue word and its associations with dimensions during processing.

**File:** `swow_pipeline/models/cue.py`

.. code-block:: python

    from .association import Association
    from .dimension import Dimension

    class Cue:
        """Cue class representing a cue word with its associations and dimensions."""
        def __init__(self, word: str):
            self.word = word
            self.associations = {}
            self.dimensions = []

        def add_association(self, word: str, frequency: int):
            if word not in self.associations:
                self.associations[word] = Association(word, frequency)

        def add_dimension(self, dimension: Dimension):
            self.dimensions.append(dimension)

        def to_dict(self):
            return {
                "word": self.word,
                "associations": {word: assoc.to_dict() for word, assoc in self.associations.items()},
                "dimensions": [dim.to_dict() for dim in self.dimensions]
            }

---

📊 Example Output
-----------------

The following JSON output shows a cue word ("music") enriched with associations and metadata.

**Output JSON Example:**

.. code-block:: json

    {
      "word": "music",
      "associations": {
        "notes": {
          "word": "notes",
          "frequency": 10,
          "dimensions": [
            { "name": "POS", "value": "NOUN" },
            { "name": "Relation", "value": "has_part" },
            { "name": "Sense", "value": "bn:00079715n: musical notation" }
          ]
        },
        "band": {
          "word": "band",
          "frequency": 7,
          "dimensions": [
            { "name": "POS", "value": "NOUN" },
            { "name": "Relation", "value": "member_of" },
            { "name": "Sense", "value": "bn:00010774n: musical group" }
          ]
        }
      },
      "dimensions": [
        { "name": "POS", "value": "NOUN" },
        { "name": "Sense", "value": "bn:00060282n: sound art form" }
      ]
    }

---

✅ Expected Outcomes
-------------------

1. **Multilingual SWOW Dataset:** Enhanced with **POS**, **Relations**, and **Senses**.
2. **Semantic Alignment:** Improved understanding of word associations across languages.
3. **Public Repository:** Code and enriched dataset available for further research.

---

📄 Running the Pipeline
-----------------------

1. Ensure `babelnet_conf.yml` is configured with your BabelNet API key.

.. code-block:: yaml

    RESTFUL_KEY: 'your-api-key-here'
    RESTFUL_URL: 'https://babelnet.io/v9/service'

2. Run the SWOW enhancement pipeline:

.. code-block:: bash

    python main.py --input data/swow_sample.csv --output_json output/clean_swow.json --output_json_with_metadata output/enhanced_swow.json --sample_size 100

---

🧪 Testing the Pipeline
-----------------------

Tests are implemented using `pytest` to ensure BabelNet integration and output validity.

**File:** `tests/test_enhancer.py`

.. code-block:: python

    import pytest
    from swow_pipeline.models import Cue
    from swow_pipeline.enhancer import enhance_word

    def test_enhance_word():
        """Test enhancing word with BabelNet."""
        word = "music"
        dimensions = enhance_word(word)
        assert dimensions, "Enhancement failed."
        assert any(dim.name == "POS" for dim in dimensions)
        assert any(dim.name == "Relation" for dim in dimensions)
        assert any(dim.name == "Sense" for dim in dimensions)

Run tests with:

.. code-block:: bash

    pytest tests/

---

📚 Conclusion
-------------

The **Enhanced SWOW Pipeline** enriches word associations with interpretable linguistic dimensions. This approach provides:

- **Cross-lingual alignment** through BabelNet senses.
- **Semantic clarity** using POS and lexical relations.
- **Efficient, scalable enrichment** for multilingual word similarity studies.

---

🔗 **Next Steps**
-----------------

1. **Expand Language Support:** Extend enhancement to non-English SWOW datasets.
2. **Add More Dimensions:** Incorporate affective meanings and conceptual hierarchies.
3. **Visualization:** Create dashboards to explore enriched associations.

---

📥 **Repository:** [GitHub - Enhance SWOW](https://github.com/CrossLingual-Semantics/Enhance_SWOW)
