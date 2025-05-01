Aggregator Module
=================

This module ingests the raw SWOW CSV file and converts it into our in-memory data model
of `Cue` and `Association` objects.

Source
------

:mod:`enhance_swow.aggregator`
:   ``enhance_swow/aggregator.py``

Overview
--------

- **Input:** A CSV with columns `cue, R1, R2, R3`
- **Output:** A Python dict mapping each cue word to a :class:`~enhance_swow.models.cue.Cue`
  instance, whose `.associations` field holds :class:`~enhance_swow.models.association.Association`
  objects with frequency counts.

Functions
---------

.. autofunction:: enhance_swow.aggregator.aggregate_csv

Implementation Details
----------------------

.. code-block:: python

    import pandas as pd
    from enhance_swow.models.cue import Cue

    def aggregate_csv(input_path: str) -> dict[str, Cue]:
        \"\"\"
        Read SWOW CSV and build Cue→Association frequencies.

        :param input_path: Path to SWOW CSV file.
        :returns: Dict where keys are cue words and values are Cue objects.
        \"\"\"
        df = pd.read_csv(input_path, encoding="utf8")
        cue_dict: dict[str, Cue] = {}

        for _, row in df.iterrows():
            cue_word = row['cue']

            # initialize Cue if needed
            if cue_word not in cue_dict:
                cue_dict[cue_word] = Cue(cue_word)

            # aggregate each of the three responses
            for response_col in ['R1', 'R2', 'R3']:
                assoc = row[response_col]
                if pd.notnull(assoc):
                    if assoc in cue_dict[cue_word].associations:
                        cue_dict[cue_word].associations[assoc].frequency += 1
                    else:
                        cue_dict[cue_word].add_association(assoc, 1)

        return cue_dict

Notes
-----

- We assume the input CSV is UTF-8 encoded.
- Frequencies count how many times each association appears for each cue.
- Invalid or missing responses (NaN) are automatically skipped.
