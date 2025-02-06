const { set } = require(process.env.SETTERS)

class GetRequestResponse {

    requestREST(request) {
        try {
            let [name, table, column] = set.url(request.originalUrl)
            set.model({ name, table })
            if (request.query && column) {
                set.filter({ name, column })
                set.query(request.query)
                if (request.query.page) { set.page(request.query.page) } else { set.count() }
            }
            return set.finally()
        } catch (err) { console.log(err) }
    }

    requestGraphQL(request) { try { return new GetRequestGraphQL(request).who() } catch (err) { console.log(err) } }

    responseREST(response, content) {
        try {
            this.status = parseInt(process.env[Object.keys(content).toString().toUpperCase()])
            return response.status(this.status ? this.status : 200).json(content)
        } catch (err) { console.log(err) }
    }
}


class GetRequestGraphQL {

    constructor(request) {
        this.request = request
        this.resolver = this.request.query || this.request.about.query
    }

    who() {
        try {
            switch (this.resolver) {
                // com 'argumentos', mas sem 'paginação'
                case '<QUERY_1>':
                    set.model('<NAME_MODEL_1>')
                    set.filter('nome_query')
                    set.param(this.request)
                    break
                case '<QUERY_2>':
                    set.model('<NAME_MODEL_2>')
                    break
                case '<QUERY_3>':
                    set.model('<NAME_MODEL_3>')
                    set.filter('param')
                    set.param(this.request)
                    set.fields(this.request.about.context)
                    break
                case '<QUERY_4>': /// <-- com 'argumentos', mas sem 'paginação'
                    set.model('<NAME_MODEL_4>')
                    set.filter(this.request)
                    set.param(this.request)
                    set.fields(this.request.about.context)
                    break
                case '<QUERY_5>': /// <-- sem 'argumentos', mas com 'paginação'
                    set.model('<NAME_MODEL_5>')
                    set.filter('param') /// <-- para ordenação
                    set.page(this.request.pagina)
                    set.fields(this.request.about.context)
                    break
                case 'genre': /// <-- com 'argumentos' e 'paginação'
                    set.model('M_GENRE')
                    set.filter(this.request)
                    set.param(this.request)
                    set.page(this.request.page)
                    set.fields(this.request.about.context)
                    break
                case 'artist': /// <-- com 'argumentos' e 'paginação'
                    set.model('M_ARTIST')
                    set.filter(this.request)
                    set.param(this.request)
                    set.page(this.request.page)
                    set.fields(this.request.about.context)
                    break
                case 'track': /// <-- com 'argumentos' e 'paginação'
                    set.model('M_TRACK')
                    set.filter(this.request)
                    set.param(this.request)
                    set.page(this.request.pagina)
                    set.lookup(['artist', 'genres'])
                    break
            }
            return set.finally()
        } catch (err) { console.log(err) }
    }
}

const get = new GetRequestResponse()

module.exports = { get }