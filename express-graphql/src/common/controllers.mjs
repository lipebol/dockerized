import { Service } from './service.mjs'
import { GetHandler } from './handlers/request-response/get.mjs'

export class Controllers {

    static async dates(request, response) {
        try {
            const set = new Set(request, response)
            request = set.Request()
            console.log(request)
            // console.log(new HasParams().Dates(request))
            console.log(new ThisParams().isDates(request))
            // if (new HasParams().Dates(request)) {
            //     const validation = await new ThisParams().isDates(request)
            //     if (typeof (validation) === process.env.TYPE_OBJECT) {
            //         const content = await set.Who(validation)
            //         return set.Response(content ? content : { NotFound: process.env.NOT_FOUND })
            //     }
            //     return set.Response({ BadRequest: process.env[validation] })
            // }
            // return set.Response({ BadRequest: process.env.REQUIRED_FIELDS })
        } catch (err) { return set.Response({ InternalServerError: err }) }
    }


    static async multi(request, response) {
        const handler = await GetHandler.create(request, response)
        if (handler.params && !handler.data?.error) {
            if (handler.db) {
                handler.data = await Service[handler.db](handler)
            }
            return GetHandler.response(handler)
        }
        return this.noparams(handler, response)
    }


    static async noparams(handler, response) {
        try {
            if (!handler.data?.error) {
                handler = handler.model && handler.db ?
                    handler : await GetHandler.create(handler, response)
                handler.data = await Service[handler.db](handler)
            }
            return GetHandler.response(handler)
        } catch (error) {
            console.log(error)
            GetHandler.response(response, { InternalServerError: err })
        }
    }
}