const {createProxyMiddleware} = require('http-proxy-middleware');

module.exports = function (app) {
    app.use('/api',
        createProxyMiddleware( {
            target: 'http://localhost:5000',//配置转发目标地址（能返回数据的服务器地址）
            changeOrigin: true,//控制服务器接收到的请求头中的host字段的值
            onProxyRes: function (proxyRes, req, res) {
                proxyRes.headers['Access-Control-Allow-Origin'] = '*';
            }
        })
    );
}