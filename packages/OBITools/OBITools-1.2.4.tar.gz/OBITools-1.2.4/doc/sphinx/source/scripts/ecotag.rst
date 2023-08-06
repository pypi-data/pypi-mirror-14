.. automodule:: ecotag

   :py:mod:`ecotag` specific options
   ---------------------------------

   .. cmdoption::  -R <FILENAME>, --ref-database=<FILENAME>

        <FILENAME> is the fasta file containing the reference sequences

   .. cmdoption::  -m FLOAT, --minimum-identity=FLOAT

        When the best match with the reference database present an identity
        level below FLOAT, the taxonomic assignment for the sequence record
        is not computed. The sequence record is nevertheless included in the
        output file. FLOAT is included in a [0,1] interval.

   .. cmdoption::    --minimum-circle=FLOAT

        minimum identity considered for the assignment circle.
        FLOAT is included in a [0,1] interval.

   .. cmdoption::  -x RANK, --explain=RANK

   .. cmdoption::  -u, --uniq

        When this option is specified, the program first dereplicates the sequence
        records to work on unique sequences only. This option greatly improves
        the program's speed, especially for highly redundant datasets.

   .. cmdoption::  --sort=<KEY>

        The output is sorted based on the values of the relevant attribute.

   .. cmdoption::  -r, --reverse

        The output is sorted in reverse order (should be used with the --sort option).
        (Works even if the --sort option is not set, but could not find on what
        the output is sorted).

   .. cmdoption::  -E FLOAT, --errors=FLOAT

        FLOAT is the fraction of reference sequences that will
        be ignored when looking for the lowest common ancestor. This
        option is useful when a non-negligible proportion of reference sequences
        is expected to be assigned to the wrong taxon, for example because of
        taxonomic misidentification. FLOAT is included in a [0,1] interval.


   .. cmdoption::  -M INTEGER, --min-matches=FLOAT

        Define the minimum congruent assignation. If this minimum is reached and
        the -E option is activated, the lowest common ancestor algorithm tolarated
        that some sequences do not provide the same taxonomic annotation (see the
        -E option).


   .. cmdoption::  --cache-size=INTEGER

        A cache for computed similarities is maintained by `ecotag`. the default
        size for this cache is 1,000,000 of scores. This option allows to change
        the cache size.

   .. include:: ../optionsSet/taxonomyDB.txt

   .. include:: ../optionsSet/inputformat.txt

   .. include:: ../optionsSet/outputformat.txt

   .. include:: ../optionsSet/defaultoptions.txt

   :py:mod:`ecotag` added sequence attributes
   ------------------------------------------

      .. hlist::
           :columns: 3

           - :doc:`best_identity <../attributes/best_identity>`
           - :doc:`best_match <../attributes/best_match>`
           - :doc:`family <../attributes/family>`
           - :doc:`family_name <../attributes/family_name>`
           - :doc:`genus <../attributes/genus>`
           - :doc:`genus_name <../attributes/genus_name>`
           - :doc:`id_status <../attributes/id_status>`
           - :doc:`order <../attributes/order>`
           - :doc:`order_name <../attributes/order_name>`
           - :doc:`rank <../attributes/rank>`
           - :doc:`scientific_name <../attributes/scientific_name>`
           - :doc:`species <../attributes/species>`
           - :doc:`species_list <../attributes/species_list>`
           - :doc:`species_name <../attributes/species_name>`
           - :doc:`taxid <../attributes/taxid>`
