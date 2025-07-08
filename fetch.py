import csv
from Bio import Entrez

Entrez.email = "test@example.com"  # Replace with your email

def fetch_pubmed_data(query, max_results=3):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    id_list = record["IdList"]

    papers = []
    if id_list:
        handle = Entrez.efetch(db="pubmed", id=",".join(id_list), retmode="xml")
        fetch_records = Entrez.read(handle)

        for article in fetch_records['PubmedArticle']:
            title = article['MedlineCitation']['Article'].get('ArticleTitle', 'No title')
            journal = article['MedlineCitation']['Article']['Journal']['Title']
            authors = article['MedlineCitation']['Article'].get('AuthorList', [])
            author_names = [f"{a.get('ForeName', '')} {a.get('LastName', '')}".strip() for a in authors]
            papers.append({
                "title": title,
                "journal": journal,
                "authors": author_names
            })
    return papers

def save_to_csv(papers, filename="pubmed_results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Journal", "Authors"])
        for paper in papers:
            writer.writerow([paper["title"], paper["journal"], ", ".join(paper["authors"])])

if __name__ == "__main__":
    print("Starting fetch...")
    results = fetch_pubmed_data("machine learning", max_results=3)
    print("Fetch complete!\n")

    for idx, paper in enumerate(results, 1):
        print(f"📄 Paper {idx}:")
        print("Title:", paper["title"])
        print("Journal:", paper["journal"])
        print("Authors:", ", ".join(paper["authors"]))
        print()

    # ✅ These two lines must be aligned to the left, not inside the for loop
    save_to_csv(results)
    print("✅ Results saved to pubmed_results.csv")


