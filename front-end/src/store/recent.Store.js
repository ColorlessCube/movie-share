import {makeAutoObservable} from "mobx";
import {http} from "../utils";


class RecentStore {
    recentMedias = []

    constructor() {
        makeAutoObservable(this)
    }

    getRecentMedia = async ({offset, limit, type}) => {
        const res = await http.post('/api/media/recent', {
            page: {
                offset: offset,
                limit: limit
            },
            search: {
                type: type
            }
        })
        this.recentMedias = res.data.data.data
        this.recentMedias.forEach(item => {
            item.thumb = 'http://127.0.0.1:5000/assets/' + item.id + '.thumb.jpg'
        })
    }
}

export default RecentStore