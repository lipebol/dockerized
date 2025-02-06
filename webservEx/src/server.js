require('dotenv').config()
const cors = require(process.env.CORS)
const Express = require(process.env.SERVER)
const graphql = require(process.env.GRAPHQL)

const Server = Express()

Server.use(cors())

//Server.use(process.env.SLASH, Express.static(
//    process.env.STATIC, {
//    index: process.env.INDEX_PAGE,
//    extensions: [process.env.TYPE_HTML]
//})
//)

Server.use(process.env.API_GRAPHQL, graphql)

Server.use((req, res) => {
    if (
        (
            req.url.includes(process.env.API) && !(
                req.url.includes(process.env.DOC) || req.url.includes(process.env.GRAPHQL_TOOL)
            )
        )
    ) {
        return res.status(404).json({ error: process.env.NOT_FOUND })
    }
    return res.status(404).redirect(process.env._404)
})

Server.listen(process.env.SERVER_PORT)