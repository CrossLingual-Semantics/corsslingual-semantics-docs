Installation & Prerequisites
============================

This section describes how to set up your environment and install all dependencies for the SWOW Enhancement Pipeline.

Prerequisites
-------------

- **Python** 3.8
- **Poetry** (or pip + virtualenv)  
- **BabelNet API key** and a configuration file `babelnet_conf.yml`  

Environment setup
-----------------

1. **Clone the repository** (replace with your path or URL):

   .. code-block:: bash

      git clone https://github.com/CrossLingual-Semantics/Enhance_SWOW
      cd Enhance_SWOW

2. **Activate your virtual environment**:

   - **With Poetry**:

     .. code-block:: bash

        poetry install
        poetry shell

   - **Or using venv + pip**:

     .. code-block:: bash

        source /home/unimelb.edu.au/manandharshr/.cache/pypoetry/virtualenvs/enhance-swow-XwaD2jyO-py3.8/bin/activate

3. **Configure BabelNet**:

   Place your API key and preferences in `conf/babelnet_conf.yml`:

   .. code-block:: yaml

      babelnet_api_key: YOUR_KEY_HERE
      cache_dir: /path/to/cache

4. **Verify installation**:

   .. code-block:: bash

      python -c "import babelnet; print('BabelNet:', babelnet.__version__)"

You are now ready to run the SWOW Enhancement Pipeline. Proceed to the Usage Guide next.
