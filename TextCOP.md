# COPyCOP
이미지⋅텍스트(문장) 표절 유사도 검증이 동시⋅병행 가능한 AI 표절 검출 시스템

- <b>ImageCOP</b> : 객체 추적 인식 AI 모델의 다중 적용 및 VGG19 벡터 비교를 통한 이미지 표절 검출 및 검출 오류 보정
  <br> &#8226; Python 3.7
  <br> &#8226; VGG19
- <b>TextCOP</b> : doc2vec 모델을 활용한 한국어 텍스트 표절 검출, TF-IDF 알고리즘으로 텍스트 유사도 오류 보정
  <br> &#8226; Python 3.7
  <br> &#8226; Sentence Pre-Processing
  <br>전체 Text를 정제된 텍스트로 변환 후, 문장 단위로 쪼개어 고유의 ID를 부여한 후 ID + 정제된 문장 쌍의 형태로 생성
  <br></br>
  <div align="center">
  <img width="60%" src="https://user-images.githubusercontent.com/131632610/233918532-7df64c0a-34c3-47fc-b797-1909061d6e95.JPG"/>
  <br><그림 1. doc2vec 모델을 위한 pre-precessing 적용>
  </div>
  <br> &#8226; doc2vec
  <br>Pre-Processing을 거친 문장들을 10만 문장 단위로 training하여 생성한 모델파일에 표절 의심 문장을 입력하여 문장 유사도를 측정하고 대상 문장의 ID를 출력</br>
  <br> &#8226; TF-IDF
  <br>doc2vec을 거친 테스트 문장과 대상 문장을 맞춤법 교정. 형태소별 분리 후 조사 제거의 전처리를 거쳐 TF-IDF 로 입력하여 vectorization 후 단어 유사도를 측정</br>
  <br></br>
  <div align="center">
  <img width="80%" src="https://user-images.githubusercontent.com/131632610/233915448-066283be-c6bc-41dd-8da4-10e0620d7060.jpg"/>
  <br><표 1. doc2vec 오류보정을 위한 TF-IDF 단어유사도 보정 방식>
  </div>
  <br> &#8226; 텍스트 표절 유사도 AI 솔루션 테스트
  <br> &#160;&#160;&#160;&#160;&#8730; 학습 데이터셋 : 위키피디아, 언론사 공모전 수상작의 내용을 무작위 추출 후 Pre-Processing을 거쳐 10만 문장 단위로 ID + 정제된 문장셋을 생성
  <br> &#160;&#160;&#160;&#160;&#8730; Training : Pre-Processing을 거친 문장들을 10만 문장 단위로 Training & 모델 생성
  <br> &#160;&#160;&#160;&#160;&#8730; 테스트 데이터셋 : 학습 데이터셋 중 무작위로 M개 문장 추출 후 100%표절, 1 ~ N개 단어 제거, 1 ~ N개 단어 교체 방법으로 변형 후 파일에 저장 및 정답 파일에 해당 ID 기록하여 테스트 데이터셋 구축 진행
  <br> &#160;&#160;&#160;&#160;&#8730; 테스트 방법 : 테스트 파일을 doc2vec 모델과 TF-IDF에 입력하여 문장 유사도, 단어 유사도를 측정 후 두 수치의 평균값이 일정 기준 이상일 때 표절 의심으로 판정
  
    
