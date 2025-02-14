const service = require(process.env.SERVICE)
const { HasParams } = require(process.env.HAS_PARAMS)
const { ThisParams } = require(process.env.THIS_PARAMS)

/// mexer aqui, acrescentando tratamento de erros do "GraphQL"
const { get } = require(process.env.GETTERS)


// enviar erro para algum lugar, e passar uma mensagem padronizada
// depois alterar no 'Swagger'
class Controller {

    async dates(request, response) {
        try {
            const set = new Set(request, response)
            request = set.Request()
            if (new HasParams().Dates(request)) {
                const validation = await new ThisParams().isDates(request)
                if (typeof (validation) === process.env.TYPE_OBJECT) {
                    const content = await set.Who(validation)
                    return set.Response(content ? content : { NotFound: process.env.NOT_FOUND })
                }
                return set.Response({ BadRequest: process.env[validation] })
            }
            return set.Response({ BadRequest: process.env.REQUIRED_FIELDS })
        } catch (err) { return set.Response({ InternalServerError: err }) }
    }


    async multi(request, response) {
        try {
            const set = new Set(request, response)
            request = set.Request()
            if (request.params) {
                const validation = await new ThisParams().isMulti(request)
                if (typeof (validation) === process.env.TYPE_OBJECT) {
                    const content = await set.Who(validation)
                    return set.Response(content ? content : { NotFound: process.env.NOT_FOUND })
                }
                return set.Response({ BadRequest: process.env[validation] })
            }
            return this.noParams(request, response)
        } catch (err) { return set.Response({ InternalServerError: err }) }
    }


    async noParams(request, response) {
        try {
            const set = new Set(request, response)
            const content = await set.Who(request.model ? request : set.Request())
            return set.Response(content ? content : { NotFound: process.env.NOT_FOUND })
        } catch (err) { return this.set.Response({ InternalServerError: err }) }
    }
}


class Set {
    constructor(request, response) {
        this.request = request
        this.response = response
    }

    Request() {
        try {
            return this.request.route ? get.requestREST(this.request) : get.requestGraphQL(this.request)
        } catch (err) { console.log(err) }
    }

    async Who(object) {
        try {
            return object.model.includes(process.env.IS_MONGODB) ?
                await service.mongodb(object) : await service.sql(object)
        } catch (err) { console.log(err) }
    }

    Response(content) {
        try {
            return this.response ?
                get.responseREST(this.response, content) : Array.isArray(content) ? content : [content]
        } catch (err) { console.log(err) }
    }
}



const c_ = new Controller()

module.exports = { c_ }