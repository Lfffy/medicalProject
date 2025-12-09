module.exports = {
    devServer: {
        port: 8082, // 设置前端服务端口为8082，避免与后端冲突
        proxy: {
            '/api': {
                target: 'http://localhost:8081', // 修正代理目标到后端端口8081
                changeOrigin: true,
                ws: true, // 启用WebSocket代理
                // 移除pathRewrite，保留/api前缀
            },
            '/socket.io': {
                target: 'http://localhost:8081',
                changeOrigin: true,
                ws: true, // 为Socket.IO添加WebSocket支持
                pathRewrite: {
                    '^/socket.io': '/socket.io'
                }
            }
        },
    },
};