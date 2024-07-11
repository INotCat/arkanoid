import sys, random, os, pickle

class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        self.prev_ballX = 0  
        self.prev_ballY = 0
        self.platformX = 0

        self.run = 0
        self.data_list = []
        self.dataFinal = []
        self.game_status =None
        print(ai_name)

    def update(self, scene_info, *args, **kwargs):
        
        self.curr_ballX = scene_info['ball'][0]
        self.curr_ballY = scene_info['ball'][1]
        self.platformX = scene_info['platform'][0]
        
        # Calculate the direction 
        deltaX = self.curr_ballX - self.prev_ballX
        deltaY = self.curr_ballY - self.prev_ballY
        
        #Update the previous ball position
        self.prev_ballX = scene_info['ball'][0]
        self.prev_ballY = scene_info['ball'][1]
        
        direction = self.direction(deltaX, deltaY)
        
        # If ball move horizontally or upward, then the platform should not move
        if not ( deltaX == 0 or deltaY <= 0 ):
            slope = deltaY / deltaX
            # Calculate the landing point (x-intercept of two lines)  
            landingX = ( (400-self.curr_ballY)/slope ) + self.curr_ballX
            # According to the even and odd characteristic to predict the x-intercept
            bounce_count = int(landingX/200)
            if bounce_count%2 == 0:
                landingX = abs(landingX-200*bounce_count)
            else:
                landingX = 200-abs(landingX-200*bounce_count)
           
            # Make decisions according to the predict landing point with a random threshold
            if landingX > (self.platformX +20+random.randint(-15, 15)):
                command = "MOVE_RIGHT"
            elif landingX < (self.platformX +20+random.randint(-15, 15)):
                command = "MOVE_LEFT"
            else:
                command = "NONE"
        else:
            command = "NONE"
            
        if command == "MOVE_LEFT":
            Cvalue = -1
        elif command == "MOVE_RIGHT":
            Cvalue = 1
        else:
            Cvalue = 0
        # Save file    
        dataPerFrame = [self.curr_ballX, self.curr_ballY, deltaX, deltaY,
                          direction, self.platformX, scene_info["frame"] ,Cvalue]
        # Append data per frame to a big list we save to file
        self.dataFinal.append(dataPerFrame)
        # Flush current data for the usage of next frame
        dataPerFrame = []  
        
        if scene_info["status"] == "GAME_PASS":
            self.game_status = "GAME_PASS"
        if(scene_info["status"] == "GAME_PASS"):
            self.run +=1
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"
        
        #serve ball
        if not scene_info["ball_served"]:
            command = "SERVE_TO_LEFT"
        
        return command

    def direction(self, deltaX, deltaY):
    # 0(↘),1(↗),2(↙),3(↖)
        if (deltaX > 0):
            if ( deltaY > 0):
                direction = 0 
            else:
                direction = 1
        else:
            if ( deltaY > 0):
                direction = 2
            else:    
                direction = 3
        return direction

    def reset(self):
        #print("round ", self.round)
        #self.round+=1
        """
        Reset the status
        """
        index = "8"
        filepath = "/Users/harris/MLGame/log" + index
        print(filepath)
        if (self.game_status == "GAME_PASS"):
            filepath = "/Users/harris/MLGame/log" + index
            # one shot is 10, without is 9
            filename = sys.argv[10]+ "-" + index +".pickle"
            print(filename)
            with open(os.path.join(filepath, filename), "wb") as f:   
                pickle.dump(self.dataFinal, f) 
        if self.run == 1:
            sys.exit()  
