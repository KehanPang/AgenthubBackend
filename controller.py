from dao import DAO
from zhipuai import ZhipuAI

class BusinessLogicLayer:
    def __init__(self):
        self.DAO = DAO
        api_key = "34fdbb9c8ce06a02a21aeed9e6b685c6.CMOwSsZwJoUc8W4Z"
        self.clinet = ZhipuAI(api_key=api_key) # 填写您自己的APIKey

    # 用户注册接口
    def register(self, register_form):
        return {
            "code": self.DAO.add_new_user(
                register_form['username'], 
                register_form['password']    
            )
        }
    
    # 用户登录接口
    def login(self, login_form):
        return {
            "code": self.DAO.login(
                login_form['username'], 
                login_form['password']
            )
        }

    # 聊天接口
    def chat(self, chat_form):
        agent_to_be_used = self.DAO.find_agent_by_id(chat_form['agent_id'])
        
        if agent_to_be_used == None:
            return {"code": 404} # 智能体不存在
        
        if chat_form['username'] != agent_to_be_used.username_belongs_to and agent_to_be_used.agent_type != "OFFICIAL_LEVEL":
            return {"code": 400} # 权限不足
        
        agent_prompt = agent_to_be_used.prompt
        final_prompt = agent_prompt + chat_form['message']['text']
        
        content = ""
        try:
            response = self.clinet.chat.completions.create(
                model="glm-4",  # 填写需要调用的模型名称
                messages=final_prompt,
            )
            content = response.choices[0].message.content
        except:
            content = "这个话题不太合适，我们换个话题吧。"
        
        return {
                    "code": 200,
                    "username": chat_form["username"],
                    "agent_id": chat_form["agent_id"],
                    "message": {
                    'text': [
                        {"role": "assistant", "content": content}
                        ]
                    }
        }


    # 查找用户接口
    def find_user(self, find_user_form):
        user = self.DAO.find_user_by_username(find_user_form["username"])
        
        if user == None:
            return {"code": 404}
        
        return {
            "code": 200,
            "username": user.username,
            "password": user.password,
            "user_level": user.user_level
        }

    # 查找所有用户接口
    def find_all_users(self, find_all_users_form):
        if find_all_users_form["username"] != "ADMIN":
            return {"code": 400}
        
        users = self.DAO.find_all_users()
        if users == None:
            return {"code": 404}
        
        user_list = []
        for user in users:
            user_list.append(
                {
                    "username": user.username,
                    "password": user.password,
                    "user_level": user.user_level
                }
            )
            
        return {
            "code": 200,
            "users": user_list
        }


    # 查找智能体接口
    def find_agent(self, find_agent_form):
        agent = self.DAO.find_agent_by_id(find_agent_form['agent_id'])
        
        if agent == None:
            return {"code": 404}
        
        if find_agent_form['username'] != agent.username_belongs_to and agent.agent_type != "OFFICIAL_LEVEL":
            return {"code": 400} # 权限不足
        
        return {
            "code": 200, #200表示正常 400表示智能体不存在 401表示用户权限不足
            "agent_id": agent.agent_id,
            "agent_name": agent.agent_name,
            "prompt": "" if agent.agent_type == "OFFICIAL_LEVEL" else agent.prompt,
            "agent_type": agent.agent_type,
            "username_belongs_to": agent.username_belongs_to
        }

    # 查找所有智能体接口
    def find_all_agents(self, find_all_agents_form):
        if find_all_agents_form["username"] != "ADMIN":
            return {"code": 400}
        
        agents = self.DAO.find_all_agents()
        if agents == None:
            return {"code": 404}
        
        agent_list = []
        for agent in agents:
            agent_list.append(
                {
                    "agent_id": agent.agent_id,
                    "agent_name": agent.agent_name,
                    "prompt": agent.prompt,
                    "agent_type": agent.agent_type,
                    "username_belongs_to": agent.username_belongs_to
                }
            )
        return {
            "code": 200,
            "users": agent_list
        }
        
    def update_user(self, update_user_form):
        return {
            "code": self.DAO.update_user_password(
                update_user_form['username'], update_user_form['password']
            )
        }

    # 添加智能体接口
    def add_agent(self, add_agent_form):
        return {
                "code": self.DAO.add_new_agent(
                    add_agent_form["agent_name"],
                    add_agent_form["agent_type"],
                    add_agent_form["prompt"],
                    add_agent_form["username_belongs_to"]
                )
        }

    # 更新智能体接口
    def update_agent(self, update_agent_form):
        return {
                "code": self.DAO.update_agent(
                    update_agent_form["agent_id"],
                    update_agent_form["username"],
                    update_agent_form["agent_name"],
                    update_agent_form["prompt"]
                )
        }

    # 删除智能体接口
    def delete_agent(self, delete_agent_form):
        return {
                "code": self.DAO.delete_agent(
                    delete_agent_form["username_belongs_to"],
                    delete_agent_form["agent_id"]
                )
        }
    
    # 返回用户可见的智能体接口
    def find_available_agents(self, find_available_agents_form):
        if find_available_agents_form["username"] != "ADMIN":
            return {"code": 400}
        
        agents = self.DAO.find_user_available_agents(find_available_agents_form["username"])
        if agents == None:
            return {"code": 404}
        
        agent_list = []
        for agent in agents:
            agent_list.append(
                {
                    "agent_id": agent.agent_id,
                    "agent_name": agent.agent_name,
                    "prompt": None if agent.agent.agent_type == "OFFICIAL_LEVEL" else agent.prompt,
                    "agent_type": agent.agent_type,
                    "username_belongs_to": agent.username_belongs_to
                }
            )
        return {
            "code": 200,
            "users": agent_list
        }


BLL = BusinessLogicLayer()
