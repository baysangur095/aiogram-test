import aiosqlite

async def add_note(user_id, text):
    async with aiosqlite.connect('aiogram_db.db') as db:
        async with db.execute(
            "INSERT INTO notes (user_id, text) VALUES (?, ?)",
            (user_id, text)
        ) as cursor:
            await db.commit()
            return cursor.lastrowid

async def get_notes(user_id):
    async with aiosqlite.connect('aiogram_db.db') as db:
        async with db.execute('SELECT * FROM notes WHERE user_id = ?', (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return rows

async def delete_note(note_id, user_id):
    async with aiosqlite.connect("aiogram_db.db") as db:
        await db.execute("DELETE FROM notes WHERE note_id = ? AND user_id = ?", (note_id, user_id))
        await db.commit()












