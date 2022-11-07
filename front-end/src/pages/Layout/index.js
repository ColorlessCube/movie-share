import {Outlet} from 'react-router-dom'
import Navigator from "./navigation"
import {Layout} from 'antd'
import './index.scss'

const {Header, Footer, Content} = Layout


function PageLayout() {
    return (
        <div>
            <Layout>
                <Header className='header'>
                    <Navigator className='navigator'/>
                </Header>
                <Content><Outlet/></Content>
                <Footer className='footer'>@movie-share</Footer>
            </Layout>
        </div>
    )
}

export default PageLayout;