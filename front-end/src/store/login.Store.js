import {makeAutoObservable} from "mobx";
import {http} from "../utils";

class LoginStore {
    token = ''

    constructor() {
        makeAutoObservable(this)
    }

    setToken = async ({username, password}) => {
        await http.post('')
    }
}

export default LoginStore