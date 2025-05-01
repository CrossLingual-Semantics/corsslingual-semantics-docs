Usage Guide
===========

This document shows how to run the SWOW Enhancement Pipeline from the command line, describes each option, and gives a few worked examples.

Command-Line Invocation
------------------------

The main entry point is the `enhanceswow` (or `process`) command.  

.. code-block:: bash

   enhanceswow \
     --input <SWOW_CSV> \
     [--annotation_csv <ANNOTATION_CSV>] \
     [--output_json <CLEAN_JSON>] \
     [--output_json_with_metadata <META_JSON>] \
     [--sample_size <N>] \
     [--force] \
     [--start <I>] \
     [--end <J>] \
     [--languages <EN,ZH,…>] \
     [--language_code <en|zh|nl|…>]

Options
-------

.. list-table::
   :header-rows: 1

   * - Option
     - Description
   * - ``--input <SWOW_CSV>``
     - Path to the raw SWOW CSV file (required).
   * - ``--annotation_csv <ANNOTATION_CSV>``
     - Path to the SME annotation CSV (optional).
   * - ``--output_json <CLEAN_JSON>``
     - Where to save the filtered JSON output.
   * - ``--output_json_with_metadata <META_JSON>``
     - Where to save the JSON including class-metadata.
   * - ``--sample_size <N>``
     - Only enhance the top N cues (for quick testing).
   * - ``--force``
     - Ignore any existing cache and re-process from scratch.
   * - ``--start <I>`, ``--end <J>``
     - Slice the cue list by index before sampling.
   * - ``--languages <EN,ZH,…>``
     - BabelNet query languages (default: EN,ZH,NL,ES).
   * - ``--language_code <code>``
     - Subfolder for caching & SME lookup (default: “en”).

Cache Behavior
--------------

By default, intermediate results are cached


- **cue_dict.pkl**: aggregated cue→association frequencies  
- **annotation_dict.pkl**: SME annotations applied  

Use `--force` to bypass the cache and re-run all stages.

Examples
--------

1. **English – single cue “apple”**:

   .. code-block:: bash

      enhanceswow \
        --input /Cross_Lingual_2025/swow_data/SWOWEN.spellchecked.27-06-2022.csv \
        --annotation_csv /Cross_Lingual_2025/swow_data/coding.v7.COGSCI.en.csv \
        --output_json /Cross_Lingual_2025/enhanced_swow_data/apple.json \
        --output_json_with_metadata /Cross_Lingual_2025/enhanced_swow_data/apple_meta.json \
        --sample_size 1

2. **Mandarin – cues “苹果” & “宗教”**:

   .. code-block:: bash

      enhanceswow \
        --input /Cross_Lingual_2025/swow_data/SWOWZH.R55.20230424.csv \
        --annotation_csv /Cross_Lingual_2025/swow_data/coding.v7.COGSCI.zh_utf8.csv \
        --output_json /Cross_Lingual_2025/enhanced_swow_data/zh_sample.json \
        --output_json_with_metadata /Cross_Lingual_2025/enhanced_swow_data/zh_sample_meta.json \
        --sample_size 2 \
        --language_code zh

3. **Dutch – cues “appel” & “religie”**:

   .. code-block:: bash

      enhanceswow \
        --input /Cross_Lingual_2025/swow_data/SWOWNL.csv \
        --annotation_csv /Cross_Lingual_2025/swow_data/coding.v7.COGSCI.nl.csv \
        --output_json /Cross_Lingual_2025/enhanced_swow_data/nl_sample.json \
        --output_json_with_metadata /Cross_Lingual_2025/enhanced_swow_data/nl_sample_meta.json \
        --sample_size 2 \
        --language_code nl

Next: see `aggregator.rst` for how the raw SWOW CSV is ingested and converted into our `Cue`/`Association` data model.


