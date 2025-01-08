import gradio as gr
from pypdf import PdfReader

from transcript_transformer import TranscriptTransformer

transformer = TranscriptTransformer()

def process_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file.name)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_transcript(transcript_text: str, pdf_file, duration: int):
    yield gr.update(value="Building the lecture..", visible=True)
    
    # Use PDF content if provided, otherwise use transcript text
    if pdf_file:
        transcript = process_pdf(pdf_file)
    else:
        transcript = transcript_text
        
    transformed_transcript = transformer.generate_lecture(transcript, duration)
    yield gr.update(value=transformed_transcript, visible=True)


with gr.Blocks() as demo:
    accordion1 = gr.Accordion("How prompts were engineered and refined?", open=False)
    with accordion1:
        gr.Markdown("This is some additional information about the app.")
        gr.Markdown("You can add more details here as needed.")

    accordion2 = gr.Accordion("Challenges faced", open=False)
    with accordion2:
        gr.Markdown("This is some additional information about the app.")
        gr.Markdown("You can add more details here as needed.")

    accordion3 = gr.Accordion("How the system can be extended or scaled?", open=False)
    with accordion3:
        gr.Markdown("This is some additional information about the app.")
        gr.Markdown("You can add more details here as needed.")

    gr.Interface(
        fn=process_transcript,
        inputs=[
            gr.Textbox(
                label="Input Transcript",
                placeholder="Paste your transcript here...",
                lines=10,
            ),
            gr.File(
                label="Or Upload PDF",
                file_types=[".pdf"],
            ),
            gr.Slider(
                minimum=15,
                maximum=60,
                value=30,
                step=15,
                label="Lecture Duration (minutes)",
            ),
        ],
        outputs=gr.Markdown(label="Transformed Teaching Transcript"),
        title="Transcript to Teaching Material Transformer",
        description="""Transform transcripts into teaching materials.
        The output will be formatted as a complete lecture with clear sections,
        examples, and interactive elements.""",
        theme="default",
    )

demo.launch()
