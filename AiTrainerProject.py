import cv2
import numpy as np
import time
import PoseModule as pm
from fpdf import FPDF

cap = cv2.VideoCapture("AiTrainer/adriantest1.mp4")

detector = pm.poseDetector()
count = 0
count1 = 0
dir = 0
dir1 = 0
pTime = 0



class PDF(FPDF):
    def header(self):
        # font
        self.set_font('helvetica', 'B', 20)
        # Padding
        self.cell(80)
        # Title
        self.cell(30, 10, 'INFORME HADET - VOLEA', ln=1, align='C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # set font
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')





while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    #print(lmList)
    if len(lmList) != 0:
        # Right Arm
        angle = detector.findAngle(img, 12, 14, 16)
        # # Left Arm
        # angle = detector.findAngle(img, 11, 13, 15,False)
        per = np.interp(angle, (190, 199), (0, 100))
        bar = np.interp(angle, (190, 199), (650, 100))

        #voleas malas

        per1 = np.interp(angle, (80, 189), (0, 100))
        bar1 = np.interp(angle, (80, 189), (650, 100))




       # print(angle, per)

        # Check for the dumbbell curls
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:

                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)


    #conteo de las voleas malas
        color = (255, 0, 255)
        if per1 == 100:
            color = (0, 255, 0)
            if dir1 == 0:
                count1 += 0.5
                dir1 = 1
        if per1 == 0:
            color = (0, 255, 0)
            if dir1 == 1:
                count1 += 0.5
                dir1 = 0
        print("volea","-", "Vole mala")
        print(count,"-", count1)


        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count

        cv2.rectangle(img, (0, 750), (400, 610), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f' Buena', (10,700 ), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 0), 3)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)


        #cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    #(255, 0, 0), 25)

       # cv2.rectangle(img, (0, 60), (300, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f' Mala', (250, 700), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 0), 3)
        cv2.putText(img, str(int(count1)), (300, 670), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)






    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                #(255, 0, 0), 5)



    # Create a PDF object
    pdf = PDF('P', 'mm', 'Letter')

    # get total page numbers
    pdf.alias_nb_pages()

    # Set auto page break
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add Page
    pdf.add_page()



    # specify font
    pdf.set_font('helvetica', 'BIU', 16)

    pdf.set_font('times', '', 12)


    pdf.cell(12, 10,f'numero de voleas realizadas: {int(count+count1)} ', ln=True)
    pdf.cell(12, 10, f' numero de voleas buenas: {int(count)} ',ln=True)
    pdf.cell(12, 10, f' numero de voleas malas: {int(count1)} ', ln=True)



    pdf.output('Informe Hadet.pdf')




    cv2.imshow("Image", img)
    cv2.waitKey(1)

