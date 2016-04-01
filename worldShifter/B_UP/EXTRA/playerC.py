def handle_slopes(self, slopeG):
        """
	(Hopefully) handles slope collisions.
	slopeG = slope sprites Group
	NOTE: slopeG must contain homogeneous slopes
	"""
	
        

        colSprite = pygame.sprite.spritecollideany(self, slopeG)
        if colSprite:
	    self.fall = False
	else:
	    self.slope_first = False

	if colSprite and (self.rect.y < colSprite.rect.y):

	    tl = colSprite.rect.topleft # used for slope calculation only
	    br = colSprite.rect.bottomright 
	    
	    m1 = float((br[1]-tl[1])/(br[0]-tl[0]))   # y2-y1/(x2-x1)
	    angle_rad = math.atan(m1)                # from atan(m1 - m1 /(1+m1m2))
	    # The angle is normally 45 degrees 

	    if self.x_vel:
		#le = self.x_vel / abs(self.x_vel) * 4
		le = self.x_vel
	    else: 
		le = 0
		
	    x_move_len = le
	    y_move_len = self.calc_vertical(x_move_len, angle_rad)
	    
	    # just for debugging
	    self.d1 = x_move_len
	    self.d2 = y_move_len

	    # Now, it is needed to move the player down till
	    # he reaches the 'essence' of the slope. This is because I 
	    # am too lazy to implement pixel-perfect collision.
	    # Since this is to be done only once, a variable will be used
	    # to keep track of whether this has beend donef for one slope or not
	    
	    # tolerance for height changing
	    tol = False
	    if abs(self.rect.topleft[1] - self.rect.bottomleft[1]) <  3:
	        tol = True

	    if not self.slope_first and tol:
	        self.slope_first = True
	        x_off_mov = colSprite.rect.topleft[0]  -  self.rect.bottomleft[0]
		y_off_mov = self.calc_vertical(x_off_mov, angle_rad)
                
		# handling for rightwards velocity
		if self.direction == RIGHT:
		    y_off_mov = -y_off_mov
		

                self.rect.move_ip((0, y_off_mov))

	    # check collision with any slope
	    
	    #self.rect.move_ip((x_move_len, y_move_len))
            # it seems that the above code is redundant; will check
	    self.rect.move_ip((-self.x_vel, 0)) # undo the shifting
	    self.rect.move_ip((x_move_len, y_move_len))

    def manage_states(self):
        
	# set appropriate animation for walking
        if self.walk and not self.fall:
	    if self.direction == RIGHT:
	        self.walkPos = self.animate(self.walk_r_list, self.walkPos, \
		                            self.walkFact)
	    elif self.direction == LEFT:
	        self.walkPos = self.animate(self.walk_l_list, self.walkPos, \
		                            self.walkFact)
	
	elif self.walk and self.fall:
	    if self.direction == RIGHT:
	        self.image = self.rightIdleImg
	    else:
	        self.image = self.leftIdleImg
	
	elif self.idle or self.fall:
	    if self.direction == RIGHT:
	        self.image = self.rightIdleImg
	    else:
	        self.image = self.leftIdleImg
	
	

    # chief method
    def update(self, keys, obstacles, slopeG):
        
	# current time
	# for toggling the self.canShift
	samaya = time.time()   
        self.OUTLIST[1] = samaya

        self.check_keys(keys)
	self.handle_slopes(slopeG)
	self.get_position(obstacles)
	self.manage_states()

	#self.x += self.x_vel
	#self.rect.x += self.x_vel

	if self.fall:
	    self.y_vel += GRAVITY
	else:
	    self.y_vel = 0
   
        self.x += self.x_vel	
	#self.rect.y += self.y_vel
	#self.y += self.y_vel

        return self.OUTLIST

    def draw(self, surface):
        surface.blit(self.image, self.rect)
       

