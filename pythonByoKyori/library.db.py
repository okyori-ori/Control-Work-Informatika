import sqlite3


def create_tables(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    available INTEGER DEFAULT 1)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS readers (
                    reader_id INTEGER,
                    name TEXT NOT NULL,
                    phone TEXT,
                    book_id INTEGER)""")


def add_book(cursor, title, author, year):
    cursor.execute("INSERT INTO books(title, author, year) VALUES(?,?,?)",
                   (title, author, year))


def add_reader(cursor, name, phone):
    cursor.execute("INSERT INTO readers(name, phone) VALUES(?,?)",
                   (name, phone))


def give_book(cursor, reader_id, book_id):
    cursor.execute("UPDATE books SET available = 0 WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE readers SET book_id = ? WHERE reader_id = ?",
                   (book_id, reader_id))


def return_book(cursor, book_id):
    cursor.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE readers SET book_id = NULL WHERE book_id = ?", (book_id,))


def get_available_books(cursor):
    cursor.execute("SELECT * FROM books WHERE available = 1")
    return cursor.fetchall()


def get_reader_books(cursor, reader_id):
    cursor.execute("SELECT book_id FROM readers WHERE reader_id = ?", (reader_id,))
    return cursor.fetchall()


# def search_books(cursor, keyword):
#     cursor.execute


if __name__ == '__main__':
    with sqlite3.connect('library.db') as conn:
        cur = conn.cursor()

        create_tables(cur)

        add_book(cur, "Война и мир", "Лев Толстой", 1869)
        add_book(cur, "Преступление и наказание", "Фёдор Достоевский", 1866)
        add_book(cur, "1984", "Джордж Оруэлл", 1949)

        add_reader(cur, "Иван Иванов", "+79991234567")
        add_reader(cur, "Мария Петрова", "+79997654321")

        give_book(cur, 1, 1)

        print("Доступные книги после выдачи:")
        print(get_available_books(cur))

        return_book(cur, 1)

        print("\nДоступные книги после возврата:")
        print(get_available_books(cur))