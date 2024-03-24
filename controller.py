# 导入所需的模块和库
import fastapi
from fastapi import Request
from service import BLL

# 创建FastAPI应用
app = fastapi.FastAPI()


# 用户注册接口
@app.post("/register")
async def register(register_form: Request):
    """
        Expected input: {
            "username": 用户名,
            "password": 密码
        }
        
        Expected return: {
            "code": 200: 正常 | 400: 权限不足 | 403: 用户名重复
        }
    """
    register_form = await register_form.json()
    # print(data)
    # > {'username': 'test', 'password': 'test'}
    return BLL.register(register_form)


# 用户登录接口
@app.post("/login")
async def login(login_form: Request):
    """
        Expected input: {
            "username": 用户名,
            "password": 密码
        }
        
        Expected return: {
            "code": 200: 正常 | 401: 密码错误 | 404: 用户不存在
        }
    """
    login_form = await login_form.json()
    return BLL.login(login_form)


# 聊天接口
@app.post("/chat")
async def chat(chat_form: Request):
    """
        Expected input: {
            "username": 用户名,
            "agent_id": 智能体id,
            "message": 用户与智能体的全部对话, 对话内容需要遵从指定格式, 如下面的message
        }
        "message": {
            "text": [
                {"role": "user", "content": "用户说的第一句话"},
                {"role": "assistant", "content": "AI说的第一句话"},
                {"role": "user", "content": "用户说的第二句话"},
                {"role": "assistant", "content": "AI说的第二句话"}
            ]
        }
        
        Expected return: {
            "code": 200: 正常 | 400: 权限不足 | 404: 智能体不存在
            "massage": 智能体回复给用户的一句话, 同样需要遵循上文的message格式
        }
    """
    chat_form = await chat_form.json()
    return BLL.chat(chat_form)


# 查找用户接口(管理员接口)
@app.post("/find_user")
async def find_user(find_user_form: Request):
    """
        Expected input: {
            "username": 用户名
        }
        
        Expected return: {
            "code": 200: 正常 | 404: 用户不存在,
            "username": 用户名,
            "password": 用户密码,
            "user_level": 用户级别，需要在["ADMIN", "USER"]里取值
        }
    """
    find_user_form = await find_user_form.json()
    return BLL.find_user(find_user_form)


# 查找所有用户接口(管理员接口)
@app.post("/find_all_users")
async def find_all_users(find_all_users_form: Request):
    """
        Expected input: {
            "username": 用户名, 必须是ADMIN, 否则会返回400
        }
        
        Expected return: {
            "code": 200: 正常 | 400: 权限不足 | 404: 用户不存在
            "users": [
                {
                    "username": 用户名,
                    "password": 用户密码,
                    "user_level": 用户级别，需要在["ADMIN", "USER"]里取值
                },
                ……
            ]
        }
    """
    find_all_users_form = await find_all_users_form.json()
    return BLL.find_all_users(find_all_users_form)


# 查找智能体接口
@app.post("/find_agent")
async def find_agent(find_agent_form: Request):
    """
        Expected input: {
            "username": 用户名, 必须是ADMIN, 否则会返回400,
            "agent_id: 智能体id
        }
        
        Expected return: {
            "code": 200: 正常 | 400: 权限不足 | 404: 智能体不存在
            "agent_id": 智能体id,
            "agent_name": 智能体名,
            "prompt": 智能体的prompt, 如果是共有智能体的则会返回None,
            "agent_type": 智能体类型, 取值于["OFFICIAL_LEVEL", "USER_LEVEL"],
            "username_belongs_to": agent.username_belongs_to
        }
    """
    find_agent_form = await find_agent_form.json()
    return BLL.find_agent(find_agent_form)


# 查找所有智能体接口
@app.post("/find_all_agents")
async def find_all_agents(find_all_agents_form: Request):
    """
        Expected input: {
            "username": 用户名, 必须是ADMIN, 否则会返回400
        }
        
        Expected return: {
            "code": 200: 正常 | 400: 权限不足 | 404: 智能体不存在
            "users": [
                {
                    "agent_id": 智能体id,
                    "agent_name": 智能体名,
                    "prompt": 智能体的prompt,
                    "agent_type": 智能体类型, 取值于["OFFICIAL_LEVEL", "USER_LEVEL"],
                    "username_belongs_to": agent.username_belongs_to
                },
                ……
                
            ]
        }
    """
    find_all_agents_form = await find_all_agents_form.json()
    return BLL.find_all_agents(find_all_agents_form)


# 添加智能体接口
@app.post("/add_agent")
async def add_agent(add_agent_form: Request):
    """
        Expected input: {
            "agent_name": 智能体名
            "agent_type": ['OFFICIAL_LEVEL', 'USER_LEVEL']
            "prompt": prompt格式与message相同
            "username_belongs_to": 动作发起用户, 管理员是ADMIN
        }
        
        Expected return: {
            "code": 200: 正常 | 400: 权限不足 | 403: 智能体已存在
        }
    """
    add_agent_form = await add_agent_form.json()
    return BLL.add_agent(add_agent_form)


# 更新智能体接口
@app.post("/update_agent")
async def update_agent(update_agent_form: Request):
    """
        Expected input: {
            "agent_id": 智能体id,
            "agent_name": 智能体名,
            "prompt": prompt格式与message相同,
        }
        
        Expected return: {
            "code": 200: 正常 | 400: 权限不足 | 404: 智能体不存在 | 403: 数据库异常
        }
    """
    update_agent_form = await update_agent_form.json()
    return BLL.update_agent(update_agent_form)


# 删除智能体接口
@app.post("/delete_agent")
async def delete_agent(delete_agent_form: Request):
    """
        Expected input: {
            "agent_id": 智能体id,
            "username": 用户名,
        }
        
        Expected return: {
            "code": 200: 正常 | 400: 权限不足 | 404: 智能体不存在 | 403: 数据库异常
        }
    """
    delete_agent_form = await delete_agent_form.json()
    return BLL.delete_agent(delete_agent_form)


# 更新用户接口
@app.post("/update_user")
async def update_user(update_user_form: Request):
    """
        Expected input: {
            "username": 用户名
            "password": 密码
        }
        
        Expected return: {
            "code": 200: 正常 | 404: 用户不存在
        }
    """
    update_user_form = await update_user_form.json()
    return BLL.update_user(update_user_form)


# 查找用户可见的接口
@app.post("/find_available_agents")
async def update_user(find_available_agents_form: Request):
    """
        Expected input: {
            "username": 用户名, 必须是ADMIN, 否则会返回400
        }
        
        Expected return: {
            "code": 200: 正常 | 400: 权限不足 | 404: 用户不存在,
            "users": [
                {
                    "agent_id": 智能体id,
                    "agent_name": 智能体名,
                    "prompt": 智能体的prompt, 如果是官方的智能体会返回None
                    "agent_type": 智能体类型, 取值于["OFFICIAL_LEVEL", "USER_LEVEL"],
                    "username_belongs_to": agent.username_belongs_to
                },
                ……
                
            ]
        }
    """
    find_available_agents_form = await find_available_agents_form.json()
    return BLL.find_available_agents(find_available_agents_form)


# 运行FastAPI应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
