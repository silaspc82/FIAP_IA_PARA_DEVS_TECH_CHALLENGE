# TECH CHALLENGE - 1IADT - Fase 3

### Grupo 12
* Silas Pereira Costa - RM355822
* Wesley Gomes Santos - RM355677

### Definição do Problema
Executar o fine-tuning de um foundation model (Llama, BERT, MISTRAL etc.), utilizando o dataset "The AmazonTitles-1.3MM". O modelo treinado deverá:
   * Receber perguntas com um contexto obtido por meio do arquivo json “trn.json” que está contido dentro do dataset.
   * A partir do prompt formado pela pergunta do usuário sobre o título do produto, o modelo deverá gerar uma resposta baseada na pergunta do usuário trazendo como resultado do aprendizado do fine-tuning os dados da sua descrição.

### Fluxo de trabalho

### 1. Seleção Dataset:

O dataset selecionado foi o "The AmazonTitles-1.3MM" que contém mais de 1.3 milhões de exemplos de títulos de produtos da Amazon, além de informações relacionadas, como descrições e categorias dos produtos. A estrutura de dados principal segue o formato JSON, onde cada linha representa um produto e contém os seguintes campos:
   * uid: O código único que identifica o produto.
   * title: Um título curto que descreve o produto.
   * content: Um texto mais longo que fornece uma descrição completa.
   * target_ind: Listas de categorias que o produto se encaixa, representadas por números.
   * target_rel: Um valor de relevância (geralmente 1.0) que mostra o quanto o produto é relacionado a essas categorias.

Utilizaremos os campos title e content desse dataset para as executar as técnicas de fine-tuning, permitindo que o modelo, após o treinamento, possa gerar descrições de produtos com base no título fornecido.

### 2. Preparação do Dataset para Fine-Tunning:

Na preparação dos dados do Dataset foram realizadas os seguintes operações para limpeza, conversão e tratamento dos dados inválidos e duplicados no arquivo ***trn.json***:
   * Carregar um arquivo JSON contendo produtos com seus títulos e descrições.
   * Converter entidades HTML para caracteres normais.
   * Remover caracteres especiais indesejados dos títulos e descrições, mantendo apenas letras, números, vírgulas e pontos.
   * Filtrar dados inválidos (linhas com título ou descrição vazios).
   * Armazenar os dados limpos em uma lista de produtos.
   * Exclusão das linhas duplicadas

Por fim, dividimos o arquivo, quebrando em arquivos menores com 100.000 linhas para agilizar o processamento no treinamento do 
modelo.

partes menores para facilitar o processamento e o fine-tuning

### 2. Chamada do Foundation Model:
O modelo base selecionado para o treinamento foi LLaMA "unsloth/tinyllama-chat-bnb-4bit" e o tokenizer usando a biblioteca transformers. O tokenizer será responsável por tokenizar as perguntas e respostas para que o modelo possa processar.

Foi usado o módulo FastLanguageModel da biblioteca Unsloth para carregar o modelo base do Hugging Face e setando parâmetros iniciais.

A biblioteca FastLanguageModel é um módulo específico da Unsloth, projetada para otimizar o treinamento e a inferência de grandes modelos de linguagem. Ela facilita o fine-tuning de modelos como Llama e Mistral ao oferecer suporte para quantização de parâmetros e economia de memória, o que torna o processo mais rápido e eficiente.

### 3. Execução do Fine-Tuning:
Usando o módulo ***FastLanguageModel*** da biblioteca ***unsloth*** para carregar o modelo base do Hugging Face e setando parâmetros iniciais.

A biblioteca ***FastLanguageModel*** é um módulo específico da Unsloth, projetada para otimizar o treinamento e a inferência de grandes modelos de linguagem. Ela facilita o fine-tuning de modelos como Llama e Mistral ao oferecer suporte para quantização de parâmetros e economia de memória, o que torna o processo mais rápido e eficiente.

Aplicando o método ***LoRA*** (Low-Rank Adaptation) e ***PEFT*** (Parameter-Efficient Fine-Tuning), que permitem treinar modelos grandes com um número muito menor de parâmetros atualizados, acelerando o treinamento e diminuindo os requisitos de memória.

### 4. Geração de Respostas:

### Considerações Finais
Considerações Finais
* Modelo LLaMA: Por questões de licenciamento e acesso, é importante certificar-se de que você possui os direitos e permissões para baixar e utilizar o LLaMA.
* Treinamento: O tempo de treinamento pode variar muito dependendo do tamanho do dataset e dos recursos de hardware (idealmente, utilize GPUs ou TPUs).
* Aprimoramentos: Você pode ajustar os hiperparâmetros (taxa de aprendizado, batch size, etc.) para melhorar a performance.

 
