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
