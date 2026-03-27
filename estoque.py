total_bombons = int(input("Digite a quantidade total de bombons: "))

caixa_grandes = total_bombons // 30
resto = total_bombons % 30

caixas_medias = resto // 10
resto = resto % 10

caixas_pequenas = resto // 2
sobra_final = resto % 2


print(f"Caixas grandes (30 bombons): {caixa_grandes}")
print(f"Caixas médias (10 bombons): {caixas_medias}")
print(f"Caixas pequenas (2 bombons): {caixas_pequenas}")
print(f"bombons sem caixa: {sobra_final}")