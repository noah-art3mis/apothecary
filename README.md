## Socratic Apothecary

Purification for pdf files. Part of autosimulacrum.

## How to

-   `utils/check_resolution.py`

## Estimated costs per page

    - haiku:    $0.0005 (x200 = 0.1)
    - sonnet:   $0.007  (x200 = 1.4)
    - opus:     $0.03   (x200 = 4.0)
    - (gpt4v)[https://openai.com/pricing]:
        - low-res:  $0.00085 (x200 = 0.17)
        - hi-res:   $0.01105 (x200 = 2.0)

## TODO

-   get pixmaps from annots

-   try claude with pdfs (see https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/best_practices_for_vision.ipynb)
-   annotation extraction / export comments

    -   'pdf data extraction'
    -   https://wrobell.dcmod.org/remt/workflow.html#pdf-annotations-indexer
    -   https://docs.tagtog.com/pdf-annotation-tool.html
    -   https://github.com/lucasrla/remarks
    -   poppler annotation id?
    -   https://library-guides.ucl.ac.uk/zotero/extracting-annotations
    -   ocr ebook
    -   https://nanonets.com/blog/ocr-with-tesseract/
    -   claude performance png x webp?
    -   change from pymupdf to pdfium2 (mu is gpl)

-   gpt4v

    -   search 'vision model ocr performance'
    -   gpt4v system card
    -   https://platform.openai.com/docs/guides/vision

-   use more threads in `convert_from_path`
-   test detail auto x high

## Refs

-   LLMs
    -   https://github.com/anthropics/anthropic-cookbook/blob/main/misc/pdf_upload_summarization.ipynb
    -   https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/reading_charts_graphs_powerpoints.ipynb
-   Anthropic
    -   https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/best_practices_for_vision.ipynb
        -   `{"type": "text", "text": "You have perfect vision and pay great attention to detail which makes you an expert at counting objects in images. How many dogs are in this picture? Before providing the answer in <answer> tags, think step by step in <thinking> tags and analyze every part of the image."}`
-   https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
-   https://nanonets.com/blog/pdf-ocr-python/

    -   pytesseract
    -   pdf2image

-   OCR

    -   tesseract
    -   https://github.com/JaidedAI/EasyOCR
    -   https://github.com/PaddlePaddle/PaddleOCR/blob/main/README_en.md
    -   https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_en/ocr_book_en.md

-   LLM

    -   vision models
    -   claude, gpt4t, qwen, cog, llava

-   PyMuPDF uses GPL license.
    -   alternatives: https://github.com/mindee/doctr/issues/23#issuecomment-795234413
    -   https://martinthoma.medium.com/the-python-pdf-ecosystem-in-2023-819141977442
    -   https://github.com/pypdfium2-team/pypdfium2
    -   pypdf, PyMuPDF, pypdfium2, Tika, pdfplumber, pdfminer.six

##
