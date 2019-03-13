# Avaliação do algoritmo genético e recozimento simulado na função de Rastrigin


## Introdução
Na matemática existe um conjunto de problemas denominados NP-Completo.  
Esses problemas possuem as seguintes características: sua solução pode ser verificada em tempo polinomial, não existe uma solução polinomial conhecida. No entanto Na ciência da computação existem a chamada meta-heurísticas que são algoritmos que ou possuem um tempo de execução aceitável ou garante ser a solução ótima ou suficientemente boa para resolver o problema. È nesse contexto que o algoritmo genético e recozimento simulado se localiza. O algoritimo genético foi criado pro John Holland (1973)[holland1973genetic]. Mas foi popularizado apenas no anos 80[satoru]. Por isso é encontrado inumeras aplicações como: [leite2006aplicaccao] um problema complexo, de grande porte, composto por várias usinas interligadas e pertencentes a diferentes cascatas. Mas devido à sua simplicidade, paralelismo e generalidade, os Algoritmos Genéticos apresentam um grande potencial para a resolução do problema.[moori2010aplicaccao],nesse artigo o algoritmo genético foi utilizado omo instrumento de tomada decisão para a gestão de suprimentos. O objetivo foi avaliar a sua utilização para a redução de estoques correntes. O resultado mostrou que a política de suprimentos simulada pelo algoritmo genético reduziu o estoque de pneus em cerca de 78%. Desse resultado pode-se concluir que o algoritmo genético proporciona importante contribuição para a gestão de suprimentos. já o Recozimento simulado foi desenvolvido por Kirkpatrick, Gelatt e Vecchi em 1983[kirkpatrick1983optimization]. O recozimento simulado já foi aplicado em diferentes situações como: [nascimento2005aplicaccao], onde o Recozimento simulado foi utilizado para fornecer uma solução Problema de Alocação de Salas. Um problema NP-difícil. Os resoltados foram satisfatórios em comparação com outros estudos da área. [vivan2010aplicaccao] onde o recozimento simulado foi utizado para resolver um problema real de programação e sequenciamento da produção. Os resultados mostraram que o recozimento simulado mostrou-se eficiente e eficaz quando a sua utilização e em termos de desempenho, o método respondeu de forma satisfatória nas
questões de proximidade a solução ótima.
Nesse trabalho foi realizado uma avaliação de desempenho entre o algoritmo genético e recozimento simulado utilizando. Com a finalidade de reconhecer os prós e contras dos algoritmos.

## Abordagem Teórica
Nesse relatório foram utilizadas as duas técnicas: algoritmo genético, recozimento simulado. Esse tópico foi divido em duas partes, a primeira descreverá  
o algoritmo genético e o segundo o recozimento simulado.
### Algoritmo Genético
O algoritimo génetico surgiu e em 1973 por john Holland[holland1973genetic]. È uma técnica de busca utilizada na ciência da computação para achar soluções aproximadas em problemas de otimização e busca. Algoritmos genéticos são uma classe particular de algoritmos evolutivos que usam técnicas inspiradas pela biologia evolutiva como hereditariedade, mutação, seleção natural e recombinação.
Algoritmos genéticos diferem dos algoritmos tradicionais de otimização em basicamente quatro aspectos:
- Baseiam-se em uma codificação do conjunto das soluções possíveis, e não nos parâmetros da otimização em si;
- os resultados são apresentados como uma população de soluções e não como uma solução única;  
- não necessitam de nenhum conhecimento derivado do problema, apenas de uma forma de avaliação do resultado;
- usam transições probabilísticas e não regras determinísticas.
[wiki:algoritimogenetico]

```
input: population_size, fitness_function 

```