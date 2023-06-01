"""Multiagent system model"""
import os
import importlib
from tempfile import NamedTemporaryFile
from selinon import run_flow

from utils.envars import MAS_UID
  
class MultiAgentSystem:  
    def __init__(self, uid):
      self.uid = uid
      
      self.internal_messenger = Messenger(creds)
      
      
      # get topics from db
      topics = ['internal_broadcast']
      self.internal_messenger.consume_messages(topics[0], self._)
      
      # connect perceptors
      self.innate_interoceptor.consume_messages(self._perceive_internal_event)
      self.innate_exteroceptor.consume_messages(self._perceive_external_event)
    
        
    @perceptor
    def _perceive_internal_event(self, payload):
      """
        Default handler for perceiving internal events
      """
      self.execute_skill('handle_internal_event', payload)
    
    @perceptor
    def _perceive_external_event(self, payload):
      """
        Default handler for perceiving external events
      """
      self.execute_skill('handle_external_event', payload)
            
    @executor
    def execute_skill(self, skill_name, payload):
      """
        Execute the handler with the stimulus
      """
      
      # TODO - load skill/code from name trigger
      skill = self.memory.get_skill(skill_name)
      
      # write the flow definition to a temporary file
      with NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(skill['code'])
            tmp_file_path = f.name

      # import the flow definition from the temporary file
      file_name = os.path.splitext(os.path.basename(tmp_file_path))[0]
      module = __import__(file_name)


      module_name = 'skills'
      module = importlib.import_module(module_name)
      flow_cls = getattr(module, skill_name)
      flow_result = run_flow(flow_cls, payload)

      # Check the result of the flow execution
      if flow_result.is_success():
          print("Flow executed successfully!")
          print(f"Results: {flow_result.result}")
      else:
          print("Flow execution failed:")
          print(f"Errors: {flow_result.errors}")

      # Remove the temporary file
      os.remove(tmp_file_path)