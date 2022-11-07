// 导入模块
import recentStore from './recent.Store'
import React from "react"
class RootStore {
    // 组合模块
    constructor() {
        this.recentStore = new recentStore()
    }
}
// 实例化根store注入context
const StoresContext = React.createContext(new RootStore())
// 导出方法 供组件调用方法使用store根实例
export const useStore = () => React.useContext(StoresContext)
