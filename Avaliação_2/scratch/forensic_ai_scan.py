import fitz
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_files = glob.glob(os.path.join(r"c:\Users\jsous\Desktop\Redes 2\Avaliação_2", "*.pdf"))
if not pdf_files:
    print("Nenhum PDF encontrado!")
    sys.exit(1)

pdf_path = pdf_files[0]
doc = fitz.open(pdf_path)

print(f"Arquivo analisado: {pdf_path}")
print(f"Total de páginas: {len(doc)}\n")

print("="*75)
print("1. METADADOS E PROPRIEDADES DO PDF")
print("="*75)
for k, v in doc.metadata.items():
    print(f"  {k}: {v}")

print("\n" + "="*75)
print("2. ANÁLISE DE CAMADAS, ANOTAÇÕES E JAVASCRIPT")
print("="*75)
for i, page in enumerate(doc):
    annots = list(page.annots())
    if annots:
        print(f"  Página {i+1}: {len(annots)} anotações encontradas.")
        for a in annots:
            print(f"    Tipo: {a.type}, Conteúdo: {a.info}")

js_list = doc.embfile_names()
if js_list:
    print(f"  Arquivos embutidos encontrados: {js_list}")
else:
    print("  Nenhum arquivo embutido ou script JavaScript detectado.")

print("\n" + "="*75)
print("3. BUSCA TEXTUAL DIRETA DE TERMOS RELACIONADOS A IA E PLÁGIO")
print("="*75)
keywords = [
    "inteligência", "inteligencia", "artificial", "sintétic", "sintetic",
    "plágio", "plagio", "similaridade", "detector", "turnitin", "copyspider",
    "gpt", "chatgpt", "llm", "claude", "gemini", "copilot", "prompt",
    "automação", "gerad", "robô", "watermark", "marca d'água"
]

found_terms = {}
for i, page in enumerate(doc):
    text = page.get_text()
    for kw in keywords:
        matches = [line.strip() for line in text.split("\n") if kw in line.lower()]
        if matches:
            for m in matches:
                found_terms.setdefault((i+1, kw), []).append(m)

if found_terms:
    for (page_num, kw), lines in sorted(found_terms.items()):
        print(f"  [Página {page_num:02d} | Palavra-chave: '{kw}']")
        for l in set(lines):
            print(f"    --> {l}")
else:
    print("  Nenhum termo explícito de IA encontrado.")

print("\n" + "="*75)
print("4. ANÁLISE FORENSE DE TEXTO OCULTO, MICRO-FONTES, CORES E UNICODE INVISÍVEL")
print("="*75)
hidden_anomalies = []

for i, page in enumerate(doc):
    rect = page.rect
    blocks = page.get_text("rawdict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for line in b["lines"]:
                for s in line["spans"]:
                    if "text" not in s:
                        continue
                    text = s["text"]
                    size = s.get("size", 12)
                    color = s.get("color", 0)
                    bbox = s.get("bbox", [0, 0, 0, 0])
                    flags = s.get("flags", 0)

                    # 1. Caracteres Unicode Invisíveis / Zero-width
                    invisibles = [c for c in text if ord(c) in [0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0xFEFF]]
                    if invisibles:
                        hidden_anomalies.append(
                            f"Página {i+1}: Caractere invisível/zero-width {[hex(ord(c)) for c in invisibles]} em '{text}'"
                        )

                    # 2. Micro-texto (font size < 3pt)
                    if size < 3.0:
                        hidden_anomalies.append(
                            f"Página {i+1}: Microfonte suspeita (size={size:.2f}pt) em '{text}'"
                        )

                    # 3. Texto com cor branca ou transparente (0xFFFFFF / 16777215)
                    if color in [0xFFFFFF, 16777215]:
                        hidden_anomalies.append(
                            f"Página {i+1}: Texto em cor branca (invisível em fundo branco): '{text}'"
                        )

                    # 4. Texto renderizado fora da área visível da página
                    if bbox[2] < 0 or bbox[0] > rect.width or bbox[3] < 0 or bbox[1] > rect.height:
                        hidden_anomalies.append(
                            f"Página {i+1}: Texto fora dos limites da página: '{text}'"
                        )

if hidden_anomalies:
    print(f"  ⚠️ FORAM DETECTADAS {len(hidden_anomalies)} ANOMALIAS:")
    for a in hidden_anomalies:
        print(f"    - {a}")
else:
    print("  ✅ Nenhuma anomalia forense detectada (sem micro-textos, sem texto branco, sem zero-width spaces e sem texto fora da página).")

print("\n" + "="*75)
print("5. ANÁLISE ESPECÍFICA DA SEÇÃO DE INTEGRIDADE ACADÊMICA (PÁGINA 11)")
print("="*75)
p11_text = doc[10].get_text()
for line in p11_text.split("\n"):
    if any(term in line.lower() for term in ["plágio", "plagio", "integridade", "similaridade", "sintética", "sintetica", "zero", "equipe"]):
        print(f"  {line}")
