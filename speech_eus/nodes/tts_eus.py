#!/usr/bin/env python

# /*********************************************************************
# * Software License Agreement (BSD License)
# *
# * Copyright 2014, RSAIT research group, University of Basque Country
# * All rights reserved.
# *
# * Redistribution and use in source and binary forms, with or without
# * modification, are permitted provided that the following conditions
# * are met:
# *
# *  * Redistributions of source code must retain the above copyright
# *    notice, this list of conditions and the following disclaimer.
# *  * Redistributions in binary form must reproduce the above
# *    copyright notice, this list of conditions and the following
# *    disclaimer in the documentation and/or other materials provided
# *    with the distribution.
# *  * Neither the name of the University of Freiburg nor the names of its
# *    contributors may be used to endorse or promote products derived
# *    from this software without specific prior written permission.
# *
# * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# * HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# *********************************************************************/

import roslib; 
import rospy
import time
from std_msgs.msg import Int8
from std_msgs.msg import String
import os
import subprocess
 

msg_textSpeech = String("")

def textSpeech(data):
  global msg_gspeech
  msg_gspeech = data.data
  #rospy.loginfo("tts_eus.py Speech %s",msg_textSpeech)
  
  if(msg_gspeech != "repetition" or msg_gspeech != " "):
                  sayText(msg_gspeech)
                  

def sayText(data):

  global file_path, tts_path

  print "tts_eus: " + data
  text_file = open(file_path + '/script/input.txt', "w")
  text_file.write(data)
  text_file.close()				
  
  script_path = file_path + 'script/'
  audio_path = file_path + 'audio/'
  cmd_tts = 'sh ' + script_path + 'ahotts.sh' + ' ' +  tts_path + ' ' + script_path + 'input.txt' + ' ' + audio_path + 'say_text.wav'
  rospy.loginfo("%s", cmd_tts)
  os.system(cmd_tts)
  
  #Plays a WAV file
  os.system('cvlc --play-and-exit ' + audio_path + 'say_text.wav')
  #subprocess.call('cvlc --play-and-exit /home/bee/robotak/nao/ros/src/nao_rsait/nao_speech_eus/audio/say_text.wav')
  

class Say():
  def __init__(self):
    global file_path, tts_path  
    file_path = String("")
    file_path = rospy.get_param('file_path')
    tts_path = String("")
    tts_path = rospy.get_param('tts_path')

    # ROS initialization:
    rospy.init_node('nao_tts_eus')
    # Subscribe to 
    rospy.Subscriber("/tts/eu/text", String, textSpeech)
		
  def shutdown(self):
    self.unsubscribe()
    # Shutting down broker seems to be not necessary any more
    # try:
    #     self.broker.shutdown()
    # except RuntimeError,e:
    #     rospy.logwarn("Could not shut down Python Broker: %s", e)
    
if __name__ == '__main__':

    ROSSay = Say()

    rospy.spin()
    
    rospy.loginfo("Stopping tts_eus module ...")
    exit(0)
