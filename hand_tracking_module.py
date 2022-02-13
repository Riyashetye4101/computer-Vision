import cv2
import mediapipe as mp
import time


class Detection():
	def __init__(self, mode=False, maxHands=2,modelC=1, detectionCon=0.5, trackCon=0.5):
		self.mode = mode
		self.modelC = modelC
		self.maxHands=maxHands
		self.detectionCon = detectionCon
		self.trackCon = trackCon

		self.mpDraw = mp.solutions.drawing_utils
		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(
			self.mode,
			self.maxHands,
			self.modelC,
			self.detectionCon,
			self.trackCon
			)

	def findHands(self, img, draw=True):
														# sending the rgb color images
		imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		self.results =self.hands.process(imgRGB)
														# print(results.multi_hand_landmarks)
														# if the hand is detected then do some work
		if self.results.multi_hand_landmarks:
		    for handlms in self.results.multi_hand_landmarks:
		    	if draw:
		        	self.mpDraw.draw_landmarks(img,handlms,self.mpHands.HAND_CONNECTIONS)

		return img

	def findPosition(self, img, handNo=0, draw = True):
		lm_List = []
		
		if self.results.multi_hand_landmarks:
			myHand = self.results.multi_hand_landmarks[handNo]
			for id,lm in enumerate(myHand.landmark):
			    # print(id,' ',lm)
			    h, w, c= img.shape
			    cx, cy = int(lm.x*w), int(lm.y*h)  # provides the pixels of each hand frame
			  
			    lm_List.append([id,cx,cy])
			    
			    if draw:
			    	cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

		return lm_List
















def main():
	ptime=0
	ctime=0
	detector = Detection()
	cap = cv2.VideoCapture(0)

	while True:
		success, img = cap.read()
		img = detector.findHands(img)
		lmlist = detector.findPosition(img)
		if len(lmlist)!=0:
			print(lmlist[4])

		ctime=time.time()
		fps = 1/(ctime-ptime)
		ptime = ctime

		cv2.putText(img,str(int(fps)),(10,78),cv2.FONT_HERSHEY_PLAIN,3,
		            (255,0,255),3)

		cv2.imshow("frame" , img)
		cv2.waitKey(1)

if __name__ == '__main__':
	main()