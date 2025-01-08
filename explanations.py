explanation1 = """
I used two system prompts: one for summarizing the chunks if they surpass the amount of tokens
of gpt-4o-mini (the LLM model used for this app) and another one for the final response.
These were just to guide the AI that it is an expert educational content creator and to act like one.

I also used two user prompts for the same reason. One for summarizing chunks (if needed) and another
one for the final response. The user prompt for summarizing chunks includes the context of the previous
chunk and the current chunk. The user prompt for the final response includes the duration of the lecture
and the word count of the transcript. The word count of the transcript assumes that an average paced lecturer
speaks 130 words per minute.

They system prompt to generate the lecture tells the AI that it must focus on clarity,
logical flow, and educational value.

The user prompt to generate the lecture clearly describes the requirements to give structure to
the lecture and to make it more understandable, stating that it must:

1. Create a clear introduction that sets context and learning objectives
2. Organize the content into logical sections with clear headings
3. Include practical examples and real-world applications
4. Add discussion questions or interactive elements
5. Conclude with a summary and key takeaways
6. Target approximately {word_count} words

and to format the output in markdown with clear section headers and proper spacing.
"""

explanation2 = """
The main challenge was to maintain the context of the different
chunks of the transcript and then combine them (if the total amount of tokens of the transcript surpasses the limit). 
I had to make sure that the AI understands the context of the previous chunk and then summarize the current chunk
accordingly.
"""

explanation3 = """
The system can be extended by adding dynamic model selection.
This means using other LLMs like Claude or open source LLMs from HuggingFace to see different results and
stay with the one that is the best in terms of costs and performance.

Another idea is to generate content according to the level of difficulty.
For example, content for beginners, intermediate learners, or advanced audiences.

Also the system could handle videos, written articles, or interactive presentations.

Finally, the system could be deployed as an API to integrate it with other services.
"""