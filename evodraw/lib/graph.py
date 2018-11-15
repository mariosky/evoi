
from neo4j import GraphDatabase


class EvoGraph(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()


    def create_user(self, username):
        with self._driver.session() as session:
            session.run("MERGE (u:User {name: $username})", username=username)

    def create_individual(self, individual):
        with self._driver.session() as session:
            session.run("MERGE (u:Individual {name: $individual})", individual=individual)


    def like(self, username, individual):
        with self._driver.session() as session:
            session.write_transaction(self._like, username, individual)

    def rate(self, username, individual, rating):
        with self._driver.session() as session:
            session.write_transaction(self._rate, username, individual, rating)

    def is_child(self,  child, parent):
        with self._driver.session() as session:
            session.write_transaction(self._child,  child, parent)

    def follows(self,  u1, u2):
        with self._driver.session() as session:
            session.write_transaction(self._follows,  u1, u2)

    def delete_all(self):
        with self._driver.session() as session:
            session.write_transaction(self._delete_all)

    @staticmethod
    def _delete_all(tx):
        tx.run("MATCH(n)"
               "DETACH DELETE n")
    @staticmethod
    def _child(tx, child, parent):
        tx.run("MATCH (p:Individual {name: $parent})"
               "MATCH (c:Individual {name: $child}) "
               "MERGE (c)-[:CHILD]->(p)",
               child=child, parent=parent)


    @staticmethod
    def _like(tx, username, individual):
        tx.run("MATCH (u:User {name: $username})"
               "MATCH (i:Individual {name: $individual}) "
               "MERGE (u)-[:LIKES]->(i)",
               username=username, individual=individual)

    @staticmethod
    def _rate(tx, username, individual, rating):
        tx.run("MATCH (u:User {name: $username})"
               "MATCH (i:Individual {name: $individual})"
               "MERGE (u)-[:RATING { rating: $rating } ]->(i)",
               username=username, individual=individual, rating=rating)

    @staticmethod
    def _follows(tx, username1, username2):
        tx.run("MATCH (u1:User {name: $username1})"
               "MATCH (u2:User {name: $username2})"
               "MERGE (u1)-[:FOLLOWS]->(u2)",
               username1=username1, username2=username2)



if __name__ == "__main__":
    eg = EvoGraph( 'bolt://localhost:7687','neo4j', 'masterkey')
    eg.delete_all()
    eg.create_user('Benzo')
    eg.create_user('Washi')
    eg.create_individual('pop:101')
    eg.create_individual('pop:102')
    eg.is_child('pop:101', 'pop:102')
    eg.like('Benzo','pop:102')
    eg.rate('Benzo', 'pop:101', 5)
    eg.rate('Washi', 'pop:101', 2)
    eg.follows('Washi','Benzo')


