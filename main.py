from BraveProject_FDV.Session import Session, Session1
from BraveProject_FDV.Agent import Agent

if __name__ == "__main__":
 Session.register("session1", Session1)
 agent = Agent()
 agent.launch_session("session1")