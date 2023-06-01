# # init org-db based on relationships in yaml with access such that only managers can modify the subordinates



# # CREATE (john:Person {name: 'John Doe', role: 'CEO', email: 'john.doe@example.com'})
# # CREATE (jane:Person {name: 'Jane Smith', role: 'VP of Engineering', email: 'jane.smith@example.com'})
# # CREATE (alice:Person {name: 'Alice Johnson', role: 'Software Development Manager', email: 'alice.johnson@example.com'})
# # CREATE (bob:Person {name: 'Bob Brown', role: 'Software Developer', email: 'bob.brown@example.com'})

# # CREATE (john)-[:MANAGES]->(jane)
# # CREATE (jane)-[:MANAGES]->(alice)
# # CREATE (alice)-[:MANAGES]->(bob)

# from neo4j import GraphDatabase

# class Neo4jService:
#     def __init__(self, uri, user, password):
#         self._driver = GraphDatabase.driver(uri, auth=(user, password))

#     def close(self):
#         self._driver.close()

#     def write_data(self, user_role, query, parameters=None):
#         if user_role != 'read_write':
#             raise Exception('User does not have write permission')
#         with self._driver.session() as session:
#             return session.write_transaction(self._create_and_return, query, parameters)

#     @staticmethod
#     def _create_and_return(tx, query, parameters):
#         return tx.run(query, parameters)
