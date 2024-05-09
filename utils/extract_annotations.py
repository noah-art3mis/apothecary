import subprocess


def get_annots_from_pdf(file_name):
    params = [
        "pdfannots",
        "-p",
        "-f",
        "json",
        f"input/{file_name}.pdf",
        "-o",
        f"intermediate/{file_name}_0.json",
    ]

    subprocess.run(params)
