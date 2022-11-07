import {Menu} from 'antd';


function Navigator() {
    const items = [
        { label: '最近观看', key: 'recent' }, // 菜单项务必填写 key
        { label: '未来清单', key: 'future' },
    ];

    return (
        <Menu mode="horizontal"
              items={items}
              defaultSelectedKeys={['recent']}
        >
        </Menu>
    )
}
export default Navigator;