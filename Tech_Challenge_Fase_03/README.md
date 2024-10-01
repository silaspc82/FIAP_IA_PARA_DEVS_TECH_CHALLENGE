# TECH CHALLENGE - 1IADT - Fase 3

### Grupo 12
* Silas Pereira Costa - RM355822
* Wesley Gomes Santos - RM355677

### Definição do Problema
Executar o fine-tuning de um foundation model (Llama, BERT, MISTRAL etc.), utilizando o dataset "The AmazonTitles-1.3MM". O modelo treinado deverá:
   * Receber perguntas com um contexto obtido por meio do arquivo json “trn.json” que está contido dentro do dataset.
   * A partir do prompt formado pela pergunta do usuário sobre o título do produto, o modelo deverá gerar uma resposta baseada na pergunta do usuário trazendo como resultado do aprendizado do fine-tuning os dados da sua descrição.

### Fluxo de trabalho

### 1. Seleção e Preparação do Dataset para Fine-Tunning:
O dataset selecionado foi o "The AmazonTitles-1.3MM" que contém mais de 1.3 milhões de exemplos de títulos de produtos da Amazon, além de informações relacionadas, como descrições e categorias dos produtos. A estrutura de dados principal segue o formato JSON, onde cada linha representa um produto e contém os seguintes campos:
   * uid: O código único que identifica o produto.
   * title: Um título curto que descreve o produto.
   * content: Um texto mais longo que fornece uma descrição completa.
	* target_ind: Listas de categorias que o produto se encaixa, representadas por números.
	* target_rel: Um valor de relevância (geralmente 1.0) que mostra o quanto o produto é relacionado a essas categorias.

Utilizaremos esse dataset para as executar as técnicas de fine-tuning, permitindo que o modelo, após o treinamento, possa gerar descrições de produtos com base no título fornecido.

Na preparação dos dados do Dataset foram realizadas os seguintes tratamentos:
   * Carregar um arquivo JSON contendo produtos com seus títulos e descrições.
   * Converter entidades HTML para caracteres normais.
   * Remover caracteres especiais indesejados dos títulos e descrições, mantendo apenas letras, números, vírgulas e pontos.
   * Filtrar dados inválidos (linhas com título ou descrição vazios).
   * Armazenar os dados limpos em uma lista de produtos.

### 2. Chamada do Foundation Model:

### 3. Execução do Fine-Tuning:

### 4. Geração de Respostas:

 
