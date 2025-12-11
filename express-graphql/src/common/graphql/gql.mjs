import { dirname, join } from 'path'
import { fileURLToPath } from 'url'
import { Router } from 'express'
import { createHandler } from 'graphql-http/lib/use/express'
import { schemas } from './handlers/schemas.mjs'
import { resolvers } from './handlers/resolvers.mjs'

const router = Router()

router.all(
    "/", createHandler(
        { schema: schemas, rootValue: resolvers, context: request => request }
    )
)
router.get("/tool", (_, response) => {
        response.sendFile(
            join(dirname(fileURLToPath(import.meta.url)), "./graphiql.html")
        )
    }
)

export default router