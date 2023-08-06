.. automodule:: obisubset
 

   :py:mod:`obisubset` specific options
   ------------------------------------

   .. cmdoption::  -s <TAGNAME>,  --sample=<TAGNAME>,

     The option ``-s`` allows to specify the tag containing sample descriptions,
     the default value is set to *merged_sample*.

     *Example:*

         .. code-block:: bash

             > obiuniq -m sample seq1.fasta > seq2.fasta
             > obisubset -s merged_sample -n sample1 seq2.fasta > seq3.fasta

         After the dereplication of the sequences using the
         in the new attribute ``merged_sample``.

   .. cmdoption::  -o <TAGNAME>,  --other-tag=<TAGNAME>,

     Another tag to clean according to the sample subset

     *Example:*

          .. code-block:: bash

              > obisubset -s merged_sample -o -n sample1 seq2.fasta > seq3.fasta

   .. cmdoption::  -l <FILENAME>,  --sample-list=<FILENAME>,

     File containing the samples names (one sample id per line).

     *Example:*

          .. code-block:: bash

              > obisubset -s merged_sample -o -l ids.txt seq2.fasta > seq3.fasta

   .. cmdoption::  -p <REGEX>,  --sample-pattern=<REGEX>,

     A regular expression pattern matching the sample ids to extract.

     *Example:*

         .. code-block:: bash

             > obisubset -s merged_sample -o -p "negative_.*" seq2.fasta > seq3.fasta

   .. cmdoption::  -n <SAMPLEIDS>,  --sample-name=<SAMPLEIDS>,

     A sample id to extract

     *Example:*

          .. code-block:: bash

              > obisubset -s merged_sample -o -n sample1 seq2.fasta > seq3.fasta

   .. include:: ../optionsSet/inputformat.txt

   .. include:: ../optionsSet/outputformat.txt

   .. include:: ../optionsSet/defaultoptions.txt

   :py:mod:`obisubset` modifies sequence attributes
   ------------------------------------------------

      .. hlist::
           :columns: 3

           - :doc:`count <../attributes/count>`
           - :doc:`merged_* <../attributes/merged_star>`

   :py:mod:`obisubset` used sequence attribute
   -------------------------------------------

           - :doc:`count <../attributes/taxid>`
           - :doc:`merged_* <../attributes/merged_star>`
