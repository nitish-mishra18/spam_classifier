package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

// Article struct
type Article struct {
	ID      int
	Title   string
	Content string
}

// Create table
func createTable(db *sql.DB) {
	query := `
	CREATE TABLE IF NOT EXISTS articles (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT,
		content TEXT
	);`
	_, err := db.Exec(query)
	if err != nil {
		log.Fatal(err)
	}
}

// Insert sample data
func insertData(db *sql.DB) {
	articles := []Article{
		{Title: "Go Language Basics", Content: "Go is fast and efficient"},
		{Title: "Machine Learning Intro", Content: "ML is future of AI"},
		{Title: "Deep Learning Guide", Content: "Neural networks are powerful"},
	}

	for _, a := range articles {
		_, err := db.Exec("INSERT INTO articles (title, content) VALUES (?, ?)", a.Title, a.Content)
		if err != nil {
			log.Fatal(err)
		}
	}
}

// Search function
func searchArticles(db *sql.DB, keyword string) {
	query := `
	SELECT id, title, content FROM articles
	WHERE title LIKE ? OR content LIKE ?;
	`

	rows, err := db.Query(query, "%"+keyword+"%", "%"+keyword+"%")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	fmt.Println("🔍 Search Results:")
	for rows.Next() {
		var a Article
		rows.Scan(&a.ID, &a.Title, &a.Content)
		fmt.Printf("ID: %d | Title: %s\nContent: %s\n\n", a.ID, a.Title, a.Content)
	}
}

func main() {
	db, err := sql.Open("sqlite3", "articles.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	createTable(db)
	insertData(db)

	var keyword string
	fmt.Print("Enter search keyword: ")
	fmt.Scanln(&keyword)

	searchArticles(db, keyword)
}
