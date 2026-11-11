import gradio as gr
from groq import Groq

MODEL = "openai/gpt-oss-20b"

def generate_plan(api_key, level, days, equipment, food):
    if not api_key or not api_key.strip():
        raise gr.Error("Please enter your Groq API key.")

    prompt = f"""
Create a clear weekly fitness and food plan.

Fitness level: {level}
Workout days per week: {days}
Available equipment: {equipment}
Food preference: {food}

Include:
1. Weekly workout timetable.
2. Exercises with sets and repetitions.
3. Warm-up and cool-down.
4. Rest days and recovery.
5. One-day meal plan with breakfast, lunch, snacks and dinner.
6. Water, sleep and healthy lifestyle tips.

Use simple language and clear headings.
If no equipment is available, use bodyweight exercises.
Avoid extreme diets and unsafe exercises.
Mention that people with injuries or medical conditions
should consult a healthcare professional.
"""

    try:
        client = Groq(api_key=api_key.strip())

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are Fitness Buddy, a helpful and safety-conscious fitness assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            max_completion_tokens=2000
        )

        return response.choices[0].message.content

    except Exception as e:
        raise gr.Error(f"Connection error: {str(e)}")

with gr.Blocks(theme=gr.themes.Soft(), title="Fitness Buddy") as demo:

    gr.Markdown("# 💪 FITNESS BUDDY")
    gr.Markdown("### Your personal AI fitness and nutrition assistant")

    api_key = gr.Textbox(
        label="Groq API Key",
        placeholder="Paste your Groq API key here",
        type="password"
    )

    level = gr.Radio(
        ["Beginner", "Intermediate", "Advanced"],
        value="Beginner",
        label="Fitness Level"
    )

    days = gr.Slider(
        minimum=1,
        maximum=7,
        value=3,
        step=1,
        label="Workout Days Per Week"
    )

    equipment = gr.Dropdown(
        choices=[
            "No equipment",
            "Dumbbells",
            "Resistance bands",
            "Gym equipment",
            "Bodyweight and basic home equipment"
        ],
        value="No equipment",
        label="Available Equipment"
    )

    food = gr.Radio(
        ["Vegetarian", "Non-Vegetarian", "Vegan"],
        value="Non-Vegetarian",
        label="Food Preference"
    )

    generate = gr.Button(
        "✨ Generate My Fitness Plan",
        variant="primary"
    )

    output = gr.Markdown(label="Your Fitness Plan")

    generate.click(
        fn=generate_plan,
        inputs=[api_key, level, days, equipment, food],
        outputs=output
    )

    gr.Markdown("""
    ---
    **Disclaimer:** This application provides general educational
    fitness and nutrition suggestions. It is not a replacement
    for professional medical advice.

    **Developed using Python, Gradio and Groq.**
    """)

demo.launch(share=True, debug=True)
