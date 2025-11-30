import graphene
import core.schema
import social.schema

class Query(core.schema.Query, social.schema.Query, graphene.ObjectType):
    pass

class Mutation(core.schema.Mutation, social.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
