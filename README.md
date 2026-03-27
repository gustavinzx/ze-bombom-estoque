# 🍬 Zé Bombom — Sistema de Estoque

> **Marcha & Bombons · Est. 2025**  
> Sistema de distribuição de caixas de bombons com interface gráfica desktop.

---

## 📦 Sobre o projeto

O **Zé Bombom** é um sistema de estoque que calcula automaticamente como distribuir uma quantidade de bombons nas caixas disponíveis, priorizando sempre as maiores embalagens para minimizar desperdício.

O projeto nasceu como um script simples em Python e evoluiu para uma aplicação desktop com interface gráfica usando **Tkinter** — com mascote animado e tudo!

### Tamanhos de caixa suportados

| Caixa | Capacidade |
|-------|-----------|
| 📦 Grande | 30 bombons |
| 🗃️ Média | 10 bombons |
| 🧁 Pequena | 2 bombons |

---

## 🖥️ Arquivos

```
ze-bombom-estoque/
├── estoque.py      # versão original em terminal (script simples)
└── ze_bombom.py    # versão com interface gráfica Tkinter
```

---

## 🚀 Como usar

### Pré-requisitos

- Python 3.x instalado
- Tkinter (já vem incluso no Python padrão)

### Rodando a interface gráfica

```bash
python ze_bombom.py
```

### Rodando a versão terminal

```bash
python estoque.py
```

---

## ✨ Funcionalidades

- 🎨 Interface gráfica com identidade visual própria
- 🤖 Mascote **Zé Bombom** animado (balança, pisca e segura as caixinhas)
- 💬 Balão de fala com frases aleatórias a cada cálculo
- 📊 Cards individuais para cada tamanho de caixa
- 📈 Barra de resumo com total de caixas, bombons embalados e eficiência
- ⌨️ Suporte a tecla **Enter** para calcular rapidamente
- 🔄 Botão de nova consulta para resetar

---

## 🧠 Lógica de distribuição

```python
caixa_grandes  = total_bombons // 30
resto          = total_bombons % 30

caixas_medias  = resto // 10
resto          = resto % 10

caixas_pequenas = resto // 2
sobra_final     = resto % 2
```

O algoritmo usa divisão inteira (`//`) e resto (`%`) para encaixar o máximo de bombons nas caixas maiores primeiro, deixando o mínimo possível sem embalagem.

---

## 📸 Preview

```
┌─────────────────────────────────────┐
│  🍬  Zé Bombom                      │
│      MARCHA & BOMBONS · EST. 2025   │
│      [SISTEMA DE ESTOQUE OFICIAL]   │
│                                     │
│  Quantidade total de bombons:       │
│  [ 175        ] [ Calcular ]        │
│                                     │
│  📦 Grande     🗃️ Média             │
│  5 caixas      2 caixas             │
│                                     │
│  🧁 Pequena    Sem caixa            │
│  1 caixa       1 un.                │
│                                     │
│  Caixas: 8 | Embalados: 174 | 99%  │
└─────────────────────────────────────┘
```

---

## 🛠️ Tecnologias

- **Python 3**
- **Tkinter** — interface gráfica nativa
- **math** — animações do mascote
- **random** — frases aleatórias do Zé

---

## 👤 Autor

Feito com 🍫 por **Gustavo Silva dos Santos **  
Repositório: [github.com/gsds0/ze-bombom-estoque](https://github.com/gsds0)

---

*"Missão aceita: seus bombons, organizados!"* — Zé Bombom
