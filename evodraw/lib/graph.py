
from neo4j import GraphDatabase
from django.conf import settings

class EvoGraph(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_actor(self, actorname):
        with self._driver.session() as session:
            session.run("MERGE (u:Actor {name: $actorname})", actorname=actorname)

    def create_individual(self, individual):
        with self._driver.session() as session:
            session.run("MERGE (u:Individual {name: $individual})", individual=individual)

    def like(self, actorname, individual):
        with self._driver.session() as session:
            session.write_transaction(self._like, actorname, individual)

    def rate(self, actorname, individual, rating):
        with self._driver.session() as session:
            session.write_transaction(self._rate, actorname, individual, rating)

    def add_child(self,  child, parent):
        with self._driver.session() as session:
            session.write_transaction(self._child,  child, parent)

    def follows(self,  actor1, actor2):
        with self._driver.session() as session:
            session.write_transaction(self._follows,  actor1, actor2)

    def actor_role(self, actorname, individual, relationship):
        with self._driver.session() as session:
            session.write_transaction(self._author_role, actorname, individual, relationship )

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
               "MERGE (c)-[:CHILD_OF]->(p)",
               child=child, parent=parent)


    @staticmethod
    def _like(tx, actorname, individual):
        tx.run("MATCH (u:Actor {name: $actorname})"
               "MATCH (i:Individual {name: $individual}) "
               "MERGE (u)-[:LIKES]->(i)",
               actorname=actorname, individual=individual)

    @staticmethod
    def _rate(tx, actorname, individual, rating):
        tx.run("MATCH (u:Actor {name: $actorname})"
               "MATCH (i:Individual {name: $individual})"
               "MERGE (u)-[:RATES { rating: $rating } ]->(i)",
               actorname=actorname, individual=individual, rating=rating)

    @staticmethod
    def _author_role(tx, actorname, individual, relationship):
        tx.run("MATCH (a:Actor {name: $actorname})"
               "MATCH (i:Individual {name: $individual})"
               "MERGE (a)-[_:%s]->(i)" % relationship ,
               actorname=actorname, individual=individual, ROLE=relationship)

    @staticmethod
    def _follows(tx, actor1, actor2):
        tx.run("MATCH (a1:Actor {name: $actor1})"
               "MATCH (a2:Actor {name: $actor2})"
               "MERGE (a1)-[:FOLLOWS]->(a2)",
               actor1=actor1, actor2=actor2)

def has_graph():
    if hasattr(settings, 'GRAPH') and settings.GRAPH and hasattr(settings, 'GRAPHENEDB_URL'):
        return True
    else:
        return False


if __name__ == "__main__":
    eg = EvoGraph( 'bolt://localhost:7687','neo4j', 'masterkey')
    eg.delete_all()
    eg.create_actor('Benzo')
    eg.create_actor('Washi')
    eg.create_individual('pop:101')
    eg.create_individual('pop:102')
    eg.create_individual('pop:103')
    eg.add_child('pop:102', 'pop:101')
    eg.add_child('pop:103', 'pop:101')
    eg.like('Benzo', 'pop:102')
    eg.actor_role('Benzo','pop:102', 'EVOLVED')
    eg.actor_role('Washi', 'pop:101', 'AUTHORED')
    eg.actor_role('Washi', 'pop:103', 'OWNS')
    eg.rate('Benzo', 'pop:101', 5)
    eg.rate('Washi', 'pop:101', 2)
    eg.follows('Washi','Benzo')


