import os, csv, zipfile, pathlib, sys
from urllib.parse import urlparse
import requests

REFS = [
  ("Haraway_1988_Situated_Knowledges.pdf", "https://www.jstor.org/stable/3178066"),
  ("Harding_1991_Whose_Science_Whose_Knowledge.html", "https://cornellpress.cornell.edu/book/9780801497469/whose-science-whose-knowledge/"),
  ("Collins_2000_Black_Feminist_Thought.html", "https://www.routledge.com/Black-Feminist-Thought/Collins/p/book/9780415924840"),
  ("Bourdieu_1984_Distinction.html", "https://www.hup.harvard.edu/books/9780674212774"),
  ("Bourdieu_1986_Forms_of_Capital.pdf", "https://www.socialcapitalgateway.org/sites/socialcapitalgateway.org/files/data/paper/2016/04/18/rbasicsbourdieu1986-theformsofcapital.pdf"),
  ("Ceci_Williams_2011_PNAS_Understanding_Causes.pdf", "https://www.pnas.org/doi/10.1073/pnas.1014871108"),
  ("MossRacusin_2012_PNAS_Gender_Bias.pdf", "https://www.pnas.org/doi/10.1073/pnas.1211286109"),
  ("Xie_Shauman_2003_Women_in_Science.html", "https://www.hup.harvard.edu/books/9780674018581"),
  ("Merton_1968_Matthew_Effect.pdf", "https://www.science.org/doi/10.1126/science.159.3810.56"),
  ("Clauset_Arbesman_Larremore_2015_SciAdv_Faculty_Hiring.pdf", "https://www.science.org/doi/10.1126/sciadv.1400005"),
  ("ERIC_2024_Policy_Article.pdf", "https://files.eric.ed.gov/fulltext/EJ1425602.pdf"),
  ("TuningJournal_1920.pdf", "https://tuningjournal.org/article/view/1920/2146"),
  ("DIPRES_Informe_Final.pdf", "https://www.dipres.gob.cl/597/articles-163122_informe_final.pdf"),
  ("Doing_Global_Sociology_2024.html", "https://global-qualitative-sociology.net/2024/09/10/doing-global-sociology/"),
  ("Redalyc_Art_14069725011.html", "https://www.redalyc.org/journal/140/14069725011/html/"),
  ("BCN_BecasChile_Cumplimiento.pdf", "https://obtienearchivo.bcn.cl/obtienearchivo?id=repositorio%2F10221%2F37318%2F1%2FBCN___Becas_Chile_Estado_de_cumplimiento_obligaciones_y_retribucion.pdf"),
  ("CONICYT_2016_Becas_Doctorado_Extranjero.html", "https://www.conicyt.cl/becasconicyt/2016/01/13/becas-doctorado-en-el-extranjero-bch-2016/"),
  ("arXiv_2205_01833.pdf", "https://arxiv.org/pdf/2205.01833.pdf"),
  ("ACM_2019_Knowledge_Graphs_Chapter.pdf", "https://dl.acm.org/doi/pdf/10.1007/978-3-030-30796-7_8"),
]

OUTDIR = "referencias_raw"
ZIPNAME = "referencias.zip"
os.makedirs(OUTDIR, exist_ok=True)

def fetch(url, path):
    try:
        r = requests.get(url, allow_redirects=True, timeout=60)
        r.raise_for_status()
        ct = r.headers.get("Content-Type","").lower()
        if path.suffix.lower()==".pdf" and "pdf" not in ct:
            # si no es PDF real, guarda HTML
            path = path.with_suffix(".html")
        path.write_bytes(r.content)
        print(f"↳ guardado {path.name}")
        return path.name
    except Exception as e:
        print(f"   ! fallo: {url} -> {e}")
        return None

manifest_rows = []
for fname, url in REFS:
    saved = fetch(url, pathlib.Path(OUTDIR)/fname)
    if saved:
        manifest_rows.append((fname, url))

with open(os.path.join(OUTDIR,"manifest.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["filename","url"])
    w.writerows(manifest_rows)

with zipfile.ZipFile(ZIPNAME, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(OUTDIR):
        for fn in files:
            p = pathlib.Path(root)/fn
            z.write(p, arcname=str(p.relative_to(OUTDIR)))
print(f"✔ Hecho: {ZIPNAME}")
