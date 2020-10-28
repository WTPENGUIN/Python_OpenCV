#-*-coding:utf-8-*-
#필요 모듈 임포트
import cv2
import time

#변수 선언
imageInvert = 1
isDetect = 0

#시간 초기화
pSec = time.time()

#카메라 열기
cap=cv2.VideoCapture(0) 

#배경 사진 찍기
ret1,frame1= cap.read()

#회색으로 처리
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) 
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

while(True):

    #탐색변수 초기화
    isDetect = 0

    #다음 프레임 찍기
    ret2,frame2=cap.read()

    #회색으로 처리
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
    
    #이미지 뺄셈 처리로 차이점 만들어내기
    deltaframe=cv2.absdiff(gray1,gray2)
    
    #너무 민감하지 않게 threshold 적용
    threshold = cv2.threshold(deltaframe, 30, 255, cv2.THRESH_BINARY)[1]

    #윤곽선 만들기 쉽게 팽창연산 2번 적용
    threshold = cv2.dilate(threshold, None, iterations = 2)

    #윤곽 찾기
    countour,heirarc = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #윤곽선 그리기
    for i in countour:
        #일정 면적 미만이면 무시
        if cv2.contourArea(i) < 500:
            continue
        
        #탐색변수, 찾은시간 활성화
        isDetect = 1
        nSec = time.time()

        #사각형 그리기
        (x, y, w, h) = cv2.boundingRect(i)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)

    #알람 활성화 판단
    if (isDetect == True) and (nSec - pSec >= 5):
        print('Detect!')
        print('TEST CODE!')
        pSec = time.time()
    
    if imageInvert:
        frame2 = cv2.flip(frame2, -1) #invert image
    
    cv2.imshow('camera',frame2)
    
    #키 입력 기다림, q 누르면 종료
    if cv2.waitKey(20) == ord('q'):
      break

#opencv 종료
cap.release()
cv2.destroyAllWindows()