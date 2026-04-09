# base_acidentes_trabalho.py
import requests
import pandas as pd
import io
import zipfile
import os
from time import sleep

# === Configurações ===
package_id = "e6219d53-5478-4143-bcb9-a922ee622eca"
url = f"https://dadosabertos.inss.gov.br/api/3/action/package_show?id={package_id}"

saida_dir = "resultados"
os.makedirs(saida_dir, exist_ok=True)
saida_csv = os.path.join(saida_dir, "acidentes_trabalho_tratado.csv")
saida_relatorio = os.path.join(saida_dir, "relatorio_qualidade.csv")

# === Função de leitura robusta de CSV ===
def try_read_csv_from_filelike(fobj):
    for enc in ("utf-8", "latin1"):
        for sep in (";", ","):
            try:
                fobj.seek(0)
            except Exception:
                pass
            try:
                df = pd.read_csv(fobj, sep=sep, encoding=enc, low_memory=False)
                return df
            except Exception:
                pass
    fobj.seek(0)
    return pd.read_csv(fobj, low_memory=False)

# === Busca de metadados ===
print("🔍 Buscando metadados do dataset...")
resp = requests.get(url, timeout=30)
resp.raise_for_status()
data = resp.json()

# Captura TODOS os formatos possíveis (CSV, ZIP, XLSX, XLS, XLTX)
resources = [
    r for r in data["result"]["resources"]
    if r.get("format") and any(ext in r["format"].lower() for ext in ("csv", "zip", "xlsx", "xls", "xltx"))
]

print(f"✅ Total de recursos considerados: {len(resources)}")

dfs = []
errors = []

# === Loop pelos arquivos ===
for idx, r in enumerate(resources, start=1):
    name = r.get("name", f"resource_{idx}")
    resource_url = r.get("url")
    fmt = r.get("format", "").lower()
    print(f"\n[{idx}/{len(resources)}] Processando: {name}  (format={fmt})")

    try:
        with requests.get(resource_url, stream=True, timeout=60) as rr:
            rr.raise_for_status()
            content = rr.content

        if resource_url.lower().endswith(".zip"):
            z = zipfile.ZipFile(io.BytesIO(content))
            csv_names = [n for n in z.namelist() if n.lower().endswith(".csv")]
            if not csv_names:
                raise ValueError(f"Nenhum CSV encontrado dentro do ZIP: {name}")
            csv_name = csv_names[0]
            print(f"   → ZIP detectado. Lendo membro: {csv_name}")
            with z.open(csv_name) as f:
                bio = io.BytesIO(f.read())
                df = try_read_csv_from_filelike(bio)

        elif resource_url.lower().endswith((".xlsx", ".xls", ".xltx")):
            print("   → XLSX/XLS detectado, tentando leitura")
            bio = io.BytesIO(content)
            # tenta ler a primeira aba
            try:
                df = pd.read_excel(bio, engine="openpyxl")
            except Exception:
                df = pd.read_excel(bio, sheet_name=0)

        else:
            print("   → CSV direto detectado, tentando leitura")
            bio = io.BytesIO(content)
            df = try_read_csv_from_filelike(bio)

        df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")

        for col in df.columns:
            col_upper = col.upper().replace(" ", "_").replace("-", "_").replace(".", "_")
            if "CNPJ" in col_upper or "CEI" in col_upper:
                df.rename(columns={col: "CNPJ_CEI_EMPREGADOR"}, inplace=True)

        if "CNPJ_CEI_EMPREGADOR" in df.columns:
            df["CNPJ_CEI_EMPREGADOR"] = (
                df["CNPJ_CEI_EMPREGADOR"]
                .astype(str)
                .str.replace(r"[^0-9]", "", regex=True)
                .str.zfill(14)
                .replace("00000000000000", pd.NA)
            )

        df["ORIGEM_ARQUIVO"] = name

        print(f"   ✅ Linhas lidas: {len(df):,} | Colunas: {len(df.columns)}")
        dfs.append(df)
        sleep(0.25)

    except Exception as e:
        msg = f"Erro ao processar '{name}': {e}"
        print("   ❌", msg)
        errors.append(msg)
        continue

# === Consolidação ===
if not dfs:
    raise RuntimeError("Nenhum arquivo foi lido com sucesso.")

print("\n🧩 Concatenando todos os dataframes (mantendo todas as colunas)...")
df_final = pd.concat(dfs, ignore_index=True, sort=False)

print("🔎 Limpeza final: remover duplicatas e espaços extras")
df_final.drop_duplicates(inplace=True)
df_final = df_final.map(lambda x: x.strip() if isinstance(x, str) else x)

# === Conversão de datas ===
for col in df_final.columns:
    if "DATA" in col:
        try:
            df_final[col] = pd.to_datetime(df_final[col], errors="coerce", dayfirst=True, format="mixed")
        except Exception:
            pass

# === Adiciona ANO_BASE ===
if "DATA_ACIDENTE" in df_final.columns:
    df_final["ANO_BASE"] = df_final["DATA_ACIDENTE"].dt.year

# === Filtrar apenas 2024 e 2025 ===
df_final = df_final[df_final["ANO_BASE"].isin([2024, 2025])]

# === Gera relatório de qualidade ===
print("📋 Gerando relatório de qualidade...")
relatorio = []
for col in df_final.columns:
    nulos = df_final[col].isna().sum()
    tipo = df_final[col].dtype
    perc_nulos = round((nulos / len(df_final)) * 100, 2)
    relatorio.append({"coluna": col, "tipo": tipo, "nulos": nulos, "perc_nulos": perc_nulos})

relatorio_df = pd.DataFrame(relatorio)
relatorio_df.to_csv(saida_relatorio, sep=";", index=False, encoding="utf-8-sig")

# === Salvar base final ===
df_final.to_csv(saida_csv, sep=";", index=False, encoding="utf-8-sig")

# === Verificar faixa de datas ===
if "DATA_ACIDENTE" in df_final.columns:
    min_data = df_final["DATA_ACIDENTE"].min()
    max_data = df_final["DATA_ACIDENTE"].max()
    print("\n📅 Faixa de datas carregadas:")
    print(min_data, "→", max_data)
    if pd.to_datetime("2025-12-31") > max_data:
        print("⚠️ Atenção: Dados de dezembro/2025 podem ainda não estar publicados ou com formato divergente.")

print(f"\n💾 Arquivo final salvo em: {saida_csv}")
print(f"📊 Total de linhas consolidadas: {len(df_final):,}")
print(f"📈 Relatório de qualidade salvo em: {saida_relatorio}")

if errors:
    print("\n⚠️ Recursos com erro:")
    for e in errors[:10]:
        print("-", e)