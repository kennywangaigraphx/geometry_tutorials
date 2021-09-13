   import rclpy
   from rclpy.node import Node
   from rclpy.duration import Duration

   from geometry_msgs.msg import PointStamped, Point
   from geometry_msgs.msg import Twist
   from turtlesim.msg import Pose
   from turtlesim.srv import Spawn
   
   
   class PointPublisher(Node):

       def __init__(self):
           super().__init__('turtle_tf2_msg_broadcaster')
        
           self.client = self.create_client(Spawn, 'spawn')
           while not self.client.wait_for_service(timeout_sec=1.0):
               self.get_logger().info('service not available, waiting again...')
           request = Spawn.Request()
           request.name = 'turtle3'
           request.x = float(4)
           request.y = float(2)
           request.theta = float(0)
           self.client.call_async(request)
        
           self.vel_pub = self.create_publisher(Twist, "/turtle3/cmd_vel",1) 
           self.sub = self.create_subscription(Pose, "/turtle3/pose",self.handle_turtle_pose, 1) 
           self.sub
           self.pub = self.create_publisher(PointStamped, "/turtle3/turtle_point_stamped", 1)
        
       def handle_turtle_pose(self,msg):
           vel_msg = Twist()
           vel_msg.linear.x =1.0
           vel_msg.angular.z = 1.0
           self.vel_pub.publish(vel_msg) 
           
           ps = PointStamped()
           ps.header.stamp = self.get_clock().now().to_msg()
           ps.header.frame_id = 'world'
           ps.point.x = msg.x
           ps.point.y = msg.y
           ps.point.z = 0.0
           self.pub.publish(ps)
    
 
   def main():
       rclpy.init()
       node = PointPublisher()     
       try:
           rclpy.spin(node)
       except KeyboardInterrupt:
           pass  
       rclpy.shutdown()