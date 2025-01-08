import gradio as gr

from transcript_transformer import TranscriptTransformer

transformer = TranscriptTransformer()


def process_transcript(transcript: str, duration: int):
    yield gr.update(value="Building the lecture..", visible=True)

    transformed_transcript = transformer.generate_lecture(transcript, duration)

    yield gr.update(value=transformed_transcript, visible=True)


demo = gr.Interface(
    fn=process_transcript,
    inputs=[
        gr.Textbox(
            label="Input Transcript",
            placeholder="Paste your transcript here...",
            lines=10,
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


if __name__ == "__main__":
    demo.launch()
