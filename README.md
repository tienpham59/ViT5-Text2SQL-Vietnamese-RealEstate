# ViT5-Text2SQL-Vietnamese-RealEstate

A Vietnamese Text-to-SQL for Real Estate system using ViT5 and Gradio

This project builds a Text-to-SQL system for Vietnamese real estate queries, using the ViT5 language model and a simple Gradio interface. It allows users to input Vietnamese natural language questions (e.g., "Nhà dưới 3 tỷ ở quận Phú Nhuận") and receive an executable SQL query to retrieve matching results from a real estate database.

## Project Structure

notebooks/
Phase\_1\_CE\_S2S.ipynb: Fine-tuning with Cross-Entropy loss only (Phase 1)
Phase\_2\_CE+RL\_final\_model.ipynb: Fine-tuning with Cross-Entropy + Reinforcement Learning (Phase 2)
run\_gradio.ipynb: Launch Gradio interface for demo

model/
Phase1\_CEonly/: Output directory after Phase 1 training
Final\_model/: Final model after Phase 2 training

data/
Contains your training dataset and schema definitions

Project\_Text\_to\_SQL - NLP/
Contains the question generation pipeline (optional, for completeness)

## How to Train the Model

Note: Make sure to fix any %cd .. or file path instructions in the notebooks to match your actual directory structure.

### Step 1 – Train with Cross-Entropy Loss

Open and run `notebooks/Phase_1_CE_S2S.ipynb`. This notebook fine-tunes the ViT5 model on question-SQL pairs using cross-entropy loss. The trained model will be saved to `model/Phase1_CEonly/`.

### Step 2 – Train with Cross-Entropy + Reinforcement Learning

Open and run `notebooks/Phase_2_CE+RL_final_model.ipynb`. This continues training by incorporating reward signals based on SQL execution correctness. The final model is saved to `model/Final_model/`.

## Run Gradio Demo

To launch the user interface, open `notebooks/run_gradio.ipynb`. This loads the final trained model from `model/Final_model/` and allows interactive querying. Users can input Vietnamese questions, view the generated SQL, and optionally run the query on a connected SQLite real estate database.

## Question Generation Pipeline (Optional)

Folder `Project_Text_to_SQL - NLP` includes a pipeline to generate synthetic training data (question, schema, SQL triplets). This part is not required to run the system, as a prepared sample dataset is already included. It is provided for completeness if you want to extend or regenerate the dataset.

### How to Use:

1. Edit `run_pipeline.py` and set:

```python
NUM_SAMPLES = 15000  # Number of samples to generate
```

2. Run the pipeline:

```bash
python run_pipeline.py
```

3. (Optional) To adjust the distribution of SQL query types, open `sql_type_manager.py` and make sure all values in `SQL_TYPE_RULES` are set to 1 for balanced generation:

```python
SQL_TYPE_RULES = {
    'simple_query':               {'sql_type': 'select',                        'ratio': 0.01},
    'top_k_query':                {'sql_type': 'select_orderby_desc_limit_k',   'ratio': 0.03},
    'range_query':               {'sql_type': 'select_where',                  'ratio': 0.06}, 
    ...
}
```

## Dependencies

transformers
gradio
unidecode
tabulate

## Notes

The trained model is not included in this repository due to size. You must train it yourself following the steps above.

You can customize and expand the training data under the `data/` directory to improve performance.

## Contact

For collaboration or questions, feel free to reach out via GitHub: [https://github.com/tienpham59](https://github.com/tienpham59)
