from util.query_runner import QueryRunner
from core.db_factory import DBFactory

def main():
    kg = DBFactory.get_neo4j_vector_db()
    runner = QueryRunner(kg)
    runner.run()

if __name__ == "__main__":
    main()