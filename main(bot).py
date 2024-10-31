import request_gpt
from config import token, host_BD, user_BD, password_BD, db_name

import asyncpg
import time

from aiogram import Bot, Dispatcher, types
import asyncio

async def connect_db():
    try:
        connection = await asyncpg.connect(
            host=host_BD,
            user=user_BD,
            password=password_BD,
            database=db_name,
        )
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

bot = Bot(token=token["API_KEY"])
dp = Dispatcher()

@dp.message()
async def promt(message: types.Message):
    connection = await connect_db()
    if connection:
        try:
            user = await connection.fetchrow(f"""SELECT id FROM "User" WHERE id = {message.from_user.id}""")
            if user:
                try:
                    answer = request_gpt.get_answer(message.text)
                    await message.reply(answer)
                except:
                    await message.reply("Error 500 (Internal Server Error)")
            else:
                await message.reply("Error 403 (Forbidden)")
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            await connection.close()
    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())








    # connection = await connect_db()
    # if connection:
    #     try:
    #         await connection.execute(f"""
    #             INSERT INTO "User"
    #             VALUES ({message.from_user.id}, '{message.from_user.username}', '{message.from_user.first_name}')
    #             ON CONFLICT (id) DO NOTHING;
    #         """)
    #     except Exception as e:
    #         print(f"Database error: {e}")
    #     finally:
    #         await connection.close()