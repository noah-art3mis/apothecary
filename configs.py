from utils.prompts import PROMPT_EXTRACTION, SYSTEM_EXTRACTION
from utils.models import CLAUDE

FILE_NAME = "ksi-pt1"
# FILE_NAME = "test"
PAGE_LIMIT = 10
MODEL = CLAUDE.OPUS.value.id
PROMPT = PROMPT_EXTRACTION
SYSTEM = SYSTEM_EXTRACTION

IMAGE_TYPE = "image/png"
FILE_PATH = f"./input/{FILE_NAME}.pdf"
OUTPUT_FILE = f"./output/{FILE_NAME}-{MODEL}.jsonl"
