# TECH CHALLENGE - 1IADT - Fase 4

### Grupo 12
* Silas Pereira Costa - RM355822
* Wesley Gomes Santos - RM355677

## COMPUTER VISION

O objetivo deste estudo é realizar o reconhecimento facial em um video analisando as expressões faciais para detenção emocionais e descrever as atividades realizadas pelas pessoas identificadas durante a execução do video.

Foram utilizadas as bibliotecas:
* **<ins>OpenCV</ins>** para manipular os frames do video e gerar o video de resultado após o processamento
* **<ins>MediaPipe</ins>** para detecção dos rotos, gestos e movimentos
* **<ins>DeepFace</ins>** para reconhecer as emoções no rostos detectados
* **<ins>FaceRecognition</ins>** identificar os rotos e comparar com uma base de imagens para reconhecimento


## Fluxo do trabalho

### 1. Reconhecimento facial: 
* Identifique e marque os rostos presentes no vídeo.

### 2. Análise de expressões emocionais: 
* Analise as expressões emocionais dos rostos identificados.

### 3. Detecção de atividades: 
* Detecte e categorize as atividades sendo realizadas no vídeo.

### 4. Geração de resumo:
* Crie um resumo automático das principais atividades e emoções detectadas no vídeo.

## Considerações Finais
Foi possível detectar os rostos, procurar em um arquivo de fotos, idenficando os respectivos nomes das pessoas reconhecidas no video. Também foram identificados gestos e movimentos, bem como as emoções dos rostos mapeados. Exceção daqueles rostos com visualização parcial ou angulo que não permitia o mapeamento.

Conteúdo da pasta "arquivos":
* "Unlocking Facial Recognition_ Diverse Activities Analysis.mp4"
    Arquivo de entrada utilizado para o processo de computer vision.

* "output_detection_and_recognition_Unlocking Facial Recognition_ Diverse Activities Analysis.mp4":
    Arquivo de saída do processamento de computer vision.
    Contém as marcações do reconhecimento facial, expressões, movimentos e gestos.
    
* "relatorio_saida.txt":
    Arquivo contendo o resumo do processamento. 
    Nele contém as descrições do processamento de reconhecimento facial, expressões, movimentos e gestos.

Conteúdo da pasta "images":
* Contém as imagens de rostos utilizados para processamento do vídeo
