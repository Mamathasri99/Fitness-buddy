import gradio as gr
from ibm_watsonx_ai.foundation_models import ModelInference

# IBM Granite model served through IBM watsonx.ai.
# If this model is unavailable in your IBM Cloud region/account, choose an
# IBM Granite model currently listed in your watsonx.ai deployment/catalog.
MODEL_ID = "ibm/granite-3-3-8b-instruct"

SYSTEM_PROMPT = """
You are FitnessBuddy, a friendly and supportive AI fitness and healthy-lifestyle coach.
Your purpose is to provide general educational guidance, not medical diagnosis or treatment.
Be encouraging, clear, practical, and conversational.
You can:
- Recommend simple home workouts based on the user's goal, fitness level, time and equipment.
- Share short motivational tips and daily fitness inspiration.
- Suggest simple, nutritious meal ideas based on food preferences.
- Help users build realistic habits and stay consistent.
Ask a brief follow-up question if important information is missing.
Never recommend extreme dieting, starvation, unsafe exercise, unverified supplements,
or guaranteed results. Do not diagnose medical conditions. If a user reports pain,
injury, pregnancy, a chronic condition, or another health concern, recommend speaking
with a qualified healthcare professional before changing their exercise or diet routine.
"""

def make_model(api_key, project_id, url):
    if not api_key or not api_key.strip():
        raise gr.Error("Enter your IBM Cloud API key.")
    if not project_id or not project_id.strip():
        raise gr.Error("Enter your watsonx.ai project ID.")
    if not url or not url.strip():
        raise gr.Error("Choose your IBM watsonx.ai region URL.")

    return ModelInference(
        model_id=MODEL_ID,
        credentials={"url": url.strip(), "apikey": api_key.strip()},
        project_id=project_id.strip(),
        params={
            "max_new_tokens": 700,
            "temperature": 0.6,
            "top_p": 0.9
        }
    )

def fitnessbuddy_chat(message, history, api_key, project_id, url):
    if not message or not message.strip():
        return "Tell me what fitness support you need today."

    model = make_model(api_key, project_id, url)

    conversation = []
    for item in (history or [])[-8:]:
        # Gradio message history may contain role/content dictionaries.
        if isinstance(item, dict) and item.get("role") in ("user", "assistant"):
            conversation.append(f'{item["role"].capitalize()}: {item.get("content", "")}')
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            conversation.append(f"User: {item[0]}\nAssistant: {item[1]}")

    history_text = "\n".join(conversation)
    prompt = f"""{SYSTEM_PROMPT}

Previous conversation:
{history_text}

User: {message}
FitnessBuddy:"""

    try:
        answer = model.generate_text(prompt=prompt)
        if isinstance(answer, str):
            return answer
        return str(answer)
    except Exception as exc:
        raise gr.Error(
            "IBM Granite could not generate a response. Check that your API key, "
            "watsonx.ai project ID, region URL and model access are correct. "
            f"Technical detail: {exc}"
        )

with gr.Blocks(title="FitnessBuddy - IBM Granite Fitness Coach", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🏃‍♀️ FitnessBuddy
        ### Your friendly AI-powered fitness and healthy-lifestyle companion
        Ask for home workouts, healthy meal ideas, motivation and habit-building support.
        """
    )

    with gr.Accordion("Connect IBM watsonx.ai / IBM Granite", open=True):
        api_key = gr.Textbox(
            label="IBM Cloud API Key",
            type="password",
            placeholder="Paste your IBM Cloud API key"
        )
        project_id = gr.Textbox(
            label="watsonx.ai Project ID",
            placeholder="Paste the project ID from your watsonx.ai project"
        )
        region_url = gr.Dropdown(
            choices=[
                "https://us-south.ml.cloud.ibm.com",
                "https://eu-de.ml.cloud.ibm.com",
                "https://eu-gb.ml.cloud.ibm.com",
                "https://jp-tok.ml.cloud.ibm.com"
            ],
            value="https://us-south.ml.cloud.ibm.com",
            label="IBM watsonx.ai Region URL"
        )
        gr.Markdown(
            "Use the region in which your watsonx.ai project was created. "
            "Never share your API key or upload it to GitHub."
        )

    gr.ChatInterface(
        fn=fitnessbuddy_chat,
        additional_inputs=[api_key, project_id, region_url],
        title="Chat with FitnessBuddy",
        description="Example: 'Give me a 20-minute beginner home workout' or 'Suggest a healthy vegetarian lunch.'",
        examples=[
            "Give me a simple 20-minute beginner home workout.",
            "Suggest nutritious vegetarian meal ideas.",
            "Motivate me to stay consistent with exercise.",
            "Help me create a realistic weekly fitness habit."
        ]
    )

    gr.Markdown(
        """
        ---
        **Health and safety:** FitnessBuddy provides general educational information and
        does not replace a doctor, registered dietitian or qualified fitness professional.
        Stop if an activity causes pain or makes you feel unwell. Seek professional advice
        before changing your routine if you have an injury or health concern.
        """
    )

if __name__ == "__main__":
    demo.launch()
