# if you say 'yellow text' it loses too much sensitivity
prompt_classification = """Check this page for any highlighted text. Respond with 'Y' if there is any highlighted text, and 'N' if there is none. Use only these two responses for clarity."""

# PROMPT_EXTRACTION = """Scan this page for any text highlighted in yellow. If you find yellow highlighted text, extract it. There might be multiple blocks of highlighted text. If that is the case, treat them as separate entities. Provide the output in JSON format, including the page number and the extracted text. For each block of text, format the response as follows: {'page_number': "[page_number]", 'highlighted_text': '[extracted_text]'}. If there is no highlighted text, respond with an empty string."""

PROMPT_EXTRACTION = "Examine this page for any text highlighted in yellow. If you identify one or more blocks of yellow highlighted text, extract each block separately. For each block, provide the output in a structured JSON format that includes the page number and the extracted text."

SYSTEM_EXTRACTION = "Respond exclusively in JSON. Don't use line breaks. The JSON must have two fields: page_number (which is a string) and highlighted_text (an array of strings). If no highlighted text is present, respond with an empty string to indicate the absence of highlighted content."

# PROMPT_EXTRACTION = "Review this page to identify any text highlighted in yellow. If you find yellow highlighted text, extract it. For each block of highlighted text, note the page number and the text itself. If multiple blocks are present, handle each separately. If no yellow highlighted text is found, do not perform any extraction."

# SYSTEM_EXTRACTION = "Generate a response in JSON format only if yellow highlighted text is found. The JSON should include two fields: 'page_number' (a string indicating the page on which the text is found) and 'highlighted_text' (an array containing strings of extracted text). If no highlighted text is present on the page, provide a JSON object with an empty 'highlighted_text' array to clearly indicate the absence of highlighted content."
