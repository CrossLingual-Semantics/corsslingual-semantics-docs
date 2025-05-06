Usage Guide
===========

This page shows how to run the SWOW enhancement pipeline (`enhanceswow`) in English, Mandarin (Chinese), and Dutch.  
It also demonstrates how to restrict processing to a fixed set of cue words via a simple YAML file.

Sample YAML file
----------------

Create a YAML file (e.g. `sampled_cues.yaml`) listing the exact cue words you wish to process. You can use either a YAML list:

.. code-block:: yaml

   # sampled_cues.yaml
   - apple
   - religion
   - culture

or a single comma-separated string:

.. code-block:: yaml

   # sampled_cues.yaml
   "apple, religion, culture"

When you supply `--sample-cues`, this file will override `--sample-size`.

General Command-Line Options
----------------------------

- ``--input``  
  Path to the raw SWOW CSV file for the chosen language.

- ``--annotation_csv``  
  Path to the SME annotation CSV (must contain columns ``cue.<lang>``, ``response.<lang>``).

- ``--output_json``  
  Path where the clean JSON output (no metadata) will be saved.

- ``--output_json_with_metadata``  
  Path where the full JSON (with class metadata) will be saved.

- ``--cache-dir``  
  Directory for cache subfolders (default: ``/Cross_Lingual_2025/cache``).

- ``--language_code``  
  Two-letter language code, which controls both cache subfolder and annotation column suffix  
  (e.g. ``en``, ``zh``, ``nl``). Default: ``en``.

- ``--sample-cues``  
  Path to a YAML file listing exact cues to process (overrides ``--sample-size``).

- ``--sample-size``  
  If you prefer random sampling, specify the number of cues to pick at random.

- ``--force``  
  Force reprocessing of both aggregation and annotation, even if cache exists.

- ``--start``, ``--end``  
  Slice the sorted cue list by index range (zero-based) before sampling.

Examples
--------

1. English Example
   ~~~~~~~~~~~~~~~~

   Process only “apple”, “religion” and “culture” in English:

   .. code-block:: bash

      enhanceswow \
        --input /Cross_Lingual_2025/swow_data/SWOWEN.spellchecked.27-06-2022.csv \
        --annotation_csv /Cross_Lingual_2025/swow_data/coding.v7.COGSCI.en.csv \
        --output_json /Cross_Lingual_2025/enhanced_swow_data/en_sample_en.json \
        --output_json_with_metadata /Cross_Lingual_2025/enhanced_swow_data/en_sample_en_meta.json \
        --cache-dir /Cross_Lingual_2025/cache \
        --language_code en \
        --sample-cues /Cross_Lingual_2025/sampled_cues.yaml

2. Mandarin (Chinese) Example
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Run the same cues in Mandarin:

   .. code-block:: bash

      enhanceswow \
        --input /Cross_Lingual_2025/swow_data/SWOWZH.R55.20230424.csv \
        --annotation_csv /Cross_Lingual_2025/swow_data/annotated-chinese-utf8.csv \
        --output_json /Cross_Lingual_2025/enhanced_swow_data/zh_sample_zh.json \
        --output_json_with_metadata /Cross_Lingual_2025/enhanced_swow_data/zh_sample_zh_meta.json \
        --cache-dir /Cross_Lingual_2025/cache \
        --language_code zh \
        --sample-cues /Cross_Lingual_2025/sampled_cues.yaml

3. Dutch Example
   ~~~~~~~~~~~~~~~

   And in Dutch:

   .. code-block:: bash

      enhanceswow \
        --input /Cross_Lingual_2025/swow_data/SWOWNL.csv \
        --annotation_csv /Cross_Lingual_2025/swow_data/coding.v7.COGSCI.nl.csv \
        --output_json /Cross_Lingual_2025/enhanced_swow_data/nl_sample_nl.json \
        --output_json_with_metadata /Cross_Lingual_2025/enhanced_swow_data/nl_sample_nl_meta.json \
        --cache-dir /Cross_Lingual_2025/cache \
        --language_code nl \
        --sample-cues /Cross_Lingual_2025/sampled_cues.yaml

Alternative: Random Sampling
----------------------------

If you do _not_ supply ``--sample-cues``, you can randomly select `N` cues instead:

.. code-block:: bash

   enhanceswow \
     --input /path/to/swow.csv \
     --annotation_csv /path/to/annotations.csv \
     --output_json /path/to/out.json \
     --output_json_with_metadata /path/to/out_meta.json \
     --language_code en \
     --sample-size 5

This will pick 5 random cue words each run.

Notes
-----

- The same cache directory is used for all languages; a subfolder named by ``<language_code>`` (e.g. `cache/en`, `cache/zh`, `cache/nl`) keeps each language’s data separate.  
- By fixing the cue list via YAML, you ensure that all languages process exactly the same set of words—ideal for cross-lingual comparison.  
- Using random sampling is a quick way to spot-check different cues without maintaining a YAML file.  
