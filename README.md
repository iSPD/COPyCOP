# 🖥️ COPyCOP

- 공모전 표절, 도용 검증을 위한, 이미지, 텍스트 유사도 분석 AI 솔루션

  - **ImageCOP**
  - **TextCOP**

<div align="center">
<img width="30%" src="https://github.com/iSPD/COPyCOP/blob/main/images/%EA%B5%AC%EC%84%B1%EB%8F%84.png"/>

**<그림 3. COPyCOP 구성도>**
</div>

---

## 🕰️ **개발 기간**

- 2022년 4월 1일 ~ 2022년 10월 31일

---

## ⚙️ **개발 환경** 

-	CPU : Ubuntu 20.04.3 LTS

-	GPU : 지포스 RTX 3090 D6 24GB

  (Driver Version : 470.103.01, Cuda : 11.1, Cudnn : 8.2.1)
  
---

## ⚙️ **개발 언어** 

-	`Python 3.7.x`

---

## **ImageCOP** 
객체 추적 인식 AI 모델의 다중 적용 및 VGG19 벡터 비교를 통한 이미지 표절 검출 및 검출 오류 보정

### **개발 라이브러리** 

-	Tensorflow 2.8

-	Tensorflow_hub

-	Opencv

-	Torchvision

-	Keras


### **사용 알고리즘**

-	`Objcet Detection`(tensorflow, Mobilenet V3)

-	`Image Classification`(tensorflow, mobilenet_v3_large_100_244)

-	`Feature extraction`(tensorflow_hub, vgg19-block5-con2-unpooling-encoder)

-	`Spearmanr`(opencv)

---

### **개발 내용**

**1.	이미지 데이터 가공**

-	공모전 이미지 데이터 가공(1장 당 82개 가공 이미지 생성)

-	공모전 이미지를 Torchvision 라이브러리를 이용하여 Padding, Resize, Crop, Transforms, Blur, Rotation, Sharpness 등을 적용.

<div align="center">
<img width="80%" src="https://github.com/iSPD/COPyCOP/blob/main/images/%EA%B0%80%EA%B3%B5.png"/>
 
**<그림 1. 82개로 가공한 사진>>**
</div>
 
**2.	이미지 트레이닝**

-	Tensorflow_hub, Tf.kera 라이브러리를 이용하여, mobilenet_v3_large_100_244 모델 로딩 후, 100개의 클래스 씩 트레이닝(100개 클래스 모델 x N)

-	`Validation Dataset` : 15%

-	`Learning Rate` : 0.001 ~ 0.0001

-	`loss함수` : CategoricalCorssentropy(멀티클래스)

-	`기본 Epoch` : 50

-	`EarlyStopping 적용` : Epoch의 10%동안 Loss율이 변화가 없으면 종료, 대략 20Epoch에서 종료

-	`트레이닝 속도` : 지포스 RTX 3090 D6 24GB기준 20분 내외

**3.	이미지 특징 추출(Feature Extraction)**

-	Tensorflow_hub 라이브러리를 이용하여 Vgg19-block5-conv2-unpooling-encoder모델을 로딩하여, 공모작 이미지 1장당 100, 352개의 이미지 특징 추출(Image Feature Vecror)하여  Vector 값 및 Tagging(공모작 명).

-	`Infernece Time` : 1장당 5ms

<div align="center">
<img width="80%" src="https://github.com/iSPD/COPyCOP/blob/main/images/encoder.png?raw=true"/>
 
**<그림 2. Vgg19-block5-conv2-unpooling-encoder>**
</div>
 
**4. 이미지 비교(Inference)**

->	`신청작 이미지를 아래의 모델에서 추론(Inference)`

-   **Object Detection** : tensorflow 2.x 라이브러를 이용하여 Mobilenet v3 Object Detection모델을 로딩 후, Confidence Rate을 0으로 설정 후 여러 개의 Detection 박스 중  Core+Size 기준 1개를 선정. 선정된 영역을 Crop
  
-	**Image Classification** : Crop된 이미지를 트레이닝 된 N개의 mobilenet_v3_large_100_244 모델에 신청작 이미지를 추론하여 각각 모델에서 Score가 가장 높은 사진 추출

-	**Image Feature Extraction** : Vgg19-block5-conv2-unpooling-encoder에 신청작 이미지의 Feature Vector를 추출. 미리 추출된 수상작의 Feature Vector들과 Spearmanr알고리즘을  이용하여 절대수치를 산정 후, 기준 수치 이상의 사진 추출
  
---

### **사용 방법**
- Contact : ispd_daniel@outlook.kr(김경훈)
  
---
  
## **TextCOP** 
doc2vec 모델을 활용한 한국어 텍스트 표절 검출, TF-IDF 알고리즘으로 텍스트 유사도 오류 보정
  
### **요구 사항(Dependency)**
-	gensim

-	nltk

-	scikit-learn
  
### **개발 모듈**
- Sentence Pre-Processing
  
  - 각 문장의 글자가 아닌 요소들을 제거한 정제된 문장 형태로 변환. 
  
  - 수상작을 문장 단위로 쪼개어 ID를 부여. 
  
  - 10만 문장 초과시 다수의 모델로 분할하기 위해 모델별로 고유ID 부여.
  
  - ID, 정제된문장 쌍으로 구성된 데이터를 doc2vec 모델 생성을 위한 Training Dataset으로 사용.
  
  <div align="center">
  <img width="60%" src="https://github.com/iSPD/COPyCOP/blob/main/images/text-preprocess.JPG"/>
  <br><그림 1. doc2vec 모델을 위한 pre-precessing 적용>
  </div>
- Sentence Similarity
    
  - doc2vec 을 활용하여 Pre-Processing을 거친 문장들을 10만 문장 단위로 training, 생성한 모델파일에 표절 의심 문장을 입력하여 문장 유사도를 측정, 대상 문장의 ID를 출력
    
- Word Similarity
  
    - doc2vec을 거친 테스트 문장과 대상 문장을 맞춤법 교정
    
    - 전처리 - 형태소별 분리, 조사 제거
    
    - TF-IDF 로 입력하여 vectorization 후 단어 유사도를 측정

  <div align="center">
  <img width="80%" src="https://github.com/iSPD/COPyCOP/blob/main/images/tfidf.jpg"/>
  <br><표 1. doc2vec 오류보정을 위한 TF-IDF 단어유사도 측정>
  </div>
    
### **텍스트 표절 유사도 AI 솔루션 테스트**
    
- 학습 데이터셋
  
  위키피디아, 언론사 공모전 수상작의 내용을 무작위 추출 후 Pre-Processing을 거쳐 10만 문장 단위로 ID + 정제된 문장셋을 생성
  
- 학습
  
  Pre-Processing을 거친 문장들을 10만 문장 단위로 Training & 모델 생성
    ```Python
    max_epochs = 5000
    vec_size = 100
    alpha = 0.025

    model = Doc2Vec(tagged_data,vector_size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=4,
                    dm=1,window=10,epochs=max_epochs)
    ```
- 테스트 데이터셋
  
  학습 데이터셋 중 무작위로 M개 문장 추출 후 100%표절, 1 ~ N개 단어 제거, 1 ~ N개 단어 교체 방법으로 변형 후 파일에 저장 및 정답 파일에 해당 ID 기록하여 테스트 데이터셋 구축 진행 
  
- 테스트
  
  테스트 파일을 doc2vec 모델과 TF-IDF에 입력하여 문장 유사도, 단어 유사도를 측정 후 두 수치의 평균값이 일정 기준 이상일 때 표절 의심으로 판정
  
  
