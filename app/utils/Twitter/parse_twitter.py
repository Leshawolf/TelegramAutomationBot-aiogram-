import asyncio
import json
import aiohttp
import requests
from twarc import Twarc2
import twarc
import itertools

from app.classes.twitter_key import TwitterKey
from app.loader import MYSQL_POOL

async def frts_req(link,headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(link,ssl=False,headers=headers) as resp:
            return await resp.json()

async def sec_req(link,headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(link,ssl=False,headers=headers) as resp:
            return await resp.json()

async def second_req(link,headers,data):
    async with aiohttp.ClientSession() as session:
        if data is not None:
            async with session.post(link,ssl=False,headers=headers,data=data) as resp:
                return await resp.json()
        else:
            async with session.get(link,ssl=False,headers=headers) as resp:
                return await resp.json()


#{'id': '1610371144112132098', 'name': 'Jan4un', 'username': 'Jan4un'}}
async def search_twit_key(headers,query):
        #Поиск постов
        api_link_search_twit_key=f"https://api.twitter.com/2/tweets/search/recent?query={query}"
        response_search_twit=await frts_req(api_link_search_twit_key,headers)
        return response_search_twit

async def search_username_in_id(headers,id_post):
    #Поиск пользователя по его id поста
    api_link_search_userpost=f"https://api.twitter.com/2/tweets/{id_post}?expansions=author_id&user.fields=username"
    response_search_username=await frts_req(api_link_search_userpost,headers)
    return response_search_username['data']

async def info_user_in_id(headers,id_user):
    api_link_info_user_in_id=f"https://api.twitter.com/2/users/{id_user}"
    response_info_user=await frts_req(api_link_info_user_in_id,headers)
    return response_info_user['data']

async def follow_user(consumer_key,consumer_secret,access_token,access_secret,user_id):
# Создаем объект Twarc с использованием ключей доступа
    t = twarc.Twarc(consumer_key, consumer_secret, access_token, access_secret)
    # Получаем информацию о пользователе, на которого хотим подписаться
    user_info = t.user_lookup(ids=[f"{user_id}"], id_type=f"{user_id}")
    # Подписываемся на пользователя
    try:
        response = t.post("https://api.twitter.com/1.1/friendships/create.json", data={"user_id": user_id})
        print(f"Подписка на  успешно оформлена!")
    except Exception as e:
        print(e)
        print(f"Не удалось подписаться на пользователя")
        
async def is_user_following_me(consumer_key,consumer_secret,access_token,access_secret,user_id):
    # Создаем объект Twarc с использованием ключей доступа
    t = twarc.Twarc(consumer_key, consumer_secret, access_token, access_secret)
    # Получаем информацию о подписке между текущим пользователем и указанным пользователем
    try:
        response = t.get("https://api.twitter.com/1.1/friendships/show.json", params={"source_id": user_id, "target_screen_name": t.username})
        data = await response.json()
        following = data["relationship"]["target"]["following"]
        if following:
            print(f"Пользователь с ID {user_id} подписан на вас!")
        else:
            print(f"Пользователь с ID {user_id} не подписан на вас.")
    except:
        print(f"Не удалось проверить подписку пользователя с ID {user_id}.")


async def like_last_3_tweets(consumer_key,consumer_secret,access_token,access_secret,user_id):
    # Создаем объект Twarc с использованием ключей доступа
    t = twarc.Twarc(consumer_key, consumer_secret, access_token, access_secret)
    # Получаем последние 3 твита пользователя
    timeline = t.timeline(user_id=user_id)
    for tweet in itertools.islice(timeline, 4):
        try:
            response = t.post("https://api.twitter.com/1.1/favorites/create.json", data={"id": tweet["id_str"]})
            print(f"Твит с ID {tweet['id_str']} успешно лайкнут!")
        except:
            print(f"Не удалось лайкнуть твит с ID {tweet['id_str']}.")
            
async def unlike_all_tweets(consumer_key,consumer_secret,access_token,access_secret,user_id):
    # Создаем объект Twarc с использованием ключей доступа
    t = twarc.Twarc(consumer_key, consumer_secret, access_token, access_secret)
    # Получаем список лайков пользователя
    try:
        likes = t.timeline(user_id=user_id)

        # Удаляем лайки
        for like in itertools.islice(likes,15):
            try:
                response = t.post("https://api.twitter.com/1.1/favorites/destroy.json", data={"id": like["id_str"]})
                print(f"Лайк с ID {like['id_str']} успешно удален!")
            except:
                print(f"Не удалось удалить лайк с ID {like['id_str']}.")
    except Exception as e:
        print(e)

async def is_follower(consumer_key, consumer_secret, access_token, access_token_secret,user_id):
    t = twarc.Twarc(consumer_key, consumer_secret, access_token, access_token_secret)
    #Получаем Информации о пользователе который авторизовывается
    try:
        response1 = t.get("https://api.twitter.com/1.1/account/verify_credentials.json")
        account_data = response1.json()
        # Проверка наличия нужного пользователя
        params = {'user_id': account_data['id']}
        response = t.get('https://api.twitter.com/1.1/followers/ids.json', params=params)
        data = response.json()
        follower_ids = data['ids']
        p=0 
        for item in follower_ids:
            if str(user_id) in str(item):
                p=1           
        if(p==1):
            return True
        else:
            return False
    except Exception as e:
        print(f"file: parse_twitter hand:is_follower\nError: {e}")

async def unfollow_user(consumer_key,consumer_secret,access_token,access_secret,user_id):
    # Создаем объект Twarc с использованием ключей доступа
    t = twarc.Twarc(consumer_key, consumer_secret, access_token, access_secret)
    # Отписываемся от пользователя
    try:
        response = t.post("https://api.twitter.com/1.1/friendships/destroy.json", data={"user_id": user_id})
        print(f"Отписка от пользователя с ID {user_id} прошла успешно!")
    except:
        print(f"Не удалось отписаться от пользователя с ID {user_id}.")

async def main_api_search(query,id_account,tgID):
    # Укажите ключевое слово, которое нужно искать
    try:
        key_user=await TwitterKey.check_keys_in_id(id_account,MYSQL_POOL)
        headers = {'Authorization': f'Bearer {key_user[5]}'}
        response_search_twit=await search_twit_key(headers,query)
        check=0
        for tweet_full in response_search_twit['data']:
            await asyncio.sleep(5)
            response_search_username=await search_username_in_id(headers,tweet_full['id'])
            for tweet in [response_search_username]:
                check=check+1
                await asyncio.sleep(5)
                full_info_user=await info_user_in_id(headers,tweet['author_id'])
                await asyncio.sleep(5)
                await TwitterKey.create_tweeter_subscriptions(tgID,id_account,full_info_user['username'],full_info_user['id'],MYSQL_POOL)
                await asyncio.sleep(5)
                await follow_user(key_user[3],key_user[4],key_user[6],key_user[7],full_info_user['id'])
                await asyncio.sleep(5)
                await like_last_3_tweets(key_user[3],key_user[4],key_user[6],key_user[7],full_info_user['id'])
                await asyncio.sleep(5)
        return check
    except requests.exceptions.HTTPError as e:
        print("File: parse_twitter -> main")
        print(e)
        check=-1
        return check
        
#Функция для поиска информации о пользователю по его id
async def get_all_info(headers,names):
    inf = dict()
    link = f'https://api.twitter.com/2/users/by?usernames={names}'
    rezz = await frts_req(link,headers)
    print(rezz)
    try:
        rr = rezz['data'][0]['id']
    except:
        return
    
async def chech_count_friend_users(name):
    b="*******"
    headers = {'Authorization': f'Bearer {b}'}
    link = f'https://api.twitter.com/1.1/users/show.json?screen_name={name}'
    rezz = await frts_req(link,headers)
    print(rezz)

