class Account(object):
    def __init__(self, id, telegramID,username,api_key_twitter,api_secret_key_twitter,api_key_facebook,api_key_instagram,lang):
        self.id = id
        self.telegramID = telegramID
        self.username=username
        self.lang=lang
    
    """ INSERT """
    async def create_users(tgID,username,lng,pool):
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"INSERT INTO users VALUES(0,'{tgID}','{username}','{lng}')")
                    await conn.commit()
        except Exception as e:
            print(f"{e}\nError in classes.account.get_lang")
            
    """SELECT"""
    async def check_all_user(pool):
        
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM users")
                    res = await cur.fetchall()        
            return res
        except Exception as e:
            print("Error DB in check_list_all_global_tournament")
            print(e)
            
    async def check_user(tgID,pool):      
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM users WHERE telegramID='{tgID}'")
                    res = await cur.fetchone()        
            return res
        except Exception as e:
            print("Error DB in check_list_all_global_tournament")
            print(e)

    