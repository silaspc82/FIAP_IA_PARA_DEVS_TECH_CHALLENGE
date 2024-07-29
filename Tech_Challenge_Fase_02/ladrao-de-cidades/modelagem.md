## Modelagem do Problema

### Gene: Cada cidade da rota

### Indivíduo: Rota (lembrando que começa e termina no mesmo lugar) Lista dos mercadosmas olhar só até onde a primeira repetir para ter um tamanho fixo de lista. Isso vai melhorar a mutação e etcetcetc)

Fitness
	(lembrando que temos tempo limite de 72h)
	Temos que restringir indivíduos com mais de 72h de viagem  e peso total > 20kg (-inf)
	Lucro (soma dos valores do roubo - custo de transporte)
	(prof falou que gosta de colocar as limitações no fitness)

Mutação
	muda dois itens aleatórios de lugar sem contar o primeiro item do array
	[E, x, y, u, a, E, o, p, a]
	também pode não colocar o primeiro E e, no fitness, calcular sabendo que começa em E
	desse jeito, a mutação não faz papel de ambiente

Crossover
	pega o menor indivíduo, divide pela metade.
	Esse valor é o tamanho do corte no segundo indivíduo
	faz o crossover

