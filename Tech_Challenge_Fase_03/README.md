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

Após aplicar o PEFT e LoRA, preparamos o processamento de prompts para treinar um modelo de linguagem com base em um dataset de produtos.
1. Define um template de prompt (alpaca_prompt):
2. Um template onde a instrução, o título do produto (input), e sua descrição (output) são organizados.
3. O template segue o formato:
 
    ### Instruction:
    {Instrução}
    
    ### Input:
    {Título}
    
    ### Response:
    {Descrição}
 
 4. Função formatting_prompts_func:
    * Pega as colunas do dataset (instruction, title, content) e preenche o template alpaca_prompt.
    * Gera uma string formatada para cada exemplo no dataset e adiciona o token de fim de sequência (EOS_TOKEN) para indicar que a geração de texto deve parar.
 5. Função add_instruction_column:
    * Adiciona uma coluna de instrução ao dataset, fixando o valor da instrução como “Describe the product” para todos os exemplos.
 6. Carregamento e mapeamento do dataset:
    * O dataset é carregado usando a função load_dataset, e depois a função add_instruction_column é aplicada para adicionar as instruções.
    * A função formatting_prompts_func é aplicada para formatar os prompts em um novo campo chamado "text".

Esse código utiliza a biblioteca SFTTrainer (Supervised Fine-Tuning Trainer) para realizar o fine-tuning de um modelo de linguagem com um dataset específico. O objetivo é ajustar o modelo para uma tarefa com um conjunto de dados supervisionados, configurando parâmetros importantes para o treinamento.

Explicação do Código:
1.	Importações:
	* SFTTrainer: Responsável por treinar o modelo com supervisão (fine-tuning supervisionado).
	* TrainingArguments: Define os argumentos e hiperparâmetros do treinamento.
	* is_bfloat16_supported: Verifica se o hardware suporta o formato de ponto flutuante bfloat16 (para melhor eficiência de memória).
2.	Configuração do Trainer (SFTTrainer):
	* model: O modelo que será ajustado (fine-tuned).
	* tokenizer: O tokenizador que converte o texto em tensores.
	* train_dataset: O dataset que será usado para o treinamento.
	* dataset_text_field: A coluna do dataset que contém o texto para treinar.
	* max_seq_length: Comprimento máximo das sequências de entrada.
	* dataset_num_proc: Número de processos paralelos usados para preparar o dataset.
	* packing: Define se o dataset deve ser “compactado”, o que pode acelerar o treinamento para sequências curtas (desativado aqui).
3.	Configuração dos Argumentos de Treinamento (TrainingArguments):
	* per_device_train_batch_size = 2: Tamanho do lote por dispositivo (GPU ou CPU).
	* gradient_accumulation_steps = 22: Acumula os gradientes por 22 passos antes de atualizar os pesos, o que permite simular um tamanho de lote maior com menos memória.
	* warmup_steps = 5: Passos iniciais para o agendamento do aprendizado, ajudando a estabilizar o treinamento.
	* num_train_epochs = 1: Define uma época completa para o treinamento.
	* learning_rate = 2e-4: Taxa de aprendizado, que controla o quão rápido o modelo ajusta seus parâmetros.
	* fp16/bf16: Define o uso de float16 ou bfloat16 dependendo do suporte de hardware, para economizar memória.
	* max_grad_norm = 0.6: Limita o tamanho dos gradientes para evitar explosões de gradientes.
	* optim = "adamw_8bit": Otimizador AdamW com quantização de 8 bits para economizar memória.
	* weight_decay = 0.01: Regularização dos pesos para evitar overfitting.
	* lr_scheduler_type = "linear": Usa um agendador linear para a taxa de aprendizado.
	* group_by_length = True: Agrupa sequências de entrada por comprimento, o que pode melhorar a eficiência do treinamento.

Resumo:

Esse código configura e executa o fine-tuning de um modelo de linguagem utilizando a biblioteca SFTTrainer, ajustando parâmetros como taxa de aprendizado, acumulação de gradientes, e uso de memória otimizado (com bfloat16 ou fp16, e otimizador adamw_8bit). O objetivo é ajustar o modelo de forma eficiente, mesmo em hardware com recursos limitados, enquanto mantém a performance alta.


### 4. Geração de Respostas:
Realizando Inferência
utilizado para gerar texto com um modelo de linguagem treinado, como Llama, utilizando o FastLanguageModel para acelerar a inferência. Vamos dividi-lo em partes:
	1.	FastLanguageModel.for_inference(model):
	* Ativa o modo de inferência otimizado, que é até 2x mais rápido.
	2.	Preparação dos inputs:
	* O tokenizer é usado para converter um prompt em tensores que o modelo pode entender.
	* O prompt é construído usando o formato alpaca_prompt, com uma instrução (“Describe the product”) e o título do produto (“Nice for Mice”).
	* O campo output é deixado em branco porque o modelo vai gerar esse conteúdo.
	* O tokenizer converte o texto em tensores PyTorch (return_tensors = "pt") e envia para a GPU (to("cuda")).
	3.	Geração de texto:
	* O modelo gera a continuação do texto com até 128 novos tokens, usando a função generate.
	* TextStreamer é usado para exibir o texto gerado em tempo real enquanto o modelo o produz.

Explicação Simples:
	* Entrada: O modelo recebe um prompt com uma instrução (“Descreva o produto”) e o nome do produto (“Nice for Mice”).
	* Inferência: O modelo usa esse prompt para gerar uma descrição do produto, fazendo a geração em tempo real e exibindo o resultado enquanto é produzido.

Esse código exemplifica o fluxo básico de gerar uma resposta automática de um modelo treinado, usando técnicas otimizadas para inferência mais rápida e eficiente em hardware como GPUs.


### Considerações Finais

O tempo de treinamento de um modelo de IA é influenciado por diversos fatores, incluindo o tamanho do dataset, o número de épocas, o tamanho do batch e a complexidade do modelo. A relação entre esses fatores não é linear, e a Lei de Amdahl limita a aceleração obtida com mais recursos computacionais. Além disso, o tipo de dados e sua representação podem impactar significativamente o tempo de treinamento.

O uso de GPUs é altamente recomendado para o treinamento de modelos de IA devido à sua capacidade de realizar cálculos em paralelo. No entanto, a escolha da GPU ideal depende do tamanho do modelo e do dataset. A quantidade de memória da GPU e o tipo de cálculo a serem realizados são fatores importantes a serem considerados. Outros aceleradores, como TPUs, podem oferecer ainda mais performance para tarefas específicas.

O ajuste fino dos hiperparâmetros é crucial para obter um bom desempenho do modelo, e a validação cruzada é uma técnica fundamental para evitar overfitting. Técnicas como quantização, transfer learning e o uso de frameworks de deep learning otimizados podem ajudar a reduzir o tempo de treinamento e melhorar a performance do modelo.