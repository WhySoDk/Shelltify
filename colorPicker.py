
import requests
from io import BytesIO
import colorsys
from colorthief import ColorThief

class Colorpicker:
    #check if not too dark
    def isBright(color, threshold=90):
        r, g, b = color
        brightness = (0.299 * r + 0.587 * g + 0.114 * b)
        return brightness > threshold
    
    #check if too white
    def isWhite(color, threshold=220):
        r, g, b = color
        brightness = (0.299 * r + 0.587 * g + 0.114 * b)
        return brightness > threshold
    
    # the value here is bias cuz I like blue
    def calculate_brightness(color):
        r, g, b = color
        # return r+g+b
        return 0.200 * r + 0.400 * g + 0.229 * b
    
    # sat helper function
    def rgb_to_hsv(rgb):
        r, g, b = rgb
        return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    
    #ackullyyy its Sat*brightness
    def compare_saturation(color1, color2):
        _, s1, _ = Colorpicker.rgb_to_hsv(color1) 
        _, s2, _ = Colorpicker.rgb_to_hsv(color2) 
        s1 = s1 * Colorpicker.calculate_brightness(color1)
        s2 = s2 * Colorpicker.calculate_brightness(color2)
        if s1 >= s2:
            return color1
        elif s1 < s2:
            return color2
    
    # for debug purpose, its look good in commandline tho
    def print_palette(palette):
        print("sat:")
        for color in palette:
            r, g, b = color
            _, sat, _ = Colorpicker.rgb_to_hsv(color)
            print(f"\033[48;2;{r};{g};{b}m  \033[0m {sat:.2f}", end="\t\t")
        print()
        
        print("\nbrightness:")
        for color in palette:
            r, g, b = color
            print(f"\033[48;2;{r};{g};{b}m  \033[0m {(Colorpicker.calculate_brightness(color)):.2f}", end="\t")
        print()
        
        print("\nsat*brightness:")
        for color in palette:
            r, g, b = color
            _, sat, _ = Colorpicker.rgb_to_hsv(color)
            brightness = Colorpicker.calculate_brightness(color)
            print(f"\033[48;2;{r};{g};{b}m  \033[0m {(sat * brightness):.4f}", end="\t")
        print()
        
        print("\n too white? / too dark?")
        for color in palette:
            r, g, b = color
            if Colorpicker.isWhite(color): 
                flag = "fail" 
            else: 
                flag = "pass"
            print(f"\033[48;2;{r};{g};{b}m  \033[0m w?{flag}", end="\t")
        print()
        
        for color in palette:
            r, g, b = color
            if Colorpicker.isBright(color): 
                flag = "pass" 
            else: 
                flag = "fail"
            print(f"\033[48;2;{r};{g};{b}m  \033[0m b?{flag}", end="\t")
        print()
    
    # Oh no this class have low cohesion >~< 
    def getColorFromThumbnail(image_url):
        response = requests.get(image_url)
        
        if response.status_code == 200:
            image = BytesIO(response.content)
            color_thief = ColorThief(image)
            palette = color_thief.get_palette(color_count=5, quality=10)
            
            temp = [0, 0, 0]
            for color in palette:
                if not Colorpicker.isWhite(color) and Colorpicker.isBright(color):
                    temp = Colorpicker.compare_saturation(temp, color)
                            
            # r, g, b = temp
            # Colorpicker.print_palette(palette)
            # print(f"picked  \033[48;2;{r};{g};{b}m  \033[0m")
            
            return str(temp)
        
        return '(163, 207, 222)'