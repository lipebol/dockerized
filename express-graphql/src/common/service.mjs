import { Op } from 'sequelize'
import * as models from './models.mjs'

export class Service {

    static async sql(handler) {
        try {

            this.sequelize = new setSequelize(this.newObject())

            this.sequelize.order(object.filter)
            this.sequelize.attributes(object.fields)


            if (object.params) {
                if (object.params.dates === process.env.MAX) {
                    return await models[object.model].max(object.filter)
                }
                this.sequelize.where(object.filter, this.setParams(object.params, this.newObject()))
            }


            if (object.page) {
                this.sequelize.offset(this.setOffSet(object.page, this.setLimit))
                this.sequelize.limit(this.setLimit)
            } else if (handler.count) {
                handler.count = await models[handler.model]
                    .count(this.sequelize.finally())
                return {
                    total: handler.count,
                    pages: Math.ceil(parseFloat(rows) / handler.limit)
                }
            }

            return await models[object.model].findAll(this.sequelize.finally())
        } catch (err) { console.log(err) }
    }


    static async nosql(handler) {
        try {
            const data = await models[handler.model]
                .find(handler.where).sort({ [handler.filter]: 'asc' })
                .select(handler.fields).skip(handler.offset)
                .limit(handler.limit).populate(handler.lookup).exec()

            if (data.length === 0) {
                handler.error = { name: 'NotFound', status_code: 404 }
            }

            if (!handler.error && handler.info) {
                return {
                    count: data.length, countpages: Math.ceil(
                        parseFloat(data.length) / 100
                    )
                }
            }
            return data
        } catch (err) { console.log(err) }
    }
}


class setSequelize {
    constructor(objectJSON) { this.object = objectJSON }
    where(filter, params) {
        try {
            if (filter && params) {
                this.object.where = Object.keys(params).length === 1 ?
                    { [filter]: { [Op.in]: params.multi } } :
                    { [filter]: { [Op.between]: [new Date(params.start), new Date(params.end)] } }
            }
        } catch (err) { console.log(err) }
    }
    order(filter) { try { if (filter) { this.object.order = [[filter, 'ASC']] } } catch (err) { console.log(err) } }
    attributes(fields) { try { if (fields) { this.object.attributes = fields } } catch (err) { console.log(err) } }
    offset(offset) { try { if (offset) { this.object.offset = offset } } catch (err) { console.log(err) } }
    limit(limit) { try { if (limit) { this.object.limit = limit } } catch (err) { console.log(err) } }
    finally() { try { return this.object } catch (err) { console.log(err) } }
}