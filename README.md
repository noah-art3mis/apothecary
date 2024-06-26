## Automaton - Apothecary

Purification for pdf files. 

Results in a json file. Convert to .md for a manual cleanup pass, then convert back to json or yaml that can then be ingested by Semblance. If you want to translate it, do it before that.

Part of AUTOMATON, the simulacrum automation package:
- [Apothecary](https://github.com/noah-art3mis/apothecary) (text extraction and cleanup)
- [Mirage](https://github.com/noah-art3mis/mirage) (palette chooser)
- [Semblance](https://github.com/noah-art3mis/semblance) (image generation)

## How to

Before doing anything:

1. make sure the ocr quality of the original pdf is not terrible
1. highlight pdf with desired annotations

Now:

1. clone this repo
    - `git clone https://github.com/noah-art3mis/apothecary.git`
1. install requirements
    - `pip install requirements.txt`
1. move pdf file to `input` folder
1. set `INPUT_FILE` in configs (just the name of the file, without extension)
1. set `AUTHOR`, `TITLE` and `BOOK_ID`
    - author: author of the book
    - title: title of the book
    - id: a string to identify the book (such as "tst", "ime", "ose", etc.)
1. set `PAGE_OFFSET`
    - this only matters if you want to know exactly which page the annotation comes from. leave at 0 otherwise.
    - scanned pdfs usually misalign the page number of the book with the page number of the pdf.
    - check how many pages you need to add or subtract to make the pages sync. check in a few places since it can vary
        - if pdf_page is 100 and page is 90, the page offset should be -10
        - if pdf_page is 100 and page is 110, the page offset should be 10
1. set `ANTHROPIC_API_KEY` and/or `OPENAI_API_KEY` in `.env`
    - get an API key if you don't have one (i.e. [here](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)).
    - make a `.env` file with your API key.
        - `echo "ANTHROPIC_API_KEY=your_api_key_here" > .env`
    - API calls cost money. See [here](https://artificialanalysis.ai/)
1. set `MODEL`
    - options:
        - `haiku`: less than 10 cents per book. (12x cheaper than sonnet)
        - `sonnet`: less than $1 per book. this is the default.
        - `opus`: i don't know (5x more expensive than sonnet)
        - `gpt4o`: if sonnet costs $6, this one costs $7.5. it is bigger, better and faster. This is now the obvious choice.
1. extract annotations from pdf. this step also cleans up some stuff.
    - `python3 purify.py`
    - output does not show in stdin, but in `purify.log`
1. output is saved at `output`
    - if you need to debug something, intermediate steps are saved at `intermediates`
    - check changes in a [diffchecker](https://www.diffchecker.com/text-compare/)
    - returns a .md file
1. check logs to see if anything is amiss (errors from the api, etc). if changing models, you might need to change the prompt as well
1. edit prompt if necessary
1. check diffs (4 and 5 are the ai cleanup ones)
1. manually edit output. move to `ready`
1. run `python3 utils/md2json.py ready/<file>.md ready/<file>.json` (pupil/squire/protege)

## TODO

-   fix quotation marks
-   refactor
-   test prompts with crucible
-   notify if any errors happened at the end
-   add skip ai cleanup
-   separate identification and correction [tasks](https://docs.anthropic.com/claude/docs/chain-prompts#validating-outputs)

## Known issues

-   doesnt concatenate annotations between pages
-   concatenates in the same page even if different
-   does not treat ellipses properly if they were already in the text. won't be fixed
-   does not keep original formatting (italics, etc)

## Refs

-   PDF annotation tools

    -   pdfannots
    -   [remarks](https://github.com/lucasrla/remarks)
    -   https://github.com/pymupdf/PyMuPDF/issues/318#issuecomment-657102559
    -   https://stackoverflow.com/a/62859169
    -   https://stackoverflow.com/a/73646610
    -   systools pdf extractor
    -   https://docs.tagtog.com/pdf-annotation-tool.html
    -   https://wrobell.dcmod.org/remt/workflow.html#pdf-annotations-indexer
    -   pdf annotator
    -   [sumnotes](https://github.com/0xabu/pdfannots)
    -   poppler https://stackoverflow.com/questions/21050551/extracting-text-from-highlighted-annotations-in-a-pdf-file

-   text splitters

    -   https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.sent_tokenize
    -   https://github.com/rpawk/text_chunker
    -   https://github.com/umarbutler/semchunk
    -   https://github.com/benbrandt/text-splitter
    -   https://github.com/algolia/chunk-text
    -   https://pypi.org/project/chunkipy/
    -   https://github.com/akalsey/textchunk (js)

-   tests:

    -   300~400

    -   41
        -   Acho que a ideia de Boltzmann é impressionante em sua ousadia e beleza. Mas também acho que ela é bastante insustentável, pelo menos para um realista. Ela classifica a mudança unidirecional como uma ilusão. Isso faz com que a catástrofe de Hiroshima seja uma ilusão. Assim, torna nosso mundo uma ilusão e, com ele, todas as nossas tentativas de descobrir mais sobre nosso mundo. Portanto, ele é autodestrutivo (como todo idealismo).
            -   432
    -   42
        -   ... ao apoiar tacitamente as normas socialmente aceitas e ao apresentar a discussão na linguagem das "funções psicossexuais", o psicanalista faz parecer que não está preocupado com as normas, mas apenas com os "processos biológicos". Isso é exatamente o que Freud fez em seus Três Ensaios sobre a Teoria da Sexualidade e também em muitos de seus outros trabalhos. [...]
            -   370
        -   Os fungos são famosos por mudarem de forma em relação a seus encontros e ambientes. Muitos são "potencialmente imortais", o que significa que morrem de doenças, lesões ou falta de recursos, mas não de velhice. Até mesmo esse pequeno fato pode nos alertar sobre o quanto nossos pensamentos sobre conhecimento e existência pressupõem apenas uma forma de vida e uma envelhecimento determinados.
            -   391
        -   A ironista... é uma nominalista e uma historicista. Ela acha que nada tem uma natureza intrínseca, uma essência real. Portanto, ela pensa que a ocorrência de um termo como “justo” ou “científico” ou “racional” no vocabulário final do dia não é razão para pensar que a investigação socrática sobre a essência da justiça ou da ciência ou da racionalidade levará além dos jogos de linguagem da época.
            -   397
    -   43
        -   A produção é deixada à mercê da diversidade tumultuosa da não-escalabilidade, com seus sonhos e esquemas relacionalmente particulares. Conhecemos melhor esse fato na "corrida para o fundo do poço": o papel das cadeias de suprimentos globais na promoção de trabalho forçado, fábricas perigosas, ingredientes substitutos venenosos e irresponsáveis de goivagem e poluição ambiental.
            -   379
        -   Quando torço o tornozelo, uma bengala robusta pode me ajudar a andar, e eu peço sua ajuda. Agora sou um encontro em movimento, uma mulher-e-bengala. É difícil para mim pensar em qualquer desafio que eu possa enfrentar sem solicitar a ajuda de outros, humanos e não humanos. É um privilégio inconsciente que nos permite fantasiar - contra fatos - que cada um de nós sobrevive sozinho.
            -   383
        -   Tais opiniões são muito comuns; mas não tenho dúvidas de que interpretam mal Marx. Aqueles que o admiram por tê-los mantido, posso chamar de marxistas vulgares … O marxista vulgar médio acredita que o marxismo revela os segredos sinistros da vida social, revelando os motivos ocultos da ganância e do desejo por ganho material que acionam os poderes nos bastidores da história …
            -   378
        -   Assim como o objetivo final da revolução socialista não era apenas a eliminação do privilégio de classe econômica, mas da própria distinção de classe econômica, o objetivo final da revolução feminista deve ser [. . .] não apenas a eliminação do privilégio masculino, mas da própria distinção entre os sexos: a diferença genital entre os seres humanos não importaria mais culturalmente.
            -   385
    -   44

        -   O uso do conceito de transferência na psicoterapia levou, assim, a dois resultados diferentes. Por um lado, possibilitou ao analista trabalhar onde de outra forma não poderia ter trabalhado; por outro, expunha-o ao perigo de estar “errado” em relação ao paciente – e de abusar da relação analítica – sem que ninguém pudesse demonstrar isso a ele.
            -   346
        -   ...significa obedecer às convenções normais de sua disciplina, não disfarçar demais os dados, não deixar que suas esperanças e medos influenciem suas conclusões, a menos que essas esperanças e medos sejam compartilhados por todos aqueles que estão na mesma linha de trabalho, estando abertos à refutação pela experiência, não bloqueando o caminho da investigação.
            -   363
        -   Grande parte do meu trabalho nos últimos anos tem sido em defesa da objetividade, atacando ou contra-atacando posições subjetivistas. Para começar, devo deixar bem claro que não sou comportamentalista, e minha defesa da objetividade não tem nada a ver com qualquer negação de "métodos introspectivos" em psicologia.
            -   315
        -   O incidente foi, em parte, atribuído ao meu costume, sempre que sou convidado a falar em algum lugar, de tentar desenvolver algumas consequências de meus pontos de vista que espero que sejam inaceitáveis para o público específico. Pois acredito que há apenas uma desculpa para uma palestra: desafiar. Essa é a única maneira pela qual a fala pode ser melhor do que a escrita.
            -   375

    -   51
        -   [...] Aqueles que seguem a linha da ecologia profunda adoram acreditar nessas histórias apenas para repudiá-las em nome do selvagem que precedeu a Queda na cultura; assim como humanistas acreditam nelas para salvaguardar a cultura de invasões biológicas.
            -   252
    -   53
        -   Nossa alegação não é apenas que o TRF [hormônio] é cercado, influenciado por, em parte depende de, ou também é causado por circunstâncias; em vez disso, argumentamos que a ciência é inteiramente fabricada a partir das circunstâncias;
            -   233
