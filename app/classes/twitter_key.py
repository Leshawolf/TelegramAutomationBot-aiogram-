import datetime

class TwitterKey(object):
    def __init__(self, id, tgID_user,api_key,api_secret,bearer_key,access_key,access_secret):
        self.id = id
        self.tgID_user = tgID_user
        self.api_key=api_key
        self.api_secret=api_secret
        self.bearer_key=bearer_key
        self.access_key=access_key
        self.access_secret=access_secret

    """SELECT"""
    async def check_user_key_twitter(tgID,id_account,pool):      
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM twitter_key WHERE tgID_user='{tgID}' and id='{id_account}'")
                    res = await cur.fetchone()        
            return res
        except Exception as e:
            print("Error DB in check_user_key_twitter")
            print(e)
            
    async def check_user_account_twitter(tgID,pool):      
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM twitter_key WHERE tgID_user='{tgID}'")
                    res = await cur.fetchall()        
            return res
        except Exception as e:
            print("Error DB in check_user_key_twitter")
            print(e)
            
    async def check_user_key_twitters(tgID,pool):      
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM twitter_key WHERE tgID_user='{tgID}'")
                    res = await cur.fetchone()        
            return res
        except Exception as e:
            print("Error DB in check_user_key_twitter")
            print(e)            

    async def check_user_active_key_twitter(tgID,pool):      
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM twitter_key WHERE tgID_user='{tgID}' and status=1")
                    res = await cur.fetchall()        
            return res
        except Exception as e:
            print("Error DB in check_user_active_key_twitter")
            print(e)
          
    async def check_keys_in_id(id,pool):      
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM twitter_key WHERE id='{id}'")
                    res = await cur.fetchone()        
            return res
        except Exception as e:
            print("Error DB in check_keys_in_id")
            print(e)  
            
    async def check_twitter_time(pool):      
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"SELECT * FROM tweeter_subscriptions WHERE status = 0 AND DATE_ADD(tweeter_subscriptions.date, INTERVAL 3 HOUR) <= NOW()")
                    res = await cur.fetchall()     
            return res
        except Exception as e:
            print("Error DB in check_user_key_twitter")
            print(e)
            


    """Update"""
    async def update_twitter_key(tgID,id,type_key,key,pool):      
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    if(type_key=="api"):
                        await cur.execute(f"UPDATE `twitter_key` SET `api_key`='{key}' WHERE `tgID_user`='{tgID}' and `id`={id}")
                        await conn.commit()
                    elif(type_key=="api_secret"):
                        await cur.execute(f"UPDATE `twitter_key` SET `api_secret`='{key}' WHERE `tgID_user`='{tgID}' and `id`={id}")
                        await conn.commit()
                    elif(type_key=="bearer"):
                        await cur.execute(f"UPDATE `twitter_key` SET `bearer_key`='{key}' WHERE `tgID_user`='{tgID}' and `id`={id}")
                        await conn.commit()
                    elif(type_key=="access"):
                        await cur.execute(f"UPDATE `twitter_key` SET `access_token`='{key}' WHERE `tgID_user`='{tgID}' and `id`={id}")
                        await conn.commit()
                    elif(type_key=="access_secret"):
                        await cur.execute(f"UPDATE `twitter_key` SET `access_secret`='{key}' WHERE `tgID_user`='{tgID}' and `id`={id}")
                        await conn.commit()
                    elif(type_key=="name"):
                        await cur.execute(f"UPDATE `twitter_key` SET `name_account`='{key}' WHERE `tgID_user`='{tgID}' and `id`={id}")
                        await conn.commit()
                    elif(type_key=="keyword"):
                        await cur.execute(f"UPDATE `twitter_key` SET `keyword`='{key}' WHERE `tgID_user`='{tgID}' and `id`={id}")
                        await conn.commit()
                    elif(type_key=="status"):
                        if(key=='1'): 
                            await cur.execute(f"UPDATE `twitter_key` SET `status`=0 WHERE `tgID_user`='{tgID}' and `id`={id} and `status`=1")
                            await conn.commit()
                        else:
                            await cur.execute(f"UPDATE `twitter_key` SET `status`=1 WHERE `tgID_user`='{tgID}' and `id`={id} and `status`=0")
                            await conn.commit()
            return True
        except Exception as e:
            print("Error DB update_twitter_key")
            print(e)  
            
    async def update_twitter_sub_status(tgID,pool):
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"UPDATE `tweeter_subscriptions` SET `status`=1 WHERE `id_sub`='{tgID}'")
                    await conn.commit()
            return True
        except Exception as e:
            print("Error DB update_twitter_key")
            print(e)  
    
    """INSERT"""
    async def create_tweeter_subscriptions(tgID,id_account,username_user_post,id_user_post,pool):
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"INSERT INTO tweeter_subscriptions VALUES(0,'{tgID}','{id_account}','{username_user_post}','{id_user_post}','{datetime.datetime.now()}',0)")
                    await conn.commit()
        except Exception as e:
            print(f"{e}\nError in classes.account.get_lang")
            
    async def create_new_account_twitter(tgID,id,pool):
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"INSERT INTO twitter_key VALUES(0,'{tgID}','Account{id}','','','','','','',0)")
                    await conn.commit()
        except Exception as e:
            print(f"{e}\nError in classes.account.get_lang")
            
    """DELETE"""
    async def delete_account_twitter(tgID, id, pool):
        try:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"DELETE FROM twitter_key WHERE tgID_user = '{tgID}' AND id = '{id}'")
                    await conn.commit()
        except Exception as e:
            print(f"{e}\nError in deleting twitter account")