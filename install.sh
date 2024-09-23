# 1. clone 
git clone https://github.com/wenhuizhang/transformers.git
cd transformers

# 2. (Optional) Create and activate virtual environment
python -m venv transformers_venv
source transformers_venv/bin/activate

# 3. Install dependencies and transformers from source
pip install -e .

# 4. Verify installation
python -c "import transformers; print(transformers.__version__)"

# 5. (Optional) Run tests
pip install pytest
pytest tests
