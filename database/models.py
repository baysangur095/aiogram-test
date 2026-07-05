import aiosqlite

async def create_table():
    async with aiosqlite.connect('aiogram_db.db') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT )
            
        """)
        await db.commit()
        print("Database connected successfully!")

