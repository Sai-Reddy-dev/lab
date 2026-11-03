
from google.colab import userdata
from groq import Groq
import re

# Get API key from Google Colab Secrets
GROQ_API_KEY = userdata.get("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

MODEL = "openai/gpt-oss-20b"

# Structured Prompt
structured_prompt = """
You are a health and wellness researcher.

[Task]
Provide three key benefits of daily exercise.

[Formatting Requirements - STRICT]

1. Section 1: Output a Markdown table with exactly two columns
labeled 'Benefit' and 'Description'. Include 3 rows of data.

2. Section 2: Output a bulleted list titled 'Recommended Daily Goals'
containing exactly 3 bullet points starting with standard dash symbols ('- ').

Do not add any conversational intro or conclusion.
Output ONLY the requested Markdown structures.
"""


# Function to execute prompt
def execute_prompt(prompt_text: str) -> str:

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content.strip()


# Function to verify Markdown table
def verify_markdown_table(text: str) -> bool:

    lines = text.splitlines()

    # Check table header
    has_header = any(
        re.fullmatch(r"\|\s*Benefit\s*\|\s*Description\s*\|", line.strip())
        for line in lines
    )

    # Check table divider
    has_divider = any(
        re.fullmatch(r"\|\s*:?-{3,}:?\s*\|\s*:?-{3,}:?\s*\|", line.strip())
        for line in lines
    )

    # Count table data rows
    table_rows = [
        line for line in lines
        if line.strip().startswith("|")
        and "Benefit" not in line
        and "---" not in line
    ]

    return has_header and has_divider and len(table_rows) == 3


# Function to verify bullet list
def verify_bullet_list(text: str) -> bool:

    bullets = [
        line for line in text.splitlines()
        if line.startswith("- ")
    ]

    return len(bullets) == 3


# Final Testing
try:

    print("Executing Structured Format Prompt on Groq...\n")

    output = execute_prompt(structured_prompt)

    print("=" * 80)
    print("MODEL OUTPUT")
    print("=" * 80)

    print(output)

    print("\n" + "=" * 80)
    print("STRUCTURE VERIFICATION CHECKS")
    print("=" * 80)

    table_valid = verify_markdown_table(output)
    bullets_valid = verify_bullet_list(output)

    print(
        "1. Markdown Table Verification "
        "('Benefit' & 'Description' columns, 3 rows): "
        f"{'PASSED' if table_valid else 'FAILED'}"
    )

    print(
        "2. Bullet List Verification "
        "(3 bullet points starting with '- '): "
        f"{'PASSED' if bullets_valid else 'FAILED'}"
    )

    if table_valid and bullets_valid:

        print(
            "\nOVERALL VERIFICATION: SUCCESS\n"
            "Output matched all structural constraints!"
        )

    else:

        print(
            "\nOVERALL VERIFICATION: FAILED\n"
            "Output did not match all structural constraints."
        )

except Exception as e:

    print(f"\nAPI Error: {e}")


#pip install groq

#from google.colab import userdata

#GROQ_API_KEY = userdata.get("GROQ_API_KEY")