Annotation Module
=================

Overview
--------

The **annotation** step integrates expert (SME)‐provided MacroCode and MicroCode labels
into each cue’s associations and limits the number of associations per cue to a
fixed maximum (default: 20), always preserving any that have SME labels.

Key Functions
-------------

.. function:: safe_read_csv(path: str) → pandas.DataFrame

   Read a CSV file whose text encoding may vary (e.g., Mandarin CSVs). Tries multiple
   encodings (`utf-8`, `utf-8-sig`, `gb18030`, `utf-16`, `ISO-8859-1`) in turn, and
   returns a DataFrame if successful.

   **Parameters**  
   - `path`: filesystem path to the CSV file.

   **Returns**  
   A `pandas.DataFrame` loaded with the file’s contents.

   **Raises**  
   - `ValueError` if no encoding succeeds.

.. function:: add_sme_annotations(cue_dict: dict[str, Cue], annotation_csv: str, language_code: str) → dict[str, Cue]

   Augment each `Cue`’s `.associations` with SME annotations (MacroCode & MicroCode),
   then prune to at most 20 associations per cue, always including those with SME labels.

   **Parameters**  
   - `cue_dict`: mapping `cue_word → Cue` from the aggregator step.  
   - `annotation_csv`: path to the SME annotation CSV.  
   - `language_code`: e.g. `"en"`, `"zh"`, indicating which columns to read (`cue.en`, `response.en`).

   **Process**  
   1. **Load CSV** .  
   2. **Clean & Filter**  
      - Drop rows missing either cue-response.  
      - Trim, lowercase both columns.  
   3. **Build Lookup**  
      - Create `annotation_dict[(cue_word, response)] = { "macroCode":…, "microCode":… }`.  
   4. **Apply Annotations**  
      - For each `(cue, assoc)` in `cue_dict`:  
        * If `(cue.lower(), assoc.lower())` in `annotation_dict`, add  
          `MacroCode` and/or `MicroCode` via `assoc.add_dimension(...)`.  
   5. **Select Top-20 Associations**  
      - Split into **annotated** vs **unannotated** associations.  
      - Sort unannotated by descending `.frequency`.  
      - Concatenate annotated + unannotated, then slice `[:20]`.  
      - Replace `cue.associations` with this reduced set.

   **Returns**  
   A new `cue_dict` containing only cues that have ≥1 association after filtering,
   each with at most 20 associations (all SME-annotated ones guaranteed included).

Example
-------

.. code-block:: python

    from enhance_swow.aggregator import aggregate_csv
    from enhance_swow.enhancer import add_sme_annotations

    # Step 1: build raw cue_dict
    cue_dict = aggregate_csv("swow_en.csv")

    # Step 2: annotate (English annotations)
    cue_dict = add_sme_annotations(cue_dict,
                                   annotation_csv="coding.v7.COGSCI.en.csv",
                                   language_code="en")

    # Now each Cue.associations has ≤20 entries,
    # and all with MacroCode/MicroCode are preserved.

Notes
-----

- SME CSV must contain columns named `cue.<lang>` and `response.<lang>` (e.g. `cue.zh`).
- If your annotation file fails to load due to encoding, use `safe_read_csv()`
  in place of `pd.read_csv`.
