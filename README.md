#Chess-bot
Welcome!

Welcome to the Chess bot landing page. This page is home to a ROS package that manipulates a Widow X robotic arm to play chess in real-time against a human player. The package enables the robot to interpret the changing chessboard with machine vision, calculate the best move to make, and then pick up and place its chess piece in order to make that move.
Meet the team:

    Will Young: Will Young is a mechanical engineering student at Olin College of Engineering set to graduate in 2024. He is excited to work on robotic arm control and path planning. He would also like to focus on making sure we have a good ROS structure for the project. He says he has watched Gotham Chess like twice, so he’s basically a chess expert.
    Mia Chevere: Mia Chevere is an electrical and computer engineering student at Olin College of Engineering. She’s excited to do the kinematic math involved in moving an arm to specific locations! She says that she never took basic geometry, so she looks forward to the challenge.
    Eddy Pan: Eddie is either an engineering with computing student at Olin College of Engineering. He used to play chess in his prime (4th grade) and has been on the low ever since. He’s pretty interested in how the game is played and has been hoping to make a chess bot ever since declaring his major. He also says he saw a robot chess arm break the finger of a kid, and he thought that was really not cool, so he thinks we can do it better.
    Dan Park: Dan Park is an engineering with computing student at Olin College of Engineering set to graduate in 2025. He says he got round of 16 for the JPMorgan Chess Competition, so he guesses he’s okay at chess.

Package structure

This package is structured in (at least) the following ROS nodes:

    Perception

    This node will intake information from the camera and use it to determine which pieces are stored in which squares.

    Movement calculator

    The information from the perception node can be used to recreate the board and calculate the robot's next move. This decision will be made using discrete math taken from Eddie’s discrete final. The final decision of which piece to move will be sent to the path planner node.

    Path Planner

    Our setup will be using a specific chessboard with a precise relationship to the Widow X arm. This will allow us to store the pose information of each square of the board such that when a piece is placed on a board, we have a pose estimate for where it is based on which square it’s in. We can then create waypoints along its trajectory to guide it.

    Arm movement controller

    Based on the waypoint the arm is at, the arm movement controller will guide the Widow X to move towards the point and tighten and loosen its grip as necessary.

Milestone 1

After about 1 week of working on the project, our team was able to make progress on three major fronts:

    Computational Set-up
        In order to operate the Widow X with our computers, we used the robot bridge repository from the Berkeley Robot and AI Laboratory.
        We were also able to get a functional simulator running for the Widow X on each of our computers using the Trossen Robotics X Series Arms Simulator. This will be invaluable for testing as we begin to write our own nodes and don’t all have access to the Widow X at the same time.
        We also started a collection of helpful commands for controlling the robot.
    Background Research
        Before we started working on our node network, we did some research on previous uses of the Widow X, previous chess bots, and kinematic arm theory. We learned a lot about how packages for the Widow X can be structured, parallel vs. forward kinematics arm theory, and machine vision depth solutions that will inform how we structure our project.
    Structure Plan
        Our structure plan is the precursor of our system architecture that we will be finalizing in the next few days. It can be seen in greater detail in the “package structure” portion of our webpage slightly above. While we were designing this, we tried to keep in mind what the objective of the project was and how we could scope our MVP accordingly. For example, the objective of this project is not to estimate depth using stereo vision. Therefore, for our MVP we are finding alternative ways of estimating a chess piece's pose in three-dimensional space.
    Website
        We set up our website! You’re looking at it now! We’re very excited about it!

Though some of the finer details of this project have not yet been decided, we have a much better idea of what kinds of problems we will have to solve and are excited to start tackling them.

