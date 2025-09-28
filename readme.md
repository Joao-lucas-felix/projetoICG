# Projeto de Introdução a computação grafica, Algoritmo do Pintor.  🎨

Este projeto implementa uma demonstração do **Algoritmo do Pintor (Painter’s Algorithm)** utilizando **Python** e **PyOpenGL**.  

O objetivo é visualizar como o algoritmo organiza e desenha polígonos no espaço 3D ordenando-os pela profundidade, simulando a ideia de “pintar” primeiro os objetos mais distantes e, em seguida, os mais próximos.

---

## 📖 O que é o Algoritmo do Pintor?
O **Algoritmo do Pintor** é uma técnica de renderização clássica em computação gráfica.  

- Ele funciona ordenando os polígonos de uma cena **pela profundidade (eixo Z da câmera)**.  
- Objetos mais distantes são desenhados primeiro.  
- Objetos mais próximos são desenhados por último, “cobrindo” o que está atrás, assim como um pintor adiciona camadas de tinta em uma tela.  

> ⚠️ **Limitações**: Não lida bem com **interseções complexas** (quando polígonos se cruzam). E não lida bem com **Grandes Numeros de Objetos** (precisa ordenar antes de poder reenderizar) nem com cenas com muitas mudanças.

---

## ⚙️ Dependências
Antes de rodar o projeto, instale os seguintes pacotes no Python (recomenda-se usar um ambiente virtual):

```bash
pip install PyOpenGL PyOpenGL_accelerate numpy
```

## ▶️ Como executar

Clone esse projeto.

```bash
git clone https://github.com/seu-usuario/painters-algorithm-demo.git
cd painters-algorithm-demo
```

Execute algum dos arquivos de teste.

```bash
python teste_2D.py
```

## 📂 Estrutura do Projeto
```bash
.
├── painter_algorithm.py   # Implementação do algoritmo do pintor
├── polygons.py            # Geração de polígonos 2D e 3D para testes
├── test_2D.py             # Arquivo de teste com cena com poligonos planos simples. (é um abiente 2D porém são objetos planos.)
├── test_2D_1k_polys.py    # Arquivo de teste com cena com 1000 poligonos planos.
├── test_2D_100k_polys.py  # Arquivo de teste com cena com 100.000 poligonos planos.
├── test_curva_spline.py  # Arquivo de teste com com movimento de camera através de curvas parametricas.
```

## 📊 Resultados e Desempenho

Durante os testes, o algoritmo apresentou o seguinte comportamento:

- ✅ Para **1.000 polígonos planos**, o tempo de renderização foi relativamente baixo, sendo suficiente para experimentos interativos.  
- ⚠️ Para **100.000 polígonos**, a aplicação já apresenta lentidão perceptível, dificultando a visualização em tempo real.  

### 🔍 Análise
O gargalo ocorre porque, antes da renderização, os polígonos precisam ser **ordenados pela profundidade média dos vértices**.  

Atualmente, o projeto utiliza a função `sort()` do Python, cuja complexidade é:  

\[
O(n \log n)
\]

Assim, o custo de ordenação cresce rapidamente conforme o número de polígonos aumenta:

- **1k polígonos** → ordenação ainda rápida  
- **100k polígonos** → ordenação custosa, afetando a taxa de frames  

### 📌 Considerações
- O **Painter’s Algorithm** não é a técnica mais eficiente para cenas grandes e complexas.  
- Técnicas modernas de renderização utilizam **Z-buffering**, que possui custo linear por fragmento e é implementado diretamente em hardware gráfico.  
- O código atual serve bem para fins **educacionais e experimentais**, mas não é recomendado para renderização em tempo real de cenas com grande número de polígonos.

---

## 📷 Prints dos Resultados

Abaixo estão alguns exemplos de execução do algoritmo em diferentes cenários:  

### Cena 2D simples  
![2D](https://github.com/Joao-lucas-felix/projetoICG/blob/master/prints/2D.png) 
*Visualização inicial de uma cena simples em 2D com polígonos planos.*  

---

### Cena com 1k polígonos  
![2D_1K](https://github.com/Joao-lucas-felix/projetoICG/blob/master/prints/2D_1K.png)  
*Mesmo com 1.000 polígonos, a renderização se mantém fluida, permitindo testes interativos.*  

---

### Cena com 100k polígonos  
![2D_100k](https://github.com/Joao-lucas-felix/projetoICG/blob/master/prints/2D_100k.png)  
*Com 100.000 polígonos, o algoritmo sofre lentidão perceptível devido ao custo da ordenação (O(n log n)).*  

---

### Movimento de câmera em curva spline  
![Curva_Spline](https://github.com/Joao-lucas-felix/projetoICG/blob/master/prints/Curva_Spline.gif)  
*Demonstração de movimentação suave da câmera usando curvas paramétricas (spline).*  

---

### Teste com luzes  
![Luzes](https://github.com/Joao-lucas-felix/projetoICG/blob/master/prints/luzes.gif)  
*Cena experimental com efeitos de luz, evidenciando a sobreposição de objetos e a estética do algoritmo.*  

