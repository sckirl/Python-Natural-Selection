from random import randrange
import pygame
pygame.init()

class Graph:
    def __init__(self, window):
        self.WIN = window

        self.xData = [0]
        self.yData = [0]

        self.xScale = 1
        self.yScale = 1

        self.FONT = pygame.font.SysFont('montserrat', 10, bold=True)

    def addData(self, x, y):
        self.xData.append(x / self.xScale)
        self.yData.append(y / self.yScale)

    def scaleDown(self, data):
        data = data // 10
        self.scale += 10
        if data > 500: self.scaleDown(data)
        
    def visualize(self, xPos, yPos, RANGE=20):
        # y axis
        pygame.draw.lines(self.WIN, [255, 255, 255], closed=True,
                          points=[(xPos, yPos-180), (xPos, yPos)], width=2)
        # x axis
        pygame.draw.lines(self.WIN, [255, 255, 255], closed=True,
                          points=[(xPos+180, yPos), (xPos, yPos)], width=2)

        for i in range(10):
            # y markers
            pygame.draw.lines(self.WIN, [255, 255, 255], closed=True,
                          points=[(xPos-5, yPos - (RANGE * i)), (xPos+5, yPos - (RANGE * i))], width=2)
            
            marker = self.FONT.render(str(i), False, (255, 255, 255))
            self.WIN.blit(marker, (xPos-15, (yPos - (RANGE * i))))

            # x markers
            pygame.draw.lines(self.WIN, [255, 255, 255], closed=True,
                          points=[(xPos + (RANGE * i), yPos-5), (xPos + (RANGE * i), yPos + 5)], width=2)

            marker = self.FONT.render(str(i), False, (255, 255, 255))
            self.WIN.blit(marker, ((xPos + (RANGE * i), yPos+10)))

        # visualize the data
        for n in range(1, len(self.xData)-1):
            pygame.draw.lines(self.WIN, [255, 255, 255], closed=True,
                              points=[(xPos + (self.xData[n-1]), yPos - self.yData[n-1]), 
                                      (xPos + self.xData[n], yPos - self.yData[n])], width=2)