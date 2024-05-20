from utils.md2json import md2json
import pytest

def test_md2json_0():
    input = """
    ## METADATA
fg
Bruno Latour
Facing Gaia

## PAGES

### 12

My original discipline, science studies, finds itself reinforced today by the widely accepted understanding that the old constitution, the one that distributed powers between science and politics, has become obsolete.

… It is impossible to understand what is happening to us without turning to the sciences – the sciences have been the first to sound the alarm.

And yet, to understand them, it is impossible to settle for the image offered by the old epistemology; the sciences are now and will remain from now on so intermingled with the entire culture that we need to turn to the humanities to understand how they really function.

Hence a hybrid style for a hybrid subject addressed to a necessarily hybrid audience.

### 18

But here we are: what could have been just a passing crisis has turned into a profound alteration of our relation to the world. It seems as though we have become the people who could have acted thirty or forty years ago – and who did nothing, or far too little.

… Just imagine that something has happened that is not ahead of us, as a threat to come, but rather behind us, behind those who have already been born. How can we not feel rather ashamed that we have made a situation irreversible because we moved along like sleepwalkers when the alarms sounded?

And yet we haven't lacked for warnings. The sirens have been blaring all along.
"""

    expected = """
    {
  "id": "fg",
  "author": "Bruno Latour",
  "title": "Facing Gaia",
  "pages": [
    {
      "number": "12",
      "content": [
        "My original discipline, science studies, finds itself reinforced today by the widely accepted understanding that the old constitution, the one that distributed powers between science and politics, has become obsolete.",
        "\u2026 It is impossible to understand what is happening to us without turning to the sciences \u2013 the sciences have been the first to sound the alarm.",
        "And yet, to understand them, it is impossible to settle for the image offered by the old epistemology; the sciences are now and will remain from now on so intermingled with the entire culture that we need to turn to the humanities to understand how they really function.",
        "Hence a hybrid style for a hybrid subject addressed to a necessarily hybrid audience."
      ]
    },
    {
      "number": "18",
      "content": [
        "But here we are: what could have been just a passing crisis has turned into a profound alteration of our relation to the world. It seems as though we have become the people who could have acted thirty or forty years ago \u2013 and who did nothing, or far too little.",
        "\u2026 Just imagine that something has happened that is not ahead of us, as a threat to come, but rather behind us, behind those who have already been born. How can we not feel rather ashamed that we have made a situation irreversible because we moved along like sleepwalkers when the alarms sounded?",
        "And yet we haven't lacked for warnings. The sirens have been blaring all along."
      ]
    }
]
    """
    assert md2json(input) == expected
