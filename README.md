## Socratic Apothecary

Purification for pdf files. Part of autosimulacrum.

LMM extraction is bad enough that I can't recommend it. It's sensitive to the prompt.

## How to

-   `utils/check_resolution.py`

## LLM OCR possible issues

-   classification too sensitive
-   classification not sensitive enough
-   extracts more than it should

## Estimated costs per page

    - haiku:    $0.0005 (x200 = 0.1)
    - sonnet:   $0.007  (x200 = 1.4)
    - opus:     $0.03   (x200 = 4.0)
    - (gpt4v)[https://openai.com/pricing]:
        - low-res:  $0.00085 (x200 = 0.17)
        - hi-res:   $0.01105 (x200 = 2.0)

## ~

    - claude
        - accepts webp

## TODO

-   annotation extraction / export comments

    -   'pdf data extraction'
    -   https://wrobell.dcmod.org/remt/workflow.html#pdf-annotations-indexer
    -   https://docs.tagtog.com/pdf-annotation-tool.html
    -   https://github.com/lucasrla/remarks
    -   poppler annotation id?
    -   https://library-guides.ucl.ac.uk/zotero/extracting-annotations
    -   ocr ebook
    -   https://nanonets.com/blog/ocr-with-tesseract/

-   gpt4v

    -   search 'vision model ocr performance'
    -   gpt4v system card
    -   https://platform.openai.com/docs/guides/vision

-   use more threads in `convert_from_path`
-   test detail auto x high

## Refs

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

##
