# COPyCOP

<b>COPyCOP</b> : 공모전 표절, 도용 검증을 위한, 이미지, 텍스트 유사도 분석 AI 솔루션
<br><b>개발 환경</b> : 
<br>-	CPU : Ubuntu 20.04.3 LTS
<br>-	GPU : 지포스 RTX 3090 D6 24GB, 
<br>(Driver Version : 470.103.01, Cuda : 11.1, Cudnn : 8.2.1)
<br>개발 언어 : 
<br>-	Python 3.7.x
<br>개발 라이브러리 : 
<br>-	Tensorflow 2.8
<br>-	Tensorflow_hub
<br>-	Opencv
<br>-	Torchvision
<br>-	Keras
<br>사용 알고리즘
<br>-	Objcet Detection
<br>-	(tensorflow, Mobilenet V3)
<br>-	Image Classification
<br>(tensorflow, mobilenet_v3_large_100_244)
<br>-	Feature extraction
<br>(tensorflow_hub, vgg19-block5-con2-unpooling-encoder)
<br>-	Spearmanr(opencv)
<br>이미지 개발 내용
<br><br>1.	이미지 데이터 가공
<br>-	공모전 이미지 데이터 가공(1장 당 82개 가공 이미지 생성)
<br>-	공모전 이미지를 Torchvision 라이브러리를 이용하여 Padding, Resize, Crop, Transforms, Blur, Rotation, Sharpness 등을 적용.
<br><82개로 가공한 사진>
<br><img width="80%" src="https://github.com/iSPD/COPyCOP/blob/main/images/%EA%B0%80%EA%B3%B5.png"/>
 
<br>2.	이미지 트레이닝
<br>-	Tensorflow_hub, Tf.kera 라이브러리를 이용하여, mobilenet_v3_large_100_244 모델 로딩 후, 100개의 클래스 씩 트레이닝(100개 클래스 모델 x N)
<br>-	Validation Dataset : 15%
<br>-	Learning Rate : 0.0001
<br>-	loss함수 : CategoricalCorssentropy(멀티클래스)
<br>-	기본 Epoch : 50
<br>-	EarlyStopping 적용 : Epoch의 10%동안 Loss율이 변화가 없으면 종료, 대략 20Epoch에서 종료
<br>-	트레이닝 속도 : 지포스 RTX 3090 D6 24GB기준 20분 내외

<br>3.	이미지 특징 추출(Feature Extraction)
<br>-	Tensorflow_hub 라이브러리를 이용하여
<br>Vgg19-block5-conv2-unpooling-encoder모델을 로딩하여, 공모작 이미지 
<br>1장당 100, 352개의 이미지 특징 추출(Image Feature Vecror)하여 Vector 
<br>값 및 Tagging(공모작 명).
<br>-	Infernece Time : 1장당 5ms
<br><Vgg19-block5-conv2-unpooling-encoder>
<br><img width="80%" src="https://github.com/iSPD/COPyCOP/blob/main/images/encoder.png?raw=true"/>
 
<br>4. 이미지 비교(Inference)
<br>-	신청작 이미지를 아래의 모델에 추론(Inference)
<br>-	Object Detection : tensorflow 2.x 라이브러를 이용하여 Mobilenet v3 Object 
<br>Detection모델을 로딩 후, Confidence Rate 0으로 설정 후 여러 개의 
<br>Detection 박스 중 Core+Size기준 1개를 선정. 선정된 영역을 Crop
<br>-	Image Classification : Crop된 이미지를 트레이닝 된 N개의 
<br>  mobilenet_v3_large_100_244 모델에 신청작 이미지를 추론하여 각각 모델
<br>  에서 Score가 가장 높은 사진 추출
<br>-	Image Feature Extraction : Vgg19-block5-conv2-unpooling-encoder에
<br>  신청작 이미지의 Feature Vector를 추출. 미리 추출된 수상작의 Feature
<br>  Vector들과 Spearmanr알고리즘을 이용하여 절대수치를 산정 후,
<br>  기준 수치 이상의 사진 추출.
  
<br>COPyCOP 구성도
<br><img width="80%" src="https://github.com/iSPD/COPyCOP/blob/main/images/%EA%B5%AC%EC%84%B1%EB%8F%84.png"/>
