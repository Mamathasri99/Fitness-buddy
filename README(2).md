# FitnessBuddy — IBM Granite AI Fitness Coach

**Problem Statement No. 13**

FitnessBuddy is a conversational, AI-powered health and fitness assistant. It aims to make basic fitness support accessible and friendly by offering home-workout suggestions, motivational tips, simple nutritious meal ideas and habit-building guidance.

## Mandatory technology
This version uses **IBM Granite through IBM watsonx.ai**. It is not the earlier Groq-based version.

## Main features
- Conversational fitness assistant.
- Home workout recommendations based on user input.
- Motivational tips and daily fitness inspiration.
- Simple nutritious meal ideas.
- Habit-building and consistency support.
- Gradio web interface.

## Technology stack
- Python
- Gradio
- IBM watsonx.ai
- IBM Granite language model
- Git and GitHub

## Project files
- `app.py` — complete application source code.
- `requirements.txt` — required Python packages.
- `problem_statement.pdf` — Problem Statement No. 13 and project objectives.
- `project_presentation.pptx` — project presentation.
- `.gitignore` — excludes local and sensitive files.

## IBM watsonx.ai setup
1. Sign in to IBM Cloud and open watsonx.ai.
2. Create or open a watsonx.ai project.
3. Copy the project ID from the project details.
4. Create an IBM Cloud API key.
5. Confirm that the selected Granite model is available to your account and region.
6. In the FitnessBuddy app, enter the API key, project ID and correct region URL.

**Important:** IBM Cloud Lite availability, model access and quotas depend on IBM's current service terms and account. Do not assume every model or service is free or enabled in every region.

## Run on Google Colab
Upload `app.py` and run:

```python
!pip install -r requirements.txt
!python app.py
```

For a public Gradio link in Colab, change `demo.launch()` at the bottom of `app.py` to `demo.launch(share=True)`. Keep the API key private and only share the app link with people you trust.

## Run locally
```bash
pip install -r requirements.txt
python app.py
```

Open the local Gradio address shown in the terminal.

## GitHub repository
Student repository supplied:
https://github.com/Mamathasri99/Fitness-buddy

Upload the project files to that repository. The repository should contain `app.py`, `README.md`, `requirements.txt`, `problem_statement.pdf`, `project_presentation.pptx`, and other required project files.

## Safety and limitations
FitnessBuddy provides general educational information, not medical advice. It cannot diagnose or treat medical conditions and does not guarantee health or fitness outcomes. Users with pain, injury, pregnancy, chronic conditions or other health concerns should consult a qualified healthcare professional before changing exercise or diet routines.

## Model configuration
The code currently uses `ibm/granite-3-3-8b-instruct`. If it is not available in your watsonx.ai project or region, replace `MODEL_ID` in `app.py` with an IBM Granite model that is currently available to your account.
