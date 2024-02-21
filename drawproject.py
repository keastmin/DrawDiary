import numpy as np, cv2
import os

# 기본 경로 설정
### 여기서 경로를 설정하세요
base_dir = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory"
backup_dir = os.path.join(base_dir, "backupImage")
icon_dir = os.path.join(base_dir, "Icon")
picback_dir = os.path.join(base_dir, "picback")

# 필요한 디렉토리가 없으면 생성
os.makedirs(base_dir, exist_ok=True)
os.makedirs(backup_dir, exist_ok=True)
os.makedirs(icon_dir, exist_ok=True)
os.makedirs(picback_dir, exist_ok=True)

drawing = False
erase = False
centerPt = (-1, -1)
colorMode = 0
ColorDegree = (0, 0, 255)

no = 0
maxPage = 1
title = 'print'
title2 = 'controler'
pptImage = np.full((600, 800, 3), (255, 255, 255), np.uint8)

ppt_image_path = os.path.join(base_dir, "00.jpg")
backup_image_path = os.path.join(backup_dir, "00.jpg")

cv2.imwrite(ppt_image_path, pptImage)
cv2.imwrite(backup_image_path, pptImage)

pname = os.path.join(base_dir, f"{no:02d}.jpg")
image = cv2.imread(pname, cv2.IMREAD_COLOR)
print("ESC : 종료")
print(" <- : 이전 페이지")
print(" -> : 다음 페이지")
print("  + : 페이지 추가")
print("  - : 페이지 삭제")
print("  s : 이미지 저장")
print("  b : 백업본 불러오기")
print("  p : 사진 입력")
print("  u : 사진 위의 라인들에 투명도 적용")
print(" bp : 사진 백업본 불러오기")


backgroundMode = 0

##명암 보정
def mat_access(mat):
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            k = mat[i, j]
            sum = int(k[0])+int(k[1])+int(k[2])
            avg = sum / 3
            if avg < 30:
                mat[i, j] = k + 10
            elif avg < 20:
                mat[i, j] = k + 20
            elif avg < 15:
                mat[i, j] = k + 25
            elif avg < 10:
                mat[i, j] = k + 30

def mat_access_not(mat):
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            k = mat[i, j]
            sum = int(k[0])+int(k[1])+int(k[2])
            avg = sum / 3
            if avg < 17:
                mat[i, j] = 255
            else:
                mat[i, j] = 0

## 아이콘 배치 함수
def place_icons(image, size):
    icon_name = ["createPage", "deletePage", "savePage", "backupPage", "loadPicture", "UnvisibleLine", "backupPicture"]
    icons = [(i, 0, 1, 1) for i in range(len(icon_name))]
    icons = np.multiply(icons, size*2)

    for roi, name in zip(icons, icon_name):
        icon_path = os.path.join(icon_dir, f"{name}.jpg")
        icon = cv2.imread(icon_path, cv2.IMREAD_COLOR)
        if icon is None:continue
        x, y, w, h = roi
        image[y:y+h, x:x+w] = cv2.resize(icon, size)

    return list(icons)


## 마우스 그리기 이벤트
def onMouse1(event, x, y, flags, param):
    global drawing, title, no, maxPage, image, pptImage, centerPt, erase, ColorDegree

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        centerPt = (x, y)
        cv2.circle(param, centerPt, 3, ColorDegree, -1)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(param, (centerPt), (x, y), ColorDegree, 3, cv2.LINE_AA)
            centerPt = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        tmpDir = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
        cv2.imwrite(tmpDir, param)

    if event == cv2.EVENT_RBUTTONDOWN:
        erase = True
        centerPt = (x, y)
        cv2.circle(param, centerPt, 3, (255, 255, 255), -1)
    elif event == cv2.EVENT_MOUSEMOVE:
        if erase:
            cv2.line(param, (centerPt), (x, y), (255, 255, 255), 3, cv2.LINE_AA)
            centerPt = (x, y)
    elif event == cv2.EVENT_RBUTTONUP:
        erase = False
        tmpDir = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
        cv2.imwrite(tmpDir, param)


## 마우스 그리기 이벤트
def onMouse2(event, x, y, flags, param):
    global drawing, title, no, maxPage, image, pptImage, centerPt, ColorDegree, colorMode

    if event == cv2.EVENT_LBUTTONDOWN:
        if x > 0 and x < 50 and y > 0 and y < 50: ## 페이지 추가
            if no < maxPage - 1:
                for i in range(maxPage - (no + 1)):
                    tmpDir1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(maxPage - i - 1)
                    tmpDirBack1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(maxPage - i - 1)
                    tmpDir2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(maxPage - i)
                    tmpDirBack2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(maxPage - i)
                    tmpImage = cv2.imread(tmpDir1, cv2.IMREAD_COLOR)
                    tmpbackImage = cv2.imread(tmpDirBack1, cv2.IMREAD_COLOR)
                    cv2.imwrite(tmpDir2, tmpImage)
                    cv2.imwrite(tmpDirBack2, tmpbackImage)

                tmpDirecstr1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
                cv2.imwrite(tmpDirecstr1, image)
                maxPage = maxPage + 1
                no = no + 1
                tmpDirecstr2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
                tmpDirecstrBack = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(no)
                cv2.imwrite(tmpDirecstr2, pptImage)
                cv2.imwrite(tmpDirecstrBack, pptImage)
                image = cv2.imread(tmpDirecstr2, cv2.IMREAD_COLOR)
            else:
                tmpDirecstr1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
                cv2.imwrite(tmpDirecstr1, image)
                maxPage = maxPage + 1
                no = no + 1
                tmpDirecstr2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
                tmpDirecstrBack = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(no)
                cv2.imwrite(tmpDirecstr2, pptImage)
                cv2.imwrite(tmpDirecstrBack, pptImage)
                image = cv2.imread(tmpDirecstr2, cv2.IMREAD_COLOR)

        elif x > 50 and x < 100 and y > 0 and y < 50: ##페이지 삭제
            if maxPage > 1:
                file_path = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
                file_pathback = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(no)

                if os.path.exists(file_path) and os.path.exists(file_pathback):
                    os.remove(file_path)
                    os.remove(file_pathback)

                    if no + 1 == maxPage:
                        no = no - 1
                        maxPage = maxPage - 1
                        bImage = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
                        image = cv2.imread(bImage, cv2.IMREAD_COLOR)

                        file_picback = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no + 1)
                        if os.path.exists(file_picback):
                            os.remove(file_picback)
                    elif no > 0:
                        no = no - 1
                        maxPage = maxPage - 1
                        bImage = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
                        image = cv2.imread(bImage, cv2.IMREAD_COLOR)
                        for i in range(maxPage - no - 1):
                            tmp1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no + i + 2)
                            tmpb1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(no + i + 2)
                            tmp2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no + i + 1)
                            tmpb2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(no + i + 1)
                            tmpImage = cv2.imread(tmp1, cv2.IMREAD_COLOR)
                            tmpbackImage = cv2.imread(tmpb1, cv2.IMREAD_COLOR)
                            cv2.imwrite(tmp2, tmpImage)
                            cv2.imwrite(tmpb2, tmpbackImage)
                        last_file = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(maxPage)
                        last_backfile = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(maxPage)
                        os.remove(last_file)
                        os.remove(last_backfile)

                        file_picback = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no + 1)
                        if os.path.exists(file_picback):
                            os.remove(file_picback)
                        for i in range(maxPage - no - 1):
                            print(i)
                            file_picbacktmp1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no + i + 2)
                            if os.path.exists(file_picbacktmp1):
                                file_picbacktmp2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no + i + 1)
                                tmpbackImage1 = cv2.imread(file_picbacktmp1, cv2.IMREAD_COLOR)
                                cv2.imwrite(file_picbacktmp2, tmpbackImage1)
                        last_picback = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(maxPage)
                        if os.path.exists(last_picback):
                            os.remove(last_picback)

                    elif no == 0:
                        maxPage = maxPage - 1
                        bImage = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no + 1)
                        image = cv2.imread(bImage, cv2.IMREAD_COLOR)
                        for i in range(maxPage):
                            tmp1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no + i + 1)
                            tmpb1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(no + i + 1)
                            tmp2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no + i)
                            tmpb2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(no + i)
                            tmpImage = cv2.imread(tmp1, cv2.IMREAD_COLOR)
                            tmpbackImage = cv2.imread(tmpb1, cv2.IMREAD_COLOR)
                            cv2.imwrite(tmp2, tmpImage)
                            cv2.imwrite(tmpb2, tmpbackImage)
                        last_file = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(maxPage)
                        last_backfile = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(maxPage)
                        os.remove(last_file)
                        os.remove(last_backfile)

                        file_picback = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no)
                        if os.path.exists(file_picback):
                            os.remove(file_picback)
                        for i in range(maxPage):
                            file_picbacktmp1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no + i + 1)
                            if os.path.exists(file_picbacktmp1):
                                file_picbacktmp2 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no + i)
                                tmpbackImage1 = cv2.imread(file_picbacktmp1, cv2.IMREAD_COLOR)
                                cv2.imwrite(file_picbacktmp2, tmpbackImage1)
                        last_picback = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(maxPage)
                        if os.path.exists(last_picback):
                            os.remove(last_picback)

            else:
                print("더 이상 지울 수 없습니다.")

        elif x > 100 and x < 150 and y > 0 and y < 50:  ## 페이지 백업 저장
            tmp1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
            tmpb1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(no)
            tmpImage = cv2.imread(tmp1, cv2.IMREAD_COLOR)
            cv2.imwrite(tmp1, tmpImage)
            cv2.imwrite(tmpb1, tmpImage)
            print("저장")

        elif x > 150 and x < 200 and y > 0 and y < 50:  ## 페이지 백업
            tmp1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
            tmpb1 = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/backupImage/{0:02d}.jpg".format(no)
            tmpbImage = cv2.imread(tmpb1, cv2.IMREAD_COLOR)
            cv2.imwrite(tmp1, tmpbImage)
            backupImage = cv2.imread(tmp1, cv2.IMREAD_COLOR)
            image = backupImage
            print("백업")

        elif x > 200 and x < 250 and y > 0 and y < 50:  ## 사진 불러오기
            picAdd = input("주소를 입력하세요")
            print(picAdd)
            pic1 = cv2.imread(picAdd, cv2.IMREAD_COLOR)
            if pic1 is None: raise Exception("경로가 잘못되었습니다.")

            dst1 = cv2.resize(pic1, (500, 300), 0, 0, cv2.INTER_NEAREST)
            mat_access(dst1)

            picbackFile = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no)
            tmpnoFile = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)

            tmpimage = cv2.imread(tmpnoFile, cv2.IMREAD_COLOR)
            backImage = np.zeros((600, 800, 3), np.uint8)

            picture = dst1
            masks = cv2.threshold(picture, 0, 255, cv2.THRESH_BINARY)[1]
            masks = cv2.split(masks)
            fg_pass_mask = cv2.bitwise_or(masks[0], masks[1])
            fg_pass_mask = cv2.bitwise_or(masks[2], fg_pass_mask)
            bg_pass_mask = cv2.bitwise_not(fg_pass_mask)
            (H, W), (h, w) = tmpimage.shape[:2], picture.shape[:2]
            x, y = (W - w) // 2, (H - h) // 2 + 50
            roi = tmpimage[y:y + h, x:x + w]
            foreground = cv2.bitwise_and(picture, picture, mask=fg_pass_mask)
            background = cv2.bitwise_and(roi, roi, mask=bg_pass_mask)
            dst = cv2.add(background, foreground)
            tmpimage[y:y + h, x:x + w] = dst
            backImage[y:y + h, x:x + w] = dst
            cv2.imwrite(tmpnoFile, tmpimage)
            image = tmpimage
            cv2.imwrite(picbackFile, backImage) ## 백업 사진 저장

        elif x > 250 and x < 300 and y > 0 and y < 50:  ## 사진에 대한 라인 투명도
            picbackFile = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no)
            tmpnoFile = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
            if os.path.exists(picbackFile):
                backImage = cv2.imread(picbackFile, cv2.IMREAD_COLOR)
                curImage = cv2.imread(tmpnoFile, cv2.IMREAD_COLOR)
                dsr = cv2.bitwise_or(backImage, curImage)
                cv2.imwrite(tmpnoFile, dsr)
                image = dsr

        elif x > 300 and x < 350 and y > 0 and y < 50:  ## 사진 백업
            tmpnoFile = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
            picbackFile = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/picback/{0:02d}.jpg".format(no)

            curImage = cv2.imread(tmpnoFile, cv2.IMREAD_COLOR)
            backImage = cv2.imread(picbackFile, cv2.IMREAD_COLOR)
            backImage2 = cv2.imread(picbackFile, cv2.IMREAD_COLOR)
            backImagetmp = backImage
            mat_access(backImagetmp)
            mat_access_not(backImagetmp)
            dst1 = cv2.bitwise_and(curImage, backImagetmp)
            dst2 = cv2.bitwise_and(curImage, dst1)
            dst3 = cv2.bitwise_or(backImage2, dst2)

            ##cv2.imshow("bakc_not", backImage)
            ##cv2.imshow("back_file", backImage2)
            ##cv2.imshow("test1", dst1)
            ##cv2.imshow("test2", dst2)


            cv2.imwrite(tmpnoFile, dst3)
            image = dst3



        elif x > 570 and x < 590 and y > 0 and y < 50: ## 색 전환
            colorMode = (colorMode + 1) % 4
            if colorMode == 0:
                ColorDegree = (0, 0, 255)
            elif colorMode == 1:
                ColorDegree = (0, 255, 0)
            elif colorMode == 2:
                ColorDegree = (255, 0, 0)
            elif colorMode == 3:
                ColorDegree = (0, 0, 0)



cv2.namedWindow(title)
cv2.namedWindow(title2)

while True:
    controlerImage = np.full((50, 600, 3), (255, 255, 255), np.uint8)
    icons = place_icons(controlerImage, (50, 50))

    cv2.setMouseCallback(title, onMouse1, image)
    cv2.setMouseCallback(title2, onMouse2, controlerImage)

    setText = str(no + 1) + "/" + str(maxPage)
    cv2.putText(controlerImage, setText, (500, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0),1,cv2.LINE_AA)
    cv2.circle(controlerImage, (570, 20), 20, ColorDegree, -1)
    cv2.imshow(title, image)
    cv2.imshow(title2, controlerImage)

    keycode = cv2.waitKeyEx(1)
    if keycode == 0x1B:
        break
    elif keycode == 0x250000:
        no = no - 1
        if no == -1:
            no = no + 1
            print("이전 페이지가 없습니다.")
        tmpDir = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
        image = cv2.imread(tmpDir, cv2.IMREAD_COLOR)
    elif keycode == 0x270000:
        no = no + 1
        if no == maxPage:
            no = no - 1
            print("다음 페이지가 없습니다.")
        tmpDir = "C:/Users/kemin/PycharmProjects/pythonProject/DrawDiary/pptDirectory/{0:02d}.jpg".format(no)
        image = cv2.imread(tmpDir, cv2.IMREAD_COLOR)