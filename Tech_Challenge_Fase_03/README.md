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

Por fim, dividimos o arquivo, quebrando em arquivos menores com 100.000 linhas para agilizar o processamento de fine-tuninng no treinamento do modelo.

### 2. Carregamento do Foundation Model:

O modelo base selecionado para o treinamento foi LLaMA "unsloth/tinyllama-chat-bnb-4bit" e o tokenizer usando a biblioteca transformers. O tokenizer será responsável por tokenizar as perguntas e respostas para que o modelo possa processar.

Usando o módulo ***FastLanguageModel*** da biblioteca ***Unsloth*** para carregar o modelo base do Hugging Face e setar os parâmetros iniciais:
* model_name: Nome do modelo pré-treinado a ser carregado (ex: “unsloth/Meta-Llama-3.1-8B-bnb-4bit”).
* max_seq_length: Comprimento máximo de tokens que o modelo pode processar (ex: 2048).
* load_in_4bit: Carrega o modelo quantizado em 4 bits, economizando memória e acelerando o processamento.
* lora_alpha: Controla a regularização do ajuste LoRA (Low-Rank Adaptation).
* lora_dropout: Taxa de dropout aplicada nas camadas LoRA, para evitar overfitting.
* target_modules: Define quais partes do modelo serão otimizadas com LoRA (ex: “q_proj”, “v_proj”).
* use_gradient_checkpointing: Ativa o checkpointing de gradiente para economizar memória durante o treinamento.
* dtype: Define o tipo de dado a ser usado nas operações do modelo (ex: float16, bfloat16).

A biblioteca ***FastLanguageModel*** é um módulo específico da Unsloth, projetada para otimizar o treinamento e a inferência de grandes modelos de linguagem. Ela facilita o fine-tuning de modelos como Llama e Mistral ao oferecer suporte para quantização de parâmetros e economia de memória, o que torna o processo mais rápido e eficiente.

### 3. Execução do Fine-Tuning:

Aplicando o método ***LoRA*** (Low-Rank Adaptation) e ***PEFT*** (Parameter-Efficient Fine-Tuning), que permitem treinar modelos grandes com um número muito menor de parâmetros atualizados, acelerando o treinamento e diminuindo os requisitos de memória.

O método FastLanguageModel.get_peft_model(...) é usado para aplicar PEFT (Parameter-Efficient Fine-Tuning) a grandes modelos de linguagem, como Llama. O PEFT permite que apenas uma pequena parte do modelo seja ajustada durante o fine-tuning, economizando tempo e memória, especialmente útil quando o modelo tem bilhões de parâmetros.

Principais recursos do PEFT:
* Simplifica o fine-tuning: Em vez de treinar todas as camadas de um modelo grande, o PEFT ajusta apenas parâmetros específicos, como aqueles nas camadas de projeção (q_proj, k_proj, etc.), tornando o processo mais eficiente.
* Economia de memória: Reduz o número de parâmetros ajustados, o que diminui a quantidade de memória necessária para o treinamento.
* ***LoRA*** (Low-Rank Adaptation): Essa técnica é aplicada dentro do ***PEFT*** para otimizar o ajuste de parâmetros, introduzindo “pequenas matrizes” em camadas específicas do modelo, como as camadas de atenção.

### 4. Geração de Respostas:

### Considerações Finais
Considerações Finais
* Treinamento: O tempo de treinamento pode variar muito dependendo do tamanho do dataset e dos recursos de hardware (idealmente, utilize GPUs ou TPUs).
* Aprimoramentos: Você pode ajustar os hiperparâmetros (taxa de aprendizado, batch size, etc.) para melhorar a performance.

 
