import pandas as pd
import cv2

imageUrl = 'image01.jpg'
clicked = False
redValue = 0
greenValue = 0
blueValue = 0
xPosition = 0
yPosition = 0

colorNameDataFrame = pd.read_csv('wikipedia_color_names.csv')
colorNameDataFrame.drop(colorNameDataFrame.iloc[:,5:8], inplace=True, axis=1)
colorNameDataFrame.rename(columns={'Hex (24 bit)':'Hex', 'Red (8 bit)':'Red', 'Green (8 bit)':'Green', 'Blue (8 bit)':'Blue'}, inplace=True)
image = cv2.imread(imageUrl)

def getColorName(red,green,blue):
    minimumValue = 10000
    for i in range(len(colorNameDataFrame)):
        rgbValue = abs(red- int(colorNameDataFrame.loc[i,"Red"])) + abs(green- int(colorNameDataFrame.loc[i,"Green"]))+ abs(blue- int(colorNameDataFrame.loc[i,"Blue"]))
        if(rgbValue <= minimumValue):
            minimumValue = rgbValue
            colorName = colorNameDataFrame.loc[i,"Name"]
    return colorName

def draw_function(event, x,y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global blueValue, greenValue, redValue, xPosition, yPosition, clicked
        clicked = True
        xPosition = x
        yPosition = y
        blueValue, greenValue, redValue = image[yPosition, xPosition]
        blueValue = int(blueValue)
        greenValue = int(greenValue)
        redValue = int(redValue)

if __name__ == '__main__':
    cv2.namedWindow('Color Name')
    cv2.setMouseCallback('Color Name', draw_function)
    
    while (1):        
        if (clicked):            
            cv2.rectangle(image, (20, 20), (950, 60), (blueValue, greenValue, redValue), -1)
            colorName = 'Selected color name is:-' + getColorName(redValue, greenValue, blueValue)
            cv2.putText(image, colorName, (50, 50), 2, 0.75, (255, 255, 255), 1, cv2.FONT_ITALIC)
            minimumValue = abs(redValue + greenValue + blueValue)
            if (minimumValue >= 600):
                cv2.putText(image, colorName, (50, 50), 2, 0.75, (0, 0, 0), 1, cv2.FONT_ITALIC)
            clicked = False
        cv2.imshow("Color Name", image)
        # Break the loop when user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()

