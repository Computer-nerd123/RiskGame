class GraphicsMain:
    
    def updateBoard(self, frame, canvas):#more stuff probably
        from tkinter import W
        from time import sleep

        while True:
            import allCountries
            continents = allCountries.continents

            canvas.delete("armyCount")
            for continentName, countryGroup in continents.items():
                for countryName, country in continents[continentName].items():
                    
                    canvas.create_text(country.textPos[0],
                                       country.textPos[1],
                                       anchor=W,
                                       fill=country.textColor,
                                       font="Times",
                                       text=country.curPeople,
                                       tag="armyCount")
            sleep(0.5)
  
    def mainThread(self, threadName):
        import tkinter as tk
        from tkinter import Canvas
        from PIL import Image
        from PIL import ImageTk
        import _thread as thread

        import GameFunctions
        import Rectangle
        import allCountries

        GameFunctions = GameFunctions.GameFunctions()

        def key(event):
            GameFunctions.printOnScreen(canvas, str("Pressed: " + repr(event.char)))

        def on_click(event):
            import Rectangle
            print("Clicked at: " + str(event.x) + ", " + str(event.y))

            if Rectangle.Rectangle().contains([event.x,event.y], [1256,664,2000,664,2000,2000,1256,2000]):
                frame.destroy()
            else:
                CountryInfo = allCountries.CountryInfo()
                text = ""
                clickedOnCountry = CountryInfo.GetCountryNameByClick([event.x, event.y])
                file = open("CurrentClickedCountry.txt", "w")
                file.write(clickedOnCountry)
                file.close()
                text += str(clickedOnCountry + ", bordered by: \n")
                for i in CountryInfo.GetBorderingCountries(clickedOnCountry):
                    text += str("\t\t" + i + "\n")
                text += str("\tOccupied by: " + CountryInfo.GetCurrentOccupent(clickedOnCountry) + "\n")
                text += str("\t\tWith: " + str(CountryInfo.GetCurrentSoliderCount(clickedOnCountry)) + " armies\n")
                GameFunctions.printOnScreen(canvas, str(text))
                
        frame = tk.Tk()

        frame.iconbitmap(default="icon.ico")
        frame.state("zoomed")
        #frame.attributes("-fullscreen", True)
        frame.title(threadName)

        #creating the canvas
        canvas = Canvas(width=10000, height = 10000, bg="black")
        canvas.pack()

        #adding image
        board = Image.open("RiskBoard.jpg")
        boardPhoto = ImageTk.PhotoImage(board)
        canvas.create_image(0,0, image=boardPhoto, anchor="nw")

        #binding click event
        canvas.bind("<Button-1>", on_click)

        #test: drawing rectangles   
        """country = [930,440, 1000,440, 1000,550, 930,550]
        canvas.create_polygon(country, fill='red', outline='black')
        """

        #drawing all images
        canvas.create_polygon([0,664,10000,664,10000,10000,0,10000],fill="ghost white")
        guide = Image.open("ScoringGuide.jpg")
        guidePhoto = ImageTk.PhotoImage(guide)
        canvas.create_image(0,664, image=guidePhoto, anchor="nw")
        end = Image.open("Exit.jpg")
        endPhoto = ImageTk.PhotoImage(end)
        canvas.create_image(1256,664, image=endPhoto, anchor="nw")
        
        #uncomment for collider debugging
        """
        continents = allCountries.continents
        for continentName, countryGroup in continents.items():
            for countryName, country in continents[continentName].items():
                canvas.create_polygon(country.colliderPoints, fill='red', outline='black')
        """

    
        #init game
        thread.start_new_thread(GraphicsMain().updateBoard, (frame, canvas, ))
        thread.start_new_thread(GameFunctions.initGame, (frame, canvas,))
        
        #starting frame loop
        frame.mainloop()

        
