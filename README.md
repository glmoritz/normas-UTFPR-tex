# normas-UTFPR-tex

Modelo LaTeX para dissertações, teses e TCCs da UTFPR, ramo do PPGSE, com uma ferramenta que confere o trabalho contra as normas da UTFPR e da ABNT.

Baseado em [gbrante/normas-UTFPR-tex](https://github.com/gbrante/normas-UTFPR-tex/tree/ppgse-cc), o modelo indicado na página de [Procedimentos para defesa do PPGSE](https://www.utfpr.edu.br/cursos/programas-de-pos-graduacao/ppgse-ct/documentos/procedimentos-para-defesa).

## Usar o modelo

Arquivo principal: `modelo.tex`. Deixe os demais arquivos na mesma pasta para compilar corretamente.

Comece o trabalho por este modelo. A maior parte dos erros de formatação não aparece quando se parte dele.

## Conferir o trabalho antes de entregar

A pasta `.claude/skills/utfpr-norm-review` traz um *skill* do [Claude Code](https://claude.com/claude-code) que revisa o trabalho, corrige o que é seguro e gera um relatório em HTML com:

- as pendências no topo, dizendo o que fazer;
- o que foi resolvido, com a referência de cada item;
- cada alteração feita nos arquivos, com antes e depois.

O que ele confere: paginação e contagem de folhas, figuras e tabelas, citações e referências, resumo e abstract, identificação, licença Creative Commons, folha de aprovação, PDF/A e nome do arquivo.

### O que instalar

| Programa | Para quê |
|---|---|
| [Claude Code](https://claude.com/claude-code) | Roda o skill; precisa de conta |
| Python 3 | Scripts de conferência |
| poppler-utils (`pdftotext`, `pdfinfo`, `pdftohtml`) | Leitura do PDF |
| LaTeX com `latexmk` | Compilar o trabalho |
| Ghostscript | Converter para PDF/A |
| [veraPDF](https://verapdf.org/software/) | Validar o PDF/A |

No Ubuntu: `sudo apt install python3 poppler-utils latexmk ghostscript`. O veraPDF é instalado à parte. Se ele não estiver no `PATH`, indique o caminho com `VERAPDF=/caminho/verapdf`.

No Windows, use o WSL.

### Como usar

**Se o trabalho partiu deste repositório**, o skill já está na pasta. Abra o Claude Code nela e peça:

```
cd minha-dissertacao
claude
> Confere meu trabalho contra as normas da UTFPR. O PDF é dissertacao.pdf.
```

Também funciona com o comando `/utfpr-norm-review`.

**Se o trabalho está em outra pasta**, instale o skill para o seu usuário:

```
mkdir -p ~/.claude/skills
cp -r .claude/skills/utfpr-norm-review ~/.claude/skills/
```

**Se o trabalho está no Overleaf**, baixe o projeto (Menu > Download > Source) ou clone pelo Git, se o seu plano permitir. Inclua na pasta o PDF que será conferido.

### O que pedir

| Pedido | O que acontece |
|---|---|
| "Confere meu trabalho" | Revisa, aplica as correções seguras e gera o relatório |
| "Só me mostra o que corrigiria, não altere nada" | Testa as correções em uma cópia e entrega um patch |
| "Gera a versão final em PDF/A" | Converte, valida no veraPDF e sugere o nome do arquivo |

Tenha em mãos, se já existirem: a folha de aprovação emitida pelo Sistema Acadêmico, a licença escolhida e os dados de fomento.

### O que ele não faz

- Não inventa referências, fontes de figuras, datas ou nomes. O que não puder ser confirmado fica como pendência.
- Não faz commit nem push sem pedido.
- Não substitui a conferência do orientador nem a da biblioteca.
- Não inclui o texto das normas ABNT. As regras estão resumidas com o número da seção. A norma completa está no [GEDWeb](https://webapp.utfpr.edu.br/bibservices/gedWeb), com a conta da UTFPR.

Quando norma e prática divergem, o skill segue o que o modelo do PPGSE e trabalhos aceitos pela biblioteca fazem, e informa a diferença. A base ainda é pequena: dois trabalhos aceitos.

### Para orientadores

Copie `references/local.example.md` para `references/local.md` e coloque ali seus dados, como o número do processo de fomento. Esse arquivo não vai para o Git.

### Sem o Claude Code

Os scripts funcionam sozinhos, a partir desta pasta:

```
S=.claude/skills/utfpr-norm-review/scripts
python3 $S/check_tex.py .                          # configurações do projeto LaTeX
python3 $S/check_pdf.py dissertacao.pdf            # medições do PDF
bash $S/make_pdfa.sh dissertacao.pdf saida.pdf     # converte para PDF/A e valida
```

Para manter os links ao converter, inclua a opção `pdfa` no `\usepackage[...]{hyperref}`.

### Como ajudar

As regras ficam em `.claude/skills/utfpr-norm-review/references/`. Se a biblioteca devolver ou aceitar um trabalho por algo que o skill não previu, registre em `lessons.md`, ou em `precedents.md` no caso de um trabalho aceito, sem nomes de alunos.
