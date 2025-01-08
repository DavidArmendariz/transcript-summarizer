import openai
from dotenv import load_dotenv

load_dotenv()


class TranscriptTransformer:
    def __init__(self):
        # System prompt template for consistent output
        self.system_prompt = """You are an expert educational content creator. 
        Your task is to transform informal transcripts into structured, engaging teaching materials.
        Focus on clarity, logical flow, and educational value."""

        # Template for the lecture structure
        self.lecture_template = """Transform the following transcript into a structured {duration}-minute lecture.
        
        Requirements:
        1. Create a clear introduction that sets context and learning objectives
        2. Organize the content into logical sections with clear headings
        3. Include practical examples and real-world applications
        4. Add discussion questions or interactive elements
        5. Conclude with a summary and key takeaways
        6. Target approximately {word_count} words
        
        Format the output in markdown with clear section headers and proper spacing.
        """

        self.max_model_tokens = 128000

    def split_text_into_chunks(self, text: str) -> list[str]:
        """Split the text into chunks that fit within the token limit."""
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            current_chunk.append(word)
            if len(" ".join(current_chunk)) >= self.max_model_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = []

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def generate_transcript_chunk_summary(
        self, chunk: str, max_output_tokens: int, previous_summary=None
    ) -> str:
        """Summarize the current chunk with the context of the previous chunk."""

        context = (
            f"Summary of previous transcript chunk:\n{previous_summary}\n\n"
            if previous_summary
            else ""
        )

        prompt = f"""
        {context}
        Summarize the following transcript chunk:
        {chunk}
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a highly skilled educator AI."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_output_tokens,
            temperature=0.7,
        )
        generated_text = response.choices[0].message.content or chunk
        return generated_text

    def summarize_text(self, transcript: str, max_output_tokens: int) -> str:
        """Process a large transcript by splitting it into chunks and combining results."""
        chunks = self.split_text_into_chunks(transcript)

        if len(chunks) == 1:
            return chunks[0]

        summarized_transcript = []
        previous_summary = None
        for chunk in chunks:
            teaching_transcript = self.generate_transcript_chunk_summary(
                chunk, max_output_tokens, previous_summary
            )
            summarized_transcript.append(teaching_transcript)
            previous_summary = teaching_transcript
        return "\n\n".join(summarized_transcript)

    def generate_lecture(self, raw_text: str, lecture_duration: int = 30) -> str:
        # An average paced lecturer speaks 130 words per minute
        max_output_tokens = lecture_duration * 130
        summarized_transcript = self.summarize_text(
            raw_text, max_output_tokens=max_output_tokens
        )
        full_text = f"{self.lecture_template.format(
                        duration=lecture_duration, word_count=max_output_tokens
                    )}\n\nTranscript:\n{summarized_transcript}"
        final_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_text},
            ],
            max_tokens=max_output_tokens,
            temperature=0.7,
        )
        return (
            final_response.choices[0].message.content
            or "Error: No response from the model."
        )
