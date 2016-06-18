import graphene
from wiki.schema import Query as WikiQuery, Mutation as WikiMutation


class Query(WikiQuery):
    """
    Query description
    """
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(WikiMutation):
    # This class will inherit from multiple Mutations
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(name='Wiki Schema')
schema.query = Query
# schema.mutation = Mutation
