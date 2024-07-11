import sys, random, os, pickle

index = sys.argv[10]


class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):

        with open('/Users/harris/MLGame/brickgame/successful/K'+index+'.pickle', 'rb') as f:
           self.model = pickle.load(f)
        self.prev_ballX = 0  
        self.prev_ballY = 0
        self.platformX = 0

        self.level = 0
        self.run = 0
        self.dataFinal = []
        self.game_status = None
        
        #print(ai_name)

    def update(self, scene_info, *args, **kwargs):
        command = ""
        ### Grap all the information that we need to make a landing prediction
        self.curr_ballX = scene_info['ball'][0]
        self.curr_ballY = scene_info['ball'][1]
        self.platformX = scene_info['platform'][0]
        # Calculate the direction 
        deltaX = self.curr_ballX - self.prev_ballX
        deltaY = self.curr_ballY - self.prev_ballY
        # Update the previous ball position
        self.prev_ballX = scene_info['ball'][0]
        self.prev_ballY = scene_info['ball'][1]
        # Caculate the direction of velocity and the slope
        direction = self.direction(deltaX, deltaY)
        

        # input x, and would ouput y 
        dataPerFrame = [[self.curr_ballX, self.curr_ballY, deltaX, deltaY,
                          direction, self.platformX, scene_info["frame"]]]
        
        decision = self.model.predict(dataPerFrame)
        #print(decision[0])
        if decision[0] == -1:
            command = "MOVE_LEFT"
        elif decision[0] == 1:
            command = "MOVE_RIGHT"
        else:
            command = "NONE"
        #print(command)
        self.game_status = scene_info["status"]
        if (self.game_status == "GAME_PASS"):
            self.run += 1
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
        """
        Reset the status
        """
        #self.ball_served = False
        if self.run == 1:
            sys.exit()  
       
       
