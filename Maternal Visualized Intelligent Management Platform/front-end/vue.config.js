module.exports = {
    devServer: {
        port: 8082, // 设置前端服务端口为8082，避免与后端冲突
        proxy: {
            '/api': {
                target: 'http://localhost:8081', // 修正代理目标到后端端口8081
                changeOrigin: true,
                // 不重写路径，保留/api前缀，因为后端API使用/api前缀
            },
        },
    },
};