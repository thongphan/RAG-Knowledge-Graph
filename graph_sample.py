from repository.neo4j_repository import Neo4jRepository
def main():
    repo = Neo4jRepository()

    # Entities
    entities = [
        {"label": "Person", "name": "Nguyen Van A", "properties": {"age": 47, "sex": "Male"}},
        {"label": "Person", "name": "Nguyen Thi B"},
        {"label": "Person", "name": "Nguyen Van Teo"},
        {"label": "Person", "name": "Nguyen Thi C"},
        {"label": "Subject", "name": "Information Technology"},
        {"label": "Residence", "name": "Ho Chi Minh"},
        {"label": "Country", "name": "Vietnam"},
        {"label": "Company", "name": "Prudential Vietnam"},
    ]
    repo.create_entities(entities)

    # Relationships
    relationships = [
        {"from_label": "Person", "from": "Nguyen Van A", "to_label": "Person", "to": "Nguyen Thi B", "type": "MARRIED"},
        {"from_label": "Person", "from": "Nguyen Van A", "to_label": "Person", "to": "Nguyen Van Teo", "type": "HAVE"},
        {"from_label": "Person", "from": "Nguyen Van A", "to_label": "Person", "to": "Nguyen Thi C", "type": "HAVE"},
        {"from_label": "Person", "from": "Nguyen Van A", "to_label": "Subject", "to": "Information Technology",
         "type": "STUDIED"},
        {"from_label": "Person", "from": "Nguyen Van A", "to_label": "Company", "to": "Prudential Vietnam",
         "type": "WORKED"},
    ]
    repo.create_relationships(relationships)

    # Example query
    result = repo.query("MATCH p=(n)-[r]->(m) RETURN p, n.name AS name, m.name AS connected_to LIMIT 10")
    for record in result:
        print(record)

if __name__ == "__main__":
    main()


