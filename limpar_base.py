import json

with open("base.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

with open("base.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)

print(f"Total de perguntas únicas: {len(dados)}")
