from menu import create_menu
from config import bot, BotDB
import requests as r
from pycoingecko import CoinGeckoAPI
from time import sleep

cg = CoinGeckoAPI()

async def registration_user(message, user_id, referral=None):
    if(not BotDB.user_exists(user_id)):
        
        BotDB.register_user(user_id)

    return await message.answer('Привет, данный бот создан для отслеживания цен на земли, питомцев, кристаллы GENOPETS.', reply_markup=await create_menu(user_id))


async def get_stats(message):
    loading_message = await message.answer('Пожалуйста подождите...')
    attempt = 0
    except_rto = 0
    while attempt < 3:
        try:   
            # количество созданных земель
            if except_rto == 0:
                resp = r.get('https://api.solscan.io/account/tokens?address=BKMgh6yy27uVZQJxtNYQADv3P1sm93PC1MvpUTAX9ktP', timeout=4)
                count_lands = len(resp.json()['data'])
            else: count_lands = '!solscan_api_error'

            # genesis habitat
            headers = {
                'accept': '*/*',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'
            }
            floor_lands = []
            resp = r.get("https://jpn698dhc9.execute-api.us-east-1.amazonaws.com/prod/v1/shop?collection=genesis_genopets_habitats&limit=20&sort=lth", headers=headers)
            sol_floor_lands = resp.json()['result'][0]['listingPrice']
            for x in range(3):
                floor_lands.append(resp.json()['result'][x]['listingPrice'])
            resp = r.get("https://jpn698dhc9.execute-api.us-east-1.amazonaws.com/prod/v1/floorTraits?collection=genesis_genopets_habitats", headers=headers)
            lvl2_floor = resp.json()['Level']['2']['floorPrice']
            lvl3_floor = resp.json()['Level']['3']['floorPrice']

            # crystals nft
            resp = r.get("https://jpn698dhc9.execute-api.us-east-1.amazonaws.com/prod/v1/floorTraits?collection=genopets_refined_genotype_crystals", headers=headers)
            wood_nft = resp.json()['Elemental Type']['Wood']['floorPrice']
            earth_nft = resp.json()['Elemental Type']['Earth']['floorPrice']
            metal_nft = resp.json()['Elemental Type']['Metal']['floorPrice']
            water_nft = resp.json()['Elemental Type']['Water']['floorPrice']
            fire_nft = resp.json()['Elemental Type']['Fire']['floorPrice']

            # genopets
            floor_genopets = []
            resp = r.get("https://jpn698dhc9.execute-api.us-east-1.amazonaws.com/prod/v1/shop?collection=genopets&limit=20&sort=lth", headers=headers)
            sol_floor_genopets = resp.json()['result'][0]['listingPrice']
            for x in range(3):
                floor_genopets.append(resp.json()['result'][x]['listingPrice'])

            # habitat
            resp = r.get("https://jpn698dhc9.execute-api.us-east-1.amazonaws.com/prod/v2/collectionDetail?collection=genopets_habitats", headers=headers)
            habitat_floor = resp.json()['magicEdenFloorPrice']
            habitat_list_count = resp.json()['magicEdenListedCount']
            habitat_volume = resp.json()['magicEdenVolume']

            # ki and gene
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                'agent-id': '786e1f01-223b-4519-8ae1-9f2b818c50f4',
                'content-type': 'application/json; charset=utf-8',
                'origin': 'https://birdeye.so',
                'sec-ch-ua-platform': "Linux",
                'cf-be': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NjAyODExNjYsImV4cCI6MTY2MDI4MTQ2Nn0.W33Ohsde2qj2R8Cmt48bFai3adAcMxIyKNSNQ76P7zU',
                'referer': 'https://birdeye.so/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
            }
            # resp = r.get("https://api.birdeye.so/overview/token?address=kiGenopAScF8VF31Zbtx2Hg8qA5ArGqvnVtXb83sotc", headers=headers)
            # ki = resp.json()['data']['price']

            # resp = r.get("https://api.birdeye.so/overview/token?address=GENEtH5amGSi8kHAtQoezp1XEXwZJ8vcuePYnXdKrMYz", headers=headers)
            # gene = resp.json()['data']['price']

            for data in BotDB.get_token_price():
                sol = float(data[0])
                ki = float(data[1])
                gene = float(data[2])
            floor_genopets = str(floor_genopets).replace('[','',1).replace(']','',1)
            floor_lands = str(floor_lands).replace('[','',1).replace(']','',1)
            break
        except r.exceptions.ReadTimeout as ex:
            except_rto = 1
            print(ex)
        except Exception as ex:
            print(ex)
            attempt += 1
            sleep(1)
    # loading_message["message_id"]
    return await loading_message.edit_text(
        f'\U0001f3d4\uFE0F *Genesis Habitat*\
        \n3 самые дешевые земли на ME: *{floor_lands}* SOL | *({round(sol_floor_lands * sol, 1)}$)*\
        \nLevel 2: *{lvl2_floor}* SOL *({round(lvl2_floor*sol,2)}$)* | Level 3: *{lvl3_floor}* SOL *({round(lvl3_floor*sol,2)}$)*\n\
        \n\U0001f5fb *Habitat*\
        \nMagicEden Floor: *{habitat_floor}* SOL *({round(float(habitat_floor)*sol, 2)}$)*\
        \nВыставлено на продажу: *{habitat_list_count}*\
        \nTrade Volume: *{habitat_volume}* SOL\n\
        \n\U0001f7e4 Refined *Wood* Crystal (NFT): *{wood_nft}* SOL | *({round(wood_nft*sol, 1)}$)*\
        \n\U0001f7e2 Refined *Earth* Crystal (NFT): *{earth_nft}* SOL | *({round(earth_nft*sol, 1)}$)*\
        \n\u26AB Refined *Metal* Crystal (NFT): *{metal_nft}* SOL | *({round(metal_nft*sol, 1)}$)*\
        \n\U0001f535 Refined *Water* Crystal (NFT): *{water_nft}* SOL | *({round(water_nft*sol, 1)}$)*\
        \n\U0001f534 Refined *Fire* Crystal (NFT): *{fire_nft}* SOL | *({round(fire_nft*sol, 1)}$)*\n\
        \n\U0001f408 *Genesis Genopets*\
        \n3 самые дешевые петы на ME: *{floor_genopets}* SOL | *({round(sol_floor_genopets * sol, 1)}$)*\n\
        \n\U0001f4ca SOL: *{round(sol, 2)}$*\
        \n\U0001f4ca KI: *{round(ki, 4)}$*\
        \n\U0001f4ca GENE: *{round(gene, 4)}$*\
        \n\U0001f5fb Всего Habitat земель создано: *{count_lands}*', parse_mode="Markdown")



async def check_tokens_price():
    try:
        sol = round(cg.get_price(ids='solana', vs_currencies='usd')['solana']['usd'], 2)
        ki = round(cg.get_price(ids='genopet-ki', vs_currencies='usd')['genopet-ki']['usd'], 3)
        gene = round(cg.get_price(ids='genopets', vs_currencies='usd')['genopets']['usd'], 2)
        BotDB.send_token_price(sol, ki, gene)
    except Exception as ex:
        print(ex)