All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer. Redistributions in binary 
form must reproduce the above copyright notice, this list of conditions and the 
following disclaimer in the documentation and/or other materials provided 
with the distribution.
Neither the name of ETH Zürich nor the names of its contributors may be used 
to endorse or promote products derived from this software without specific 
prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description: Brightway2 input and output
        ===========================
        
        This package provides tools for the import, export, and management of inventory databases and impact assessment methods. It is part of the `Brightway2 LCA framework <https://brightwaylca.org>`_. `Online documentation <https://docs.brightwaylca.org/>`_ is available, and the source code is hosted on `Bitbucket <https://bitbucket.org/cmutel/brightway2-io>`_.
        
        In contrast with previous IO functionality in Brightway2, brightway2-io uses an iterative approach to importing and linking data. First, data is *extracted* into a common format. Next, a series of *strategies* is employed to uniquely identify each dataset and link datasets internally and to the biosphere. Following internal linking, linking to other background datasets can be performed. Finally, database data is written to disk.
        
        This approach offers a number of benefits that help mitigate some of the serious problems in existing inventory data formats: the number of unlinked exchanges can be easily seen, linking strategies can be iteratively applied, and intermediate results can be saved.
        
        Here is a typical usage:
        
        .. code-block:: python
        
            In [1]: from bw2io import *
        
            In [2]: so = SingleOutputEcospold2Importer("/path/to/ecoinvent/3.1/cutoff/datasets", "ecoinvent 3.1 cutoff")
            11301/11301 (100%) |||||||||||||||||||||||||||||||||||||||||||||||||||||||||| Time: 0:01:56
            Converting to unicode
            Extracted 11301 datasets in 262.63 seconds
        
            In [3]: so.apply_strategies()
            Applying strategy: remove_zero_amount_coproducts
            Applying strategy: remove_zero_amount_inputs_with_no_activity
            Applying strategy: es2_assign_only_product_with_amount_as_reference_product
            Applying strategy: assign_single_product_as_activity
            Applying strategy: create_composite_code
            Applying strategy: link_biosphere_by_flow_uuid
            Applying strategy: link_internal_technosphere_by_composite_code
            Applying strategy: delete_exchanges_missing_activity
            Applying strategy: delete_ghost_exchanges
            Applying strategy: mark_unlinked_exchanges
        
            In [4]: so.statistics()
            11301 datasets
            521712 exchanges
            0 unlinked exchanges
            Out[4]: (11301, 521712, 0)
        
            In [5]: so.write_database()
        
        Note that brightway2-io can't magically make problems in databases go away.
        
Platform: UNKNOWN
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: End Users/Desktop
Classifier: Intended Audience :: Developers
Classifier: Intended Audience :: Science/Research
Classifier: License :: OSI Approved :: BSD License
Classifier: Operating System :: MacOS :: MacOS X
Classifier: Operating System :: Microsoft :: Windows
Classifier: Operating System :: POSIX
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 2 :: Only
Classifier: Topic :: Scientific/Engineering :: Information Analysis
Classifier: Topic :: Scientific/Engineering :: Mathematics
Classifier: Topic :: Scientific/Engineering :: Visualization
