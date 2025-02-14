const router = require(process.env.SERVER).Router()
const { createHandler } = require(process.env.GRAPHQL_HTTP)
const GraphiQL = require(process.env.GRAPHIQL).default
const { schemas } = require(process.env.GRAPHQL_SCHEMAS)
const { resolvers } = require(process.env.GRAPHQL_RESOLVERS)


router.all(process.env.SLASH, createHandler({ 
  schema: schemas, 
  rootValue: resolvers
}))

router.get(process.env.GRAPHQL_TOOL, GraphiQL({ endpoint: process.env.API_GRAPHQL }))

module.exports = router