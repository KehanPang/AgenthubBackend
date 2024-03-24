from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from schema import *

class DataAccessObjectLayer:
    def __init__(self):
        engine = create_engine('sqlite:///AgentHub.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    # 创建一个新的User对象并添加到数据库中
    def add_new_user(self, username, password, user_level='USER'):
        if user_level not in ['ADMIN', 'USER']:
            return 400 # 用户类型错误
        new_user = User(username=username, user_level=user_level, password=password)
        self.session.add(new_user)
        try:
            self.session.add(new_user)
            self.session.commit()
        except SQLAlchemyError as _:
            self.session.rollback()
            return 403 # 用户已存在
    
    def login(self, username, password):
        user = self.find_user_by_username(username)
        if not user:
            return 404 # 用户不存在
        else:
            if user.password == password:
                return 200 # 登録済み
            else:
                return 401 # Password Error
    
    def delete_user(self, username):
        # 查询要删除的用户
        user_to_delete = self.session.query(User).filter_by(username=username).first()
        if user_to_delete:
            try:
                self.session.delete(user_to_delete)
                self.session.commit()
                return 200 # 删除成功
            except SQLAlchemyError as _:
                self.session.rollback()
                return 403 # ユーザーはありません
        else:
            return 404 # ユーザーはありません
    
    def find_user_by_username(self, username):
        # 根据用户名查询用户
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            return user
        return None

    def find_all_users(self):
        # 查询所有用户
        users = self.session.query(User).all()
        if users:
            return users
        return users
    
    def update_user_password(self, username, new_password):
        # 查询要修改密码的用户
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            try:
                # 更新用户密码
                user.password = new_password
                self.session.commit()
                return 200 # 更新成功
            except SQLAlchemyError as _:
                # 捕获并处理异常
                self.session.rollback()
                return 403 # 更新失败
        else:
            return 404 # 用户不存在
    
    def add_new_agent(self, agent_name, agent_type, prompt, username_belongs_to):
        if agent_type not in ['OFFICIAL_LEVEL', 'USER_LEVEL']:
            return 401 # 类型错误
        if username_belongs_to != 'ADMIN' and agent_type == 'OFFICIAL_LEVEL':
            return 400 # 权限不足
        new_agent = Agent(agent_name=agent_name, agent_type=agent_type, prompt=prompt, username_belongs_to=username_belongs_to)
        self.session.add(new_agent)
        try:
            self.session.commit()
            return 200 # 添加成功
        except SQLAlchemyError as _:
            self.session.rollback()
            return 403 # 添加失败，智能体已存在
    
    def delete_agent(self, username, agent_id):
        agent_to_delete = self.session.query(Agent).filter_by(agent_id=agent_id).first()
        if not agent_to_delete:
            return 404
        if agent_to_delete.username_belongs_to != username and username != "ADMIN":
            return 400 # 权限不足
        try:
            self.session.delete(agent_to_delete)
            self.session.commit()
            return 200 # 删除成功
        except SQLAlchemyError as _:
            self.session.rollback()
            return 403 # 更新失败
    
    def update_agent(self, username, agent_id, agent_name, prompt):
        agent = self.session.query(Agent).filter_by(agent_id=agent_id).first()
        if not agent:
            return 404 # 智能体不存在
        if agent.username_belongs_to != username and username != "ADMIN":
            return 400 # 权限不足
        try:
            # 更新用户密码
            agent.agent_name = agent_name
            agent.prompt = prompt
            self.session.commit()
            return 200 # 更新成功
        except SQLAlchemyError as _:
            # 捕获并处理异常
            self.session.rollback()
            return 403 # 更新失败

    def find_agent_by_id(self, agent_id):
        agent = self.session.query(Agent).filter_by(agent_id=agent_id).first()
        if agent:
            return agent
        return None

    def find_agent_by_username(self, username):
        agent = self.session.query(Agent).filter_by(username_belongs_to=username).first()
        if agent:
            return agent
        return None

    def find_user_available_agents(self, username):
        agents = self.session.query(Agent).filter_by(
            or_(agent_type='OFFICIAL_LEVEL', username_belongs_to=username)).all()
        return agents

    def find_all_agents(self):
        agents = self.session.query(Agent).all()
        if agents:
            return agents
        return agents
        
DAO = DataAccessObjectLayer()
